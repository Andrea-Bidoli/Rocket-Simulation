import numpy as np

class cylinder:
    I = None
    def __init__(self, mass: float, diameter:float, height:float):
        """retunr a new cylinder object

        Args:
            mass (float): total mass of the cylinder
            diameter (float): diameter of the cylinder
            height (float): height of the cylinder
        """
        self.mass = mass
        self.diameter = diameter
        self.height = height
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

class cone:
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
        
class fin:
    CG = None
    I = None
    def __init__(self, mass: float, height: float, mean_chord: float, taper: float):
        """return a new fin object

        Args:
            mass (float): total mass of the fin
            height (float): height of the fin
            mean_chord (float): mean chord of the fin
            taper (float): ratio between the tip chord and the root chord
        """
        self.mass = mass
        self.height = height
        self.mean_chord = mean_chord
        self.taper = taper
        self.calc_I()
        self.calc_CG()

    def calc_I(self):
        pass
    def calc_CG(self):
        pass
    
class engine(cylinder):
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
        self.calc_I()
        self.calc_CG()

class struct_rocket:
    """ fin position: relative to the cylinder, if n>1, the position is axysimetric of the cylinder"""
    tank_pos_rel_cylinder =np.array([0, 0, 0])
    cone_pos_rel_cylinder = np.array([0, 0, 0])
    fin_pos_rel_cylinder = np.array([0, 0, 0])
    n_fins = 0

    I = np.array([0, 0, 0])
    
    def __init__(self, n_fins: int, *parts):
        """retunr a new struct_rocket object

            the origin of the rocket is at the bottom of the cylinder in the center of the base and with the positive z axis pointing up

        Args:
            n_fin (int): number of fins
            **parts: dict of rocket parts, must be in order from bottom to top
             exaple: struct_rocket(engine, cylinder, fin, tank, cone)
        """
        self.n_fins = n_fins
        self.parts = parts
        self.tank_pos_rel = np.array([0, 0, self.parts[3].height/2])  # distance between the tank CG and the bottom of the cylinder
        self.fin_pos_rel_cylinder = np.array([0, 0, 0])  # distance between the fin CG and the bottom of the cylinder
        self.cone_pos_rel_cylinder = np.array([0, 0, 0]) # distance between the cone CG and the bottom of the cylinder
        self.calc_I()
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
    c1 = cylinder(3, 1, 3)
    c2 = cone(2/3, 1, 2)
    t1 = tank(1, 1, 2, 1)
    e1 = engine(0.8, 1, 0.5, 100)
    f1 = fin(0.2, 1, 1, 0.5)
    
    print(c1.CG)
    print(c2.CG)
    print(t1.CG)
    print(e1.CG)
    print(f1.CG)
    rocket = struct_rocket(3, e1, c1, f1, t1, c2)