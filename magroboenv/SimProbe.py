import math
import random
import numpy as np
import logging
import magroboenv.myconfig as myconfig
# from training_data.data_reader import DataReader
from DataGen import Bfield
import sys

##########global class and function definition#############

def square(x):
    return x*x

# calculate and return the distance unit2 
# needs to move to reach unit1
def angular_distance(unit1, unit2):
    phi = abs(unit2-unit1) % 360
    sign = 1
    # used to calculate sign
    if not ((unit1-unit2 >= 0 and unit1-unit2 <= 180) or (
            unit1-unit2 <= -180 and unit1-unit2 >= -360)):
        sign = -1
    if phi > 180:
        result = 360-phi
    else:
        result = phi
    return result*sign

#class representing the coordinates
class Coordinate():
    
    def __init__(self):
        self.x=0.0
        self.y=0.0
        self.z=0.0
        
    def set_coordinate(self, Coordinate):
        self.x=Coordinate.x
        self.y=Coordinate.y
        self.z=Coordinate.z

    def get_coordinate(self):
        return [self.x, self.y, self.z]
        
    def set_xyz(self, x, y, z):
        self.x=x
        self.y=y
        self.z=z
        
    def set_x(self, x):
        self.x=x
        
    def set_y(self, y):
        self.y=y

    def set_z(self, z):
        self.z=z
     
    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)

    def find_distance(self, Coordinate):
        sum = square(self.x - Coordinate.x) + square(self.y - Coordinate.y) + square(self.z - Coordinate.z)
        return math.sqrt(sum)

    def set_random_xyz(self):
        self.x = random.uniform(myconfig.Config.X_MAX_VAL, myconfig.Config.X_MIN_VAL)
        self.y = random.uniform(myconfig.Config.Y_MAX_VAL, myconfig.Config.Y_MIN_VAL)
        self.z = random.uniform(myconfig.Config.Z_MAX_VAL, myconfig.Config.Z_MIN_VAL)
        xyz = [ self.x, self.y, self.z ]
        return xyz

    def set_random_dev_xyz(self, Coordinate):
        self.x = random.uniform(Coordinate.x - myconfig.Config.X_MAX_DEVIATE, Coordinate.x + myconfig.Config.X_MAX_DEVIATE)
        self.y = random.uniform(Coordinate.y - myconfig.Config.Y_MAX_DEVIATE, Coordinate.y + myconfig.Config.Y_MAX_DEVIATE)
        self.z = random.uniform(Coordinate.z - myconfig.Config.Z_MAX_DEVIATE, Coordinate.z + myconfig.Config.Z_MAX_DEVIATE)
        xyz = [ self.x, self.y, self.z ]
        return xyz
        
#class representing the coordinates
class MagneticMoment():
    
    def __init__(self):
        self.mx=0.0
        self.my=0.0
        self.mz=0.0
        
    def set_mmoment(self, MagneticMoment):
        self.mx=MagneticMoment.mx
        self.my=MagneticMoment.my
        self.mz=MagneticMoment.mz
    
    def get_mmoment(self):
        return [self.mx, self.my, self.mz]
        
    def set_xyz(self, x, y, z):
        self.mx=x
        self.my=y
        self.mz=z
        
    def set_mx(self, x):
        self.mx=x
        
    def set_my(self, y):
        self.my=y

    def set_mz(self, z):
        self.mz=z
     
    def __str__(self):
        return "({}, {}, {})".format(self.mx, self.my, self.mz)

    def find_distance(self, MagneticMoment):
        # sum = square(self.mx - MagneticMoment.mx) + square(self.my - MagneticMoment.my) + square(self.mz - MagneticMoment.mz)
        # return math.sqrt(sum)
        return self.find_distance_xyz(MagneticMoment.mx, MagneticMoment.my, MagneticMoment.mz)

    def find_distance_xyz(self,x,y,z):
        # sum = square(self.mx - x) + square(self.my - y) + square(self.mz - z)
        sum = square(angular_distance(self.mx, x)) + square(angular_distance(self.my, y)) + square(angular_distance(self.mz, z))
        return math.sqrt(sum)
    
    def set_random_xyz(self):
        self.mx = random.uniform(myconfig.Config.X_MAX_MAG_MOMENT, myconfig.Config.X_MIN_MAG_MOMENT)
        self.my = random.uniform(myconfig.Config.Y_MAX_MAG_MOMENT, myconfig.Config.Y_MIN_MAG_MOMENT)
        self.mz = random.uniform(myconfig.Config.Z_MAX_MAG_MOMENT, myconfig.Config.Z_MIN_MAG_MOMENT)
        xyz = [ self.mx, self.my, self.mz ]
        return xyz

    def set_random_dev_xyz(self, MagneticMoment):
        self.mx = random.uniform(MagneticMoment.mx - myconfig.Config.X_MAX_MAG_MOMENT_DEVIATE, MagneticMoment.mx + myconfig.Config.X_MAX_MAG_MOMENT_DEVIATE)
        self.my = random.uniform(MagneticMoment.my - myconfig.Config.Y_MAX_MAG_MOMENT_DEVIATE, MagneticMoment.my + myconfig.Config.Y_MAX_MAG_MOMENT_DEVIATE)
        self.mz = random.uniform(MagneticMoment.mz - myconfig.Config.Z_MAX_MAG_MOMENT_DEVIATE, MagneticMoment.mz + myconfig.Config.Z_MAX_MAG_MOMENT_DEVIATE)
        xyz = [ self.mx, self.my, self.mz ]
        return xyz

