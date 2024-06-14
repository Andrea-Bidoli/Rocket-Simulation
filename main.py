import numpy as np
import rocket_generator as rg
import computer
g = np.array([0, 0, -9.81])


class runner:
    def __init__(self, computer: computer, rocket: rg.Rocket):
        self.computer = computer
        self.rocket = rocket
    def run(self):
        pass

