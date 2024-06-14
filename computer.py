import rocket_generator as rg
import numpy as np


parts = {rg.engine: [], rg.fin: []}

position = np.array([0, 0, 0])
velocity = np.array([0, 0, 0])
acceleration = np.array([0, 0, 0])

target_pry = np.zeros(3)
current_pry = np.zeros(3)

thrust_pitch = 0 # thruster pitch in %
thrust_yaw = 0 # thurster yaw in %

def __init__(rocket: rg.rocket, throttle=1, thrust_pitch=0, thrust_yaw=0):
    global mass
    # engine axis_rel_rocket
    throttle = throttle
    thrust_pitch = thrust_pitch
    thrust_yaw = thrust_yaw
    mass = rocket.mass
    
    for part in rocket.parts:
        match part:
            case rg.engine:
                parts[rg.engine].append(part)
            case rg.fin:
                parts[rg.fin].append(part)
            case _:
                pass

def guidence():
    """guidence of the rocket to the target pitch, roll, and yaw"""
    delta = target_pry - current_pry
    

def update_mass():
    ...

def calc_acceleration():
    """calculate the acceleration of the rocket based on the thrust of the engines"""
    ax, ay, az = 0
    for part in parts[rg.engine]:
        ax += part.thrust[0]/mass
        ay += part.thrust[1]/mass
        az += part.thrust[2]/mass
    acceleration = np.array([ax, ay, az])

def set_pry( pitch: float, roll: float, yaw: float):
    """set the target pitch, roll, and yaw of the rocket

    Args:
        pitch (float): pitch of the rocket from up in degrees
        roll (float): roll of the rocket from North in degrees
        yaw (float): yaw of the rocket from /*East*/ in degrees
    """
    target_pry = np.array([pitch, roll, yaw])