#Electric Current class
class Current():
    
    ac_low = np.array([myconfig.Config.MIN_CURRENT, myconfig.Config.MIN_CURRENT, myconfig.Config.MIN_CURRENT, myconfig.Config.MIN_CURRENT, myconfig.Config.MIN_CURRENT, myconfig.Config.MIN_CURRENT, myconfig.Config.MIN_CURRENT, myconfig.Config.MIN_CURRENT, myconfig.Config.MIN_CURRENT])
    ac_high = np.array([myconfig.Config.MAX_CURRENT, myconfig.Config.MAX_CURRENT, myconfig.Config.MAX_CURRENT, myconfig.Config.MAX_CURRENT, myconfig.Config.MAX_CURRENT, myconfig.Config.MAX_CURRENT, myconfig.Config.MAX_CURRENT, myconfig.Config.MAX_CURRENT, myconfig.Config.MAX_CURRENT])

    deviate_action_low = np.array([-2, -2, -2, -2, -2, -2, -2, -2, -2])
    deviate_action_high = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1])
    
    def __init__(self, name='unknown'):
        self.amp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.name = name
		
    def __str__(self):
        return "({}, {})".format(self.name, self.amp)

    # def uniform_current(self, curr):
    #     while True:
    #         dev = random.uniform(myconfig.Config.MAX_DEVIATE, myconfig.Config.MIN_DEVIATE)
    #         dev = curr + dev
    #         if dev < myconfig.Config.MAX_CURRENT and dev > myconfig.Config.MIN_CURRENT:
    #             return dev
            
    def generate_random(self):
        for i in range(9):
            #self.amp[i] = self.uniform_current(self.amp[i])
            self.amp[i] = random.uniform(myconfig.Config.MAX_CURRENT, myconfig.Config.MIN_CURRENT)
        #print("random:{}".format(self))
	
    def set_current(self, a1, a2, a3, a4, a5, a6, a7, a8, a9):
        self.amp[0] = a1
        self.amp[1] = a2
        self.amp[2] = a3
        self.amp[3] = a4
        self.amp[4] = a5
        self.amp[5] = a6
        self.amp[6] = a7
        self.amp[7] = a8
        self.amp[8] = a9
        #print(self)

    def set_sys_current(self, index, cur):
        if cur < myconfig.Config.MAX_CURRENT and cur > myconfig.Config.MIN_CURRENT:
            self.amp[index] = cur
            # VI.setcontrolvalue(myconfig.Config.AMP_LABEL[index], str(self.amp[index]))

    def set_all_sys_current(self, cur):
        for i in range(9):
            self.amp[i] = cur[i]

    def set_all_sys_curr_deviate(self, curr):
        for i in range(9):
            dev = 0
            if int(round(curr[i])) == 0:
                #perform no change
                continue
            elif int(round(curr[i])) == 1:
                #increment the curr
                dev = myconfig.Config.MAX_CURR_DEVIATE
            else:
                #decrement the curr
                dev = myconfig.Config.MIN_CURR_DEVIATE
            
            self.amp[i] += dev
            
            if self.amp[i] > myconfig.Config.MAX_CURRENT:
                self.amp[i] = myconfig.Config.MAX_CURRENT
            elif  self.amp[i] <  myconfig.Config.MIN_CURRENT:
                self.amp[i] = myconfig.Config.MIN_CURRENT

            # VI.setcontrolvalue(myconfig.Config.AMP_LABEL[i], str(self.amp[i]))

         
    def read_sys_current(self):
        return self.amp

        
    def get_a1(self):
        return self.amp[0]

    def get_a2(self):
        return self.amp[1]

    def get_a3(self):
        return self.amp[2]
    
    def get_a4(self):
        return self.amp[3]

    def get_a5(self):
        return self.amp[4]

    def get_a6(self):
        return self.amp[5]

    def get_a7(self):
        return self.amp[6]

    def get_a8(self):
        return self.amp[7]

    def get_a9(self):
        return self.amp[8]

