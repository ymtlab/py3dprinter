
class Pi3DP():
    def __init__(self, pi):
        self.pi = pi
        self.x = TMC2208(self.pi)
        self.y = TMC2208(self.pi)
        self.z = TMC2208(self.pi)
        self.e = TMC2208(self.pi)
        self.nozzle_heater = Heater()
        self.heat_bed = Heater()

    def jog(self, x, y, z, e):
        self.x.out(x)
        self.y.out(y)
        self.z.out(z)
        self.e.out(e)
 
class TMC2208():
    def __init__(self, pi, step_pin=0, dir_pin=0):
        self.pi = pi
        self.step_pin = step_pin
        self.dir_pin = dir_pin

    def set_mode(self, mode):
        self.pi.set_mode(self.step_pin, mode)
        self.pi.set_mode(self.dir_pin, mode)

    def move(self, arr):
        self.pi.write(self.step_pin, arr[0])
        self.pi.write(self.dir_pin, arr[1])
        self.pi.write(self.step_pin, 0)
        self.pi.write(self.dir_pin, 0)
        
    def out(self, arr):
        if self.pi is None:
            pass
        else:
            self.pi.write(self.step_pin, arr[0])
            self.pi.write(self.dir_pin, arr[1])

class Heater():
    def __init__(self):
        self.a = 0
