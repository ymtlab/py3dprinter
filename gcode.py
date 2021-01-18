# -*- coding: utf-8 -*-
import numpy as np

class Gcode(object):

    def __init__(self, text):
        self.data = []
        self.count = 0
        self.lines = text.split('\n')
        self.start_lines, self.print_lines, self.end_lines = self.split_lines()
        self.max_count = len(self.print_lines[1])

    def split_lines(self):
        def m107count(lines):
            count = 0
            for i, line in enumerate(lines):
                key = line.split(' ')[0]
                if key == 'M107':
                    count = count + 1
                if count > 1:
                    return i
        
        start = m107count(self.lines) + 1
        end = len(self.lines) - m107count(self.lines[::-1]) - 1

        start_lines = self.lines[:start]
        print_lines = self.lines_to_ndarray(self.lines[start:end])
        end_lines = self.lines[end:]

        return start_lines, print_lines, end_lines

    def lines_to_ndarray(self, print_lines):
        arr = [[0, 0, 0, 0, 0, 0]]
        keys = []

        for line in print_lines:
            splited = line.split(' ')
            d = { s[0].strip() : float(s[1:]) for s in splited[1:] }
            a = []
            for i, key in enumerate(['X', 'Y', 'Z', 'E', 'F', 'S']):
                if key in d:
                    a.append( d.get(key) )
                else:
                    a.append( arr[-1][i] )
            keys.append( splited[0] )
            arr.append(a)

        return [ keys, np.array(arr[1:]) ]
