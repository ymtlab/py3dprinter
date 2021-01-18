import numpy as np

class V3dp(object):
    def __init__(self, graph):
        self.graph = graph
        self.x_axis = graph.items[2]
        self.z_axis = graph.items[3]

    def set_coordinate(self, coordinate):
        x, y, z = coordinate[0], coordinate[1], coordinate[2]
        self.x_axis.pos = np.array( [[-10, y, 100], [230, y, 100]] )
        self.z_axis.pos = np.array( [] )
