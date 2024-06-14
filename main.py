import numpy as np
import rocket_generator as rg

g = np.array([0, 0, -9.81])

class Computer:
    parts = {rg.engine: [], rg.fin: []}

    position = np.array([0, 0, 0])
    velocity = np.array([0, 0, 0])
    acceleration = np.array([0, 0, 0])

    
    t_pitch = 0
    t_yaw = 0
    
    def __init__(self, rocket: rg.rocket, throttle=1, t_pitch=0, t_yaw=0):
        # engine axis_rel_rocket
        self.throttle = throttle
        self.t_pitch = t_pitch
        self.t_yaw = t_yaw
        
        self.mass = rocket.mass
        for part in rocket.parts:
            
            match part:
                case rg.engine:
                    self.parts[rg.engine].append(part)
                case rg.fin:
                    self.parts[rg.fin].append(part)
                case _:
                    pass
            
    def update_mass(self):
        self.mass -= self.fuel_burn_rate
    
    def calc_acceleration(self):
        for part in self.parts[rg.engine]:
            ax += part.thrust[0]/self.mass
            ay += part.thrust[1]/self.mass
            az += part.thrust[2]/self.mass
    
    def set_engine_pitch_yaw(self, pitch, yaw):
        for engine in self.parts[rg.engine]:
            engine.e_pitch_perc = pitch
            engine.e_yaw_perc = yaw
            engine.calc_thrust()