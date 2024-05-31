import numpy as np
import rocket_generator as rg

g = np.array([0, 0, -9.81])

class Computer:
    struct_rocket = None
    
    angles = np.array([0, 0, 0])
    position = np.array([0, 0, 0])
    velocity = np.array([0, 0, 0])
    acceleration = np.array([0, 0, 0])
    
    thrust = np.array([0, 0, 0])
    
    def __init__(self, struct_rocket: rg.struct_rocket, throttle=1, t_pitch=0, t_yaw=0):
        self.struct_rocket = struct_rocket
        # engine axis_rel_rocket
        self.engine_angles[0] = t_pitch
        self.engine_angles[1] = t_yaw
        self.throttle = throttle
    
    def update_velocity(self):
        self.velocity += self.acceleration
    
    def update_acceleration(self):
        if self.fuel_mass > 0:
            self.acceleration = self.thrust*self.throttle / self.struct_rocket.get_wet_mass() - g
        else:
            self.acceleration = -g

    def update_position(self):
        self.x_distance += self.velocity*np.cos(self.pitch)
        self.height += self.velocity*np.sin(self.pitch)

    def update_mass(self):
        self.mass -= self.fuel_burn_rate
    
    def update_thrust(self):
        for part in self.struct_rocket.parts:
            if isinstance(part, rg.engine):
                part.set_throttle(self.throttle)
                