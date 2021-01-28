import numpy as np
import pigpio, time
import pandas as pd

class Gcode(object):

    def __init__(self, text):
        self.axis_order = ['X', 'Y', 'Z', 'E']
        self.mm_pulse_factor = [1, 1, 1, 1]
        self.pulse_counts = np.array([])
        self.pulse_counts_index = 0
        self.pulse_array_buffer = []
        self.pulse_array_buffer_index = 0

        lines = text.split('\n')

        s = self.index_of(lines, 'M107', 1) + 1
        e = len(lines) - self.index_of(lines[::-1], 'M107', 1) - 1

        if s == 0 and e == len(lines):
            self.start_chunk = []
            self.end_chunk = []
            self.print_chunk = pd.DataFrame(
                [ { s[0].strip() : float(s[1:]) for s in line.split(' ') } for line in lines ]
                , columns=['X', 'Y', 'Z', 'E', 'F', 'S', 'G', 'M']
            ).fillna(method="ffill").fillna(0)
        else:
            self.start_chunk = lines[:s]
            self.end_chunk = lines[e:]
            self.print_chunk = pd.DataFrame(
                [ { s[0].strip() : float(s[1:]) for s in line.split(' ') } for line in lines[s:e] ]
                , columns=['X', 'Y', 'Z', 'E', 'F', 'S', 'G', 'M']
            ).fillna(method="ffill").fillna(0)

    def index_of(self, arr, search_key, counts):
        count = 0
        for i, line in enumerate(arr):
            key = line.split(' ')[0]
            if key == search_key:
                count = count + 1
            if count > counts:
                return i
        return -1

    def mm_to_pulse_factor_for_belt_pulley(self, belt_pitch, pulley_tooth, motor_pulse_rate, microstep=1):
        '''
        belt_pitch [mm]
        pulley_tooth [T]
        motor_pulse_rate [pulse/rev]
        return [pulse/mm]
        '''
        feed = belt_pitch * pulley_tooth # mm/rev
        factor = motor_pulse_rate * microstep / feed # [pulse/rev] / [mm/rev] = [pulse/mm]
        return factor

    def to_pulse(self):
        gcode_diff = np.diff(self.print_chunk[['X', 'Y', 'Z', 'E']], n=1, axis=0)
        array_length = gcode_diff.shape[0]
        factor_array = np.array([np.full( array_length, i ) for i in self.mm_pulse_factor]).T
        self.pulse_counts = (gcode_diff * factor_array).astype(np.int64)
        self.pulse_array_buffer = self.pulse_array()
        
    def pulse_array(self):
        #input  [X_COUNT, Y_COUNT, Z_COUNT, E_COUNT]
        #output [ [X_STEP], [X_DIR], [Y_STEP], [Y_DIR], [Z_STEP], [Z_DIR], [E_STEP], [E_DIR] ]

        pulse_count = self.pulse_counts[self.pulse_counts_index]
        self.pulse_counts_index = self.pulse_counts_index + 1
        
        count = int( max(np.abs(pulse_count)) )
        if count == 0:
            #return np.array([ [0] for i in pulse_count ])
            pulse_count = self.pulse_counts[self.pulse_counts_index]
            self.pulse_counts_index = self.pulse_counts_index + 1
            count = int( max(np.abs(pulse_count)) )
        
        arr = []
        for i in pulse_count:
            if i == 0:
                arr.append( np.zeros(count, np.uint8) )
                arr.append( np.zeros(count, np.uint8) )
            else:
                arr.append( np.full(count, ( np.sign(i) - 1 ) / 2 * (-1), np.uint8) )
                if count - abs(i) == 0:
                    arr.append( np.full(count, 1, np.uint8) )
                else:
                    a = count/(count - abs(i))
                    b = np.mod(np.arange(0, count), a)
                    b = b.astype(np.uint8)
                    c = np.where(b > 0, 1, 0)
                    arr.append(c)
        return np.array(arr).T

    def pulse(self):
        pulse = self.pulse_array_buffer[self.pulse_array_buffer_index]
        self.pulse_array_buffer_index = self.pulse_array_buffer_index + 1
        if self.pulse_array_buffer_index > len(self.pulse_array_buffer) - 1:
            self.pulse_array_buffer = self.pulse_array()
            self.pulse_array_buffer_index = 0
        return pulse

def main():

    print('calcurate pulse array')

    with open('programs/data/XYZcube.gco', 'r') as f:
        gcode = Gcode( f.read() )

    f = gcode.mm_to_pulse_factor_for_belt_pulley(2, 20, 200, 8)
    gcode.mm_pulse_factor = [f, f, f, f]
    gcode.to_pulse()
    
    print('gpio setting')

    X_STEP = 27
    X_DIR  = 17
    Y_STEP = 23
    Y_DIR  = 22
    ENABLE = 24
    velocity = 0.000001

    pi = pigpio.pi()
    pi.set_mode(X_STEP, pigpio.OUTPUT)
    pi.set_mode(Y_STEP, pigpio.OUTPUT)
    pi.set_mode(X_DIR,  pigpio.OUTPUT)
    pi.set_mode(Y_DIR,  pigpio.OUTPUT)
    pi.set_mode(ENABLE, pigpio.OUTPUT)
    pi.write( ENABLE, 0 )

    print('move motor')

    try:
        while True:
            p = gcode.pulse()
            #print(p)
            pi.write( X_DIR,  p[0] )
            pi.write( X_STEP, p[1] )
            pi.write( Y_DIR,  p[2] )
            pi.write( Y_STEP, p[3] )
            time.sleep(velocity)
            pi.write( X_STEP, 0 )
            pi.write( Y_STEP, 0 )
            time.sleep(velocity)
    except(KeyboardInterrupt): # when ctrl+c is pressed
        pi.write( X_DIR,  0 )
        pi.write( X_STEP, 0 )
        pi.write( Y_DIR,  0 )
        pi.write( Y_STEP, 0 )
        pi.write( ENABLE, 1 )
        pi.stop()
        print('\nstop motor')

if __name__ == '__main__':
    main()