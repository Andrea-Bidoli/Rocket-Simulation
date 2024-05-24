import numpy as np
from copy import deepcopy

R_matrix = lambda theta: np.array([[np.cos(theta), -np.sin(theta), 1], [np.sin(theta), np.cos(theta), 1]])

class part:
    versori = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    children = {}
    
    def __init__(self, diameter: float, height: float, mass: float):
        self.diameter = diameter
        self.height = height
        self.mass = mass
        self.CG = np.array([0, 0, height/2])
        
    def add_child(self, child, offset):
        self.children[child] = offset
        self.calc_child_CG()

    def calc_child_CG(self):
        for cpart in self.children:
            self.CG = (self.CG*self.mass + (cpart.CG+self.children[cpart])*cpart.mass)/ (self.mass + cpart.mass)
            self.mass += cpart.mass
        
class cylinder(part):
    I = None
    def __init__(self, mass: float, diameter:float, height:float):
        """retunr a new cylinder object

        Args:
            mass (float): total mass of the cylinder
            diameter (float): diameter of the cylinder
            height (float): height of the cylinder
        """
        super().__init__(diameter, height, mass)
        self.mass = mass
        self.calc_I()
        self.calc_CG()
        
    def calc_I(self):
        Ixy = 1/12 * self.mass * (3*(self.diameter/2)**2 + self.height**2)
        Iz = 1/2 * self.mass * (self.diameter/2)**2
        self.I = np.array([Ixy, Ixy, Iz])
    
    def calc_CG(self):
        self.CG = np.array([0, 0, self.height/2])

class tank(cylinder):
    def __init__(self, mass: float, diameter: float, height:float, fuel_mass: float):
        """return a new tank object

        Args:
            mass (float): dry mass of the tank
            diameter (float): diameter of the tank
            height (float): height of the tank
            fuel_mass (float): mass of the fuel
        """
        super().__init__(mass, diameter, height)
        self.fuel_mass = fuel_mass
        self.mass += self.fuel_mass
        self.calc_I()
        self.calc_CG()

class cone(part):
    I = None
    CG = None
    def __init__(self, mass: float, diameter: float, height: float):
        """return a new cone object

        Args:
            mass (float): total mass of the cone
            diameter (float): diameter of the cone
            height (float): height of the cone
        """
        self.mass = mass
        self.diameter = diameter
        self.height = height
        self.calc_I()
        self.calc_CG()
        
    def calc_I(self):
        Iz = 3/10 * self.mass * (self.diameter/2)**2
        Ixy = 3/20 * self.mass * ((self.diameter/2)**2+4*self.height**2)
        self.I = np.array([Ixy, Ixy, Iz])        

    def calc_CG(self):
        self.CG = np.array([0, 0, self.height/4])        
        
class fin(part):
    CG = None
    I = None
    def __init__(self, mass: float, height: float, mean_chord: float, taper: float):
        super().__init__(0, height, mass)
        """return a new fin object

        Args:
            mass (float): total mass of the fin
            height (float): height of the fin
            mean_chord (float): mean chord of the fin
            taper (float): ratio between the tip chord and the root chord
        """
        self.mean_chord = mean_chord
        self.taper = taper 
        self.root_chord = 2*self.mean_chord/(1+self.taper)
        self.tip_chord = self.root_chord*self.taper
        self.area = mean_chord*height
        
        self.calc_I()
        self.calc_CG()

    def calc_I(self):
        pass

    def calc_CG(self):
        ...
    
class engine(cylinder):
    throttle = 0
    def __init__(self, mass: float, diameter: float, height: float, max_thrust: float):
        """return a new engine object

        Args:
            mass (float): dry mass of the engine
            diameter (float): diameter of the engine
            height (float): height of the engine
            fuel_mass (float): mass of the fuel
            thrust (float): thrust of the engine
        """
        super().__init__(mass, diameter, height)
        self.max_thrust = max_thrust
        self.thrust = self.max_thrust * self.throttle
        self.calc_I()
        self.calc_CG()
        
    def set_throttle(self, new_throttle):
        self.throttle = new_throttle        
        self.thrust = self.throttle * self.max_thrust
        
class structural_rocket(part):
    
    root = None
    I = np.array([0, 0, 0])
    CT = np.zeros(3) # center of thrust
    
    def __init__(self, root_part: cylinder):
        """retunr a new structural_rocket object

            the origin of the rocket is at the bottom of the cylinder in the center of the base and with the positive z axis pointing up

        Args:
            n_fin (int): number of fins
            *parts: list of rocket parts, must be in order from bottom to top and be paired in a tuple with the offset from origin 
            exaple: structural_rocket(engine, cylinder, fin, tank, cone)
        """
        """ fin position: relative to the cylinder, if n>1, the position is axysimetric of the cylinder"""    
        self.root = root_part
        self.CG = root_part.CG.copy()
        self.mass = root_part.mass
        self.add_child(root_part, np.array([0, 0, 0]))
        self.CG = root_part.CG.copy()

    def get_dry_mass(self):
        pass
    
    def get_wet_mass(self):
        pass
    
    def get_GC(self):
        pass
    
    def get_Ct(self):
        pass
    
    def calc_I(self):
        pass            

if __name__ == "__main__":
    # base parts of the rocket
    c1 = cylinder(3, 2, 3)
    c2 = cone(2/3, 2, 2)
    t1 = tank(1, 1, 2, 1)
    e1 = engine(0.8, 1, 0.5, 100)
    # rocket parts tree
    rocket_parts_tree = {
        
            e1:np.array([0, 0, 0]),
            c1:np.array([0, 0, 0]),
            t1:np.array([0, 0, e1.height]),
            c2:np.array([0, 0, c1.height]),
    }
    # rocket assembly
    rocket = structural_rocket(c1)
    rocket.add_child(e1, rocket_parts_tree[e1])
    rocket.add_child(t1, rocket_parts_tree[t1])
    rocket.add_child(c2, rocket_parts_tree[c2])
        
    print(rocket.CG)