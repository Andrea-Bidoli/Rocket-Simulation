import numpy as np

R_matrix = lambda theta: np.array([[np.cos(theta), -np.sin(theta), 1], [np.sin(theta), np.cos(theta), 1]])

class part:
    versori = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    children = {}
    
    def __init__(self, diameter: float, height: float, mass: float|None =None):
        self.diameter = diameter
        self.height = height
        self.mass = mass if mass is not None else diameter*height
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
    def __init__(self, diameter: float, height: float, mass: float | None = None):
        super().__init__(diameter, height, mass)
        """retunr a new cylinder object

        Args:
            mass (float): total mass of the cylinder
            diameter (float): diameter of the cylinder
            height (float): height of the cylinder
        """
        self.calc_I()
        self.calc_CG()
        
    def calc_I(self):
        Ixy = 1/12 * self.mass * (3*(self.diameter/2)**2 + self.height**2)
        Iz = 1/2 * self.mass * (self.diameter/2)**2
        self.I = np.array([Ixy, Ixy, Iz])
    
    def calc_CG(self):
        self.CG = np.array([0, 0, self.height/2])

class tank(cylinder):
    def __init__(self, diameter: float, height: float, fuel_mass:float,  mass: float | None = None):
        super().__init__(diameter, height, mass)
        """return a new tank object

        Args:
            mass (float): dry mass of the tank
            diameter (float): diameter of the tank
            height (float): height of the tank
            fuel_mass (float): mass of the fuel
        """
        self.fuel_mass = fuel_mass
        self.mass += self.fuel_mass
        self.calc_I()
        self.calc_CG()

class cone(part):
    I = None
    CG = None
    def __init__(self, diameter: float, height: float, mass: float | None = None):
        super().__init__(diameter, height, mass)
        """return a new cone object

        Args:
            mass (float): total mass of the cone
            diameter (float): diameter of the cone
            height (float): height of the cone
        """
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
    def __init__(self, mean_chord: float, height: float, taper:float, mass: float | None = None):
        super().__init__(mean_chord, height, mass)
        """return a new fin object

        Args:
            mass (float): total mass of the fin
            height (float): height of the fin
            mean_chord (float): mean chord of the fin
            taper (float): ratio between the tip chord and the root chord
        """
        self.mean_chord = self.diameter
        self.taper = taper 
        self.root_chord = 2*self.mean_chord/(1+self.taper)
        self.tip_chord = self.root_chord*self.taper
        self.area = self.mean_chord*height
        self.calc_I()
        self.calc_CG()

    def calc_I(self):
        pass

    def calc_CG(self):
        xg = (self.tip_chord**2 + self.root_chord**2 + self.tip_chord*self.root_chord)/(3*(self.tip_chord+self.root_chord))
        yg = self.height*(2*self.tip_chord+self.root_chord)/(3*(self.tip_chord+self.root_chord))
        self.CG = np.array([xg, 0, yg])
    
class engine(cylinder):
    throttle = 0
    engine_angles = np.zeros(2)
    max_angle = np.deg2rad(30)
    thrust = np.zeros(3)
    e_pitch_perc=0
    e_yaw_perc=0
    
    def __init__(self, diameter: float, height: float, flow: float, max_thrust: float, mass: float | None = None):
        super().__init__(diameter, height, mass)
        """return a new engine object

        Args:
            mass (float): dry mass of the engine
            diameter (float): diameter of the engine
            height (float): height of the engine
            fuel_mass (float): mass of the fuel
            thrust (float): thrust of the engine
        """
        self.max_thrust = max_thrust
        self.flow = flow
        self.calc_CG()
        self.calc_I()
        
    def set_throttle(self, new_throttle):
        self.throttle = new_throttle        
        self.calc_thrust()
    
    def set_pitch(self, pitch):
        if -100>pitch>100:
            raise ValueError("pitch must be between -100 and 100 or -1 and 1")
        self.e_pitch_perc = pitch/100 if pitch>1 or pitch<-1 else pitch
    
    def set_yaw(self, yaw):
        if -100>yaw>100:
            raise ValueError("yaw must be between -100 and 100 or -1 and 1")
        self.e_yaw_perc = yaw/100 if yaw>1 or yaw<-1 else yaw
    
    def calc_thrust(self):
        pitch_angle = self.max_angle*self.e_pitch_perc
        yaw_angle = self.max_angle*self.e_yaw_perc
        self.thrust[0] = self.throttle*self.max_thrust*np.sin(pitch_angle)
        self.thrust[1] = self.throttle*self.max_thrust*np.sin(yaw_angle)
        self.thrust[2] = self.throttle*self.max_thrust*np.cos(pitch_angle)*np.cos(yaw_angle)
        
class structural_rocket(part):
    
    root = None
    I = np.zeros(3) # inertia tensor
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
        self.I = root_part.I.copy()

    def calc_mass(self):
        for part in self.children:
            self.mass += part.mass

    def get_Ct(self):
        for part in self.children:
            if type(part) == engine:
                self.CT += part.CG
    
    def calc_I(self):
        for part in self.children:
            dist = np.linalg.norm(part.CG-self.CG)
            self.I = self.I+part.I+part.mass*dist**2

if __name__ == "__main__":
    # base parts of the rocket
    c1 = cylinder(1, 2)
    c2 = cone(1, 2)
    t1 = tank(1, 1, 2)
    e1 = engine(1, 1, 0.5, 100)
    # rocket parts tree
    rocket_parts_tree = {
            e1:np.array([0, 0, 0]),
            c1:np.array([0, 0, 0]),
            t1:np.array([0, 0, e1.height]),
            c2:np.array([0, 0, c1.height]),
    }
    # rocket assembly
    e1.set_throttle(1)
    e1.set_pitch(10)
    e1.set_yaw(0)
    e1.calc_thrust()
    print(f"thrust: {e1.thrust} |thrust: {np.linalg.norm(e1.thrust)}|")