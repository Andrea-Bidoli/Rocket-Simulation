import numpy as np

class Rocket:
    mass = 0
    fuel_mass = 0
    fuel_burn_rate = 0
    fuel_burn_time = 0
    thrust = 0
    
    velocity = 0
    acceleration = 0
    x_distance = 0
    height = 0
    
    pitch = 0
    roll = 0
    yaw = 0
    
    thrust_pitch = 0
    thrust_roll = 0
    thrust_yaw = 0
    
    height = 0
    diameter = 0
    def __init__(self, diameter, height, mass, fuel_mass, fuel_burn_rate, fuel_burn_time, pitch=0, roll=0, yaw=0):
        self.diameter = diameter
        self.height = height
        self.mass = mass
        self.fuel_mass = fuel_mass
        self.fuel_burn_rate = fuel_burn_rate
        self.fuel_burn_time = fuel_burn_time
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw
        self.thrust = 0
        self.thrust_pitch = 0
        self.thrust_roll = 0
        self.thrust_yaw = 0
        self.velocity = 0
    
    def update_velocity(self):
        self.velocity += self.acceleration
        