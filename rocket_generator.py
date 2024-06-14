import numpy as np

# 2D matrix rotation
R_matrix = lambda theta: np.array([[np.cos(theta), -np.sin(theta), 1], [np.sin(theta), np.cos(theta), 1]])

class part:
    versori = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    O = np.array([0, 0, 0])
    def __init__(self, base: float, height: float, mass: float|None =None):
        self.base = base
        self.height = height
        self.mass = mass if mass is not None else base*height
        self.CG = np.array([0, 0, height/2])
        
    def add_child(self, child, offset: np.array|list|tuple = (0, 0, 0)):
        if isinstance(offset, (list, tuple)):
            offset = np.array(offset)
        child.O = self.O + offset
        self.calc_CG(child)

    def calc_CG(self, cpart:'part'):
        """
            must run on the root part
        """
        self.CG = ((self.CG*self.mass) + (cpart.O+cpart.CG*cpart.mass)) / (self.mass + cpart.mass)
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
    max_angle = np.deg2rad(15)
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
        theta = np.arctan2(self.e_pitch_perc, self.e_yaw_perc)
        phi = np.sqrt(self.e_pitch_perc**2 + self.e_yaw_perc**2)*self.max_angle
        
        self.thrust[0] = self.throttle*self.max_thrust*np.sin(phi)*np.cos(theta)
        self.thrust[1] = self.throttle*self.max_thrust*np.sin(phi)*np.sin(theta)
        self.thrust[2] = -self.throttle*self.max_thrust*np.cos(phi)
    
class rocket(part):
    I = np.zeros(3) # inertia vector
    CT = np.zeros(3) # center of thrust
    fuel_mass = 0
    
    def __init__(self):
        super().__init__(0, 0, 0)

    def calc_mass(self):
        for part in self.children:
            if isinstance(part, tank):
                self.fuel_mass += part.fuel_mass
            if isinstance(part, engine):
                self.engine_flow += part.flow
            self.mass += part.mass

    def get_Ct(self):
        for part in self.children:
            if isinstance(part, engine):
                self.CT += part.CG
    
    def get_Cl(self):
        for part in self.children:
            if isinstance(part, fin):
                self.CL += part.CG*part.area
    
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
    f1 = fin
    # rocket parts tree
    rocket_parts_tree = {
            e1:np.array([0, 0, 0]),
            c1:np.array([0, 0, 0]),
            t1:np.array([0, 0, e1.height]),
            c2:np.array([0, 0, c1.height]),
    }
    # rocket assembly
    R1 = rocket()
    R1.add_child(c1, (0, 0, 0))
    R1.add_child(c2, (0, 0, c1.height))
    R1.add_child(e1, (0, 0, 0))
    R1.add_child(t1, (0, 0, e1.height))
    for i in np.linspace(0, 2*np.pi, 3):
        ax, ay = np.cos(i), np.sin(i)
        R_matrix(i)
        R1.add_child(f1(1, 1, 0.5), (c1.diameter/2, 0, 0))
        R1.add_child(f1(1, 1, 0.5), (c1.diameter/2, 0, 0))
        R1.add_child(f1(1, 1, 0.5), (c1.diameter/2, 0, 0))