#class representing the probing robot 
class MProbe():

    # ob_low  = np.array([myconfig.Config.X_MIN_VAL, myconfig.Config.Y_MIN_VAL, myconfig.Config.Z_MIN_VAL, myconfig.Config.X_MIN_MAG_MOMENT, myconfig.Config.Y_MIN_MAG_MOMENT, myconfig.Config.Z_MIN_MAG_MOMENT,
    #     myconfig.Config.X_MIN_VAL, myconfig.Config.Y_MIN_VAL, myconfig.Config.Z_MIN_VAL, myconfig.Config.X_MIN_MAG_MOMENT, myconfig.Config.Y_MIN_MAG_MOMENT, myconfig.Config.Z_MIN_MAG_MOMENT])
    # ob_high = np.array([myconfig.Config.X_MAX_VAL, myconfig.Config.Y_MAX_VAL, myconfig.Config.Z_MAX_VAL, myconfig.Config.X_MAX_MAG_MOMENT, myconfig.Config.Y_MAX_MAG_MOMENT, myconfig.Config.Z_MAX_MAG_MOMENT,
    #     myconfig.Config.X_MAX_VAL, myconfig.Config.Y_MAX_VAL, myconfig.Config.Z_MAX_VAL, myconfig.Config.X_MAX_MAG_MOMENT, myconfig.Config.Y_MAX_MAG_MOMENT, myconfig.Config.Z_MAX_MAG_MOMENT])

    ob_low  = np.array([myconfig.Config.X_MIN_VAL, myconfig.Config.Y_MIN_VAL, myconfig.Config.Z_MIN_VAL, myconfig.Config.X_MIN_MAG_MOMENT, myconfig.Config.Y_MIN_MAG_MOMENT, myconfig.Config.Z_MIN_MAG_MOMENT])
    ob_high = np.array([myconfig.Config.X_MAX_VAL, myconfig.Config.Y_MAX_VAL, myconfig.Config.Z_MAX_VAL, myconfig.Config.X_MAX_MAG_MOMENT, myconfig.Config.Y_MAX_MAG_MOMENT, myconfig.Config.Z_MAX_MAG_MOMENT])

    def __init__(self, name='unknown'):
        self.coordinate = Coordinate()
        self.last_coordinate = Coordinate()
        self.last_coordinate_dist = 0.0
        self.mmoment = MagneticMoment()
        self.last_mmoment = MagneticMoment()
        self.velocity = 0.0
        self.name = name

        self.config = [0.0 for _ in range(6)]
        self.refresh()

    def __str__(self):
        return "({}, {}, {})".format(self.name, self.coordinate, self.mmoment)

    def refresh(self):
        self.last_config = self.config
        if myconfig.Config.CURR_DEVIATE_ACTIVE:
            self.set_random_dev_xyz()
        else:
            self.set_random_xyz()
            
        self.config = self.coordinate.get_coordinate() + self.mmoment.get_mmoment()
        assert (len(self.config) == 6)

    def set_coordinate(self, Coordinate):
        self.last_coordinate.set_coordinate(self.coordinate)
        self.coordinate.set_coordinate(Coordinate)
        self.last_coordinate_dist = self.coordinate.find_distance(self.last_coordinate)

    def set_x(self, x):
        self.last_coordinate.set_x(self.coordinate.x)
        self.coordinate.set_x(float(x))
        self.last_coordinate_dist = self.coordinate.find_distance(self.last_coordinate)
        # print(self)

    def set_y(self, y):
        self.last_coordinate.set_y(self.coordinate.y)
        self.coordinate.set_y(float(y))
        self.last_coordinate_dist = self.coordinate.find_distance(self.last_coordinate)
        # print(self)

    def set_z(self, z):
        self.last_coordinate.set_z(self.coordinate.z)
        self.coordinate.set_z(float(z))
        self.last_coordinate_dist = self.coordinate.find_distance(self.last_coordinate)
        # print(self)

    def set_orientation(self, mx, my, mz):
        self.last_mmoment.set_mmoment(self.mmoment)
        self.mmoment.set_xyz(mx, my, mz)
        #print(self)
        logging.debug(self)
        
    def read_sys_configuration(self):
        
        # if self.name == 'Slave':
        #     ori = DR.get_data()
        # elif self.name == 'Master':
        #     ori = DR.get_data()
        # else:
        #     sys.exit("Type not found: {}".format(self.name))

        # self.set_orientation(ori[0], ori[1], ori[2], ori[3], ori[4], ori[5])

        # return ori

        pos = self.coordinate.get_coordinate()
        ori = self.mmoment.get_mmoment()

        self.config = [pos[0], pos[1], pos[2], ori[0], ori[1], ori[2]]
        return self.config

        
    def set_random_xyz(self):
        # if myconfig.Config.TRAINING_MODE == "MOMENT":
        #     xyz = self.mmoment.set_random_xyz()
        # elif myconfig.Config.TRAINING_MODE == "COORD":
        #     xyz = self.coordinate.set_random_xyz()
        # else:
        #     xyz = self.coordinate.set_random_xyz()
        #     xyz1 = self.mmoment.set_random_xyz()
        xyz = self.coordinate.set_random_xyz()
        xyz1 = self.mmoment.set_random_xyz()
        print("Target: {}".format(self))
        logging.debug("Target: {}".format(self))
        return self
    
    def set_random_dev_xyz(self, MProbe):
        # if myconfig.Config.TRAINING_MODE == "MOMENT":
        #     xyz = self.mmoment.set_random_dev_xyz(MProbe.mmoment)
        # elif myconfig.Config.TRAINING_MODE == "COORD":
        #     xyz = self.coordinate.set_random_dev_xyz(MProbe.coordinate)
        # else:
        #     xyz = self.mmoment.set_random_dev_xyz(MProbe.mmoment)
        #     xyz1 = self.coordinate.set_random_dev_xyz(MProbe.coordinate)

        xyz = self.mmoment.set_random_dev_xyz(MProbe.mmoment)
        xyz1 = self.coordinate.set_random_dev_xyz(MProbe.coordinate)
        print("Target: {}".format(self))
        logging.debug("Target: {}".format(self))
        return self        
        
    def find_distance(self, MProbe):
        dist = self.coordinate.find_distance(MProbe.coordinate)
        return dist

    def find_moment_distance(self, MProbe):
        dist = self.mmoment.find_distance(MProbe.mmoment)
        return dist

    def find_moment_distance_xyz(self, x,y,z):
        dist = self.mmoment.find_distance_xyz(x,y,z)
        return dist

    def find_last_moment_distance(self, MProbe):
        dist = self.last_mmoment.find_distance(MProbe)
        return dist

    def find_last_moment_distance_xyz(self, x,y,z):
        dist = self.last_mmoment.find_distance_xyz(x,y,z)
        return dist

    def get_last_moment(self):
        return self.last_mmoment
    
    def get_last_config(self):
        return self.last_config

    def get_config(self):
        return self.config

    def simulate_currents(self, curr):
        pos = self.get_config()
        pos = [ [pos[0]], [pos[1]], [pos[2]] ]
        ori = Bfield.getOri(pos, curr)

        self.set_orientation(ori[0], ori[1], ori[2])
        self.read_sys_configuration()
        return ori


#---------------------------------

# master=MProbe('Master')
slave=MProbe('Slave')
goal=MProbe('Goal')
# read_current=Current('reading')
desired_current=Current('desired')

