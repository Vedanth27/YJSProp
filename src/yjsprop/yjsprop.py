import numpy as np
import matplotlib.pyplot as plt
import pint
import math

from CoolProp.CoolProp import PropsSI
from rocketprops.rocket_prop import get_prop
from numpy.typing import NDArray

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity

universal_R = Q_(8.3145, "J/mol/K") # J/mol*K
pi = Q_(np.pi, "") # pi

class _0DGasNode:
    # need to add in how to deal with saturated mixtures
    # need to add in functionality to deal with real gases

    def __init__(self,
                 fluid_name : str,
                 P : Q_,
                 T : Q_,
                 mass : Q_ = None,
                 volume : Q_ = None
    ):
        self.fluid_name = fluid_name
        self.P = P
        self.T = T
        self.density = Q_(PropsSI("D", "P", self.P.to("Pa").magnitude, "T", self.T.to("kelvin").magnitude, self.fluid_name), "kg/m^3")
        self.Cp = PropsSI("C", "P", self.P.to("Pa").magnitude, "T", self.T.to("kelvin").magnitude, self.fluid_name)
        self.Cv = PropsSI("O", "P", self.P.to("Pa").magnitude, "T", self.T.to("kelvin").magnitude, self.fluid_name)
        self.gamma = Q_(self.Cp / self.Cv, "")
        self.M = Q_(PropsSI("M", "P", self.P.to("Pa").magnitude, "T", self.T.to("kelvin").magnitude, self.fluid_name), "kg/mol")
        self.R = universal_R / self.M
        # add all properties eventually like enthalpy, k, Cp, etc.

        if mass is not None:
            self.mass = mass
            self.volume = self.mass / self.density
        elif volume is not None:
            self.volume = volume
            self.mass = self.volume * self.density
        else:
            raise AttributeError("Mass or Volume must be specified.")
    
    def dm(self, mass, sign):
        if sign == "+":
            self.mass += mass
        elif sign == "-":
            self.mass -= mass
        else:
            raise ValueError("Invalid sign")
        
        self.update_props()

    def dQ(self, heat, sign):
        if sign == "+":
            self.energy += heat
        elif sign == "-":
            self.energy -= heat
        else:
            raise ValueError("Invalid sign")
        
    def dV(self, volume, sign): # is this needed???
        if sign == "+":
            self.volume += volume
        elif sign == "-":
            self.volume -= volume
        else:
            raise ValueError("Invalid sign")

        
    def update_props(self):
        self.rho_0 = self.density
        self.density = self.mass / self.volume
        self.rho_1 = self.density
        
       # self.Cp = PropsSI()
      #  self.Cv = PropsSI()

        self.gamma = self.Cp / self.Cv
        self.isentropic_expansion()  # isentropic expansion of gas

        # isentropic expansion
    
    def isentropic_expansion(self):
        self.P = self.P * (self.rho_1 / self.rho_0)**self.gamma

        T_unit = self.T.units
        self.T = Q_(PropsSI("T", "P", self.P.to("Pa").magnitude, "D", self.density.to("kg/m^3").magnitude, self.fluid_name), "kelvin").to(T_unit) 

def get_props(fluid_name):
    # take in fluid_name and compare to either RocketProps OR CoolProp
    # retreive all properties and return them
    # take in any 2 properties and output properties
    
    pass


class _0DLiquidNode:

    def __init__(self,
                 fluid_name : str,
                 P : Q_,
                 T : Q_,
                 mass : Q_ = None,
                 volume : Q_ = None
    ):
        self.fluid_name = fluid_name
        self.P = P
        self.T = T
        self.density = Q_(PropsSI("D", "P", self.P.to("Pa").magnitude, "T", self.T.to("kelvin").magnitude, self.fluid_name), "kg/m^3")

        # add all properties eventually like enthalpy, k, Cp, etc.

        if mass is not None:
            self.mass = mass
            self.volume = self.mass / self.density
        elif volume is not None:
            self.volume = volume
            self.mass = self.volume * self.density
        else:
            raise AttributeError("Mass or Volume must be specified.")
        
    def dm(self, mass, sign, density=None):
        if sign == "+":
            self.mass += mass
            if density is not None:
                self.volume += mass * density
        elif sign == "-":
            self.mass -= mass
            if density is not None:
                self.volume += mass * density
        else:
            raise ValueError("Invalid sign")

    def dQ(self, heat, sign):
        if sign == "+":
            self.energy += heat
        elif sign == "-":
            self.energy -= heat
        else:
            raise ValueError("Invalid sign")
    
    def update_props(self):
        self.density = self.mass / self.volume
        
       # self.Cp = PropsSI()
      #  self.Cv = PropsSI()


class Valve:

    def __init__(self,
                 CdA : pint,
                 opening_time : pint,
                 closing_time : pint,
                 CdA_swept : NDArray[np.float64],
                 K_fac : float,
                 state : int, # 0 = CLOSE and 1 = OPEN
    
    ):
        self.CdA = CdA

class ThrottlingValve:
    
    def __init__(self, 
                 CdA_swept
    ):
        self.CdA_swept = CdA_swept

class Orifice:
    '''
    Create an orifice. Either specify the CdA OR the diameter and a guessed Cd.
    '''
    def __init__(self,
                 CdA : pint = None,
                 diameter : float | int = None,
                 Cd_guess : float | int = 0.65,
    ): 
        if CdA is not None:
            self.CdA = CdA
        else:
            self.CdA = Cd_guess * np.pi * 0.25 * (diameter **2)

class Tank:
    '''
    Create Tank objects to be used for fluid states modeling and sizing. Uses Gas and Liquid Nodes.
    '''
    # also deal with head pressure
    def __init__(self,
                 height : Q_,
                 OD : Q_,
                 wt : Q_,
                 #geo : str,
                 ullage_frac : Q_,
                 prop_name : str,
                 mode : str = "Vapak",
                 prop_P : Q_ = None,
                 prop_T : Q_ = None,
                 ullage_P : Q_ = None,
                 ullage_T : Q_ = None,
                 mass : float | int = None,
                 tank_volume : Q_ = None,
                 ullage_name : str = None,
                 collapse_factor : Q_ = None

    ):

        self.height = height.to("in")
        self.OD = OD
        self. wt = wt
        #self.geo = geo # geo is either Flat Caps, Dome Caps, or Custom (custom volume entered)
        self.ullage_frac = ullage_frac
        self.prop_frac = 1 - ullage_frac

        if collapse_factor is not None:
            self.collapse_factor = collapse_factor

        if tank_volume is not None:
            self.tank_volume = tank_volume
        else:
            self.tank_volume = (OD - wt*2)**2 * np.pi * height

        match mode: # modes are either VaPak or PressGas
            case "Vapak":
                # Define EITHER Prop P or T, all properties calculated from here
                if (prop_P & prop_T) is None:
                    raise AttributeError("Prop P and T cannot both be defined in Vapak mode.")
                elif prop_P is not None:
                    # calculate properties with prop_P
                    self.prop_T = PropsSI("T", "P", prop_P.to("Pa").magnitude, "Q", 0, prop_name)
                    self.ullage_T = self.prop_T
                else:
                    self.prop_P = PropsSI("P", "T", prop_T.to("kelvin").magnitude, "Q", 0, prop_name)
                    self.ullage_P = self.prop_P
                
                self.ullage = _0DGasNode(prop_name, prop_P, prop_T, volume=self.ullage_frac * self.tank_volume)
                self.prop = _0DLiquidNode(prop_name, prop_P, prop_T, volume=self.prop_frac * self.tank_volume)
            
            case "PressGas": # add the Vapak things
                if ullage_P is None or ullage_T is None or prop_T is None:
                    raise AttributeError("Define Ullage P and T and Prop T")
                else:
                    self.ullage = _0DGasNode(ullage_name, ullage_P, ullage_T, volume=self.ullage_frac * self.tank_volume)
                    self.prop = _0DLiquidNode(prop_name, ullage_P, prop_T, volume=self.prop_frac * self.tank_volume)
            
            case _:
                raise AttributeError("Invalid tank operating mode. Choose either Vapak or PressGas.")
            
        self.tank_mass = self.ullage.mass + self.prop.mass
        self.prop_height = self.get_fluid_height(self.prop)
        self.ullage_height = self.get_fluid_height(self.ullage)
        self.prop_head_pressure = calc_head_pressure(self.prop.density, self.prop_height)
        self.ullage_head_pressure = calc_head_pressure(self.ullage.density, self.ullage_height)

    def update_props(self):

        self.tank_mass = self.prop_mass + self.ullage_mass
        self.ullage.update_props()
        self.prop.update_props()
        self.ullage.volume = self.tank_volume - self.prop.volume
        self.prop_head_pressure = calc_head_pressure(self.prop.density, self.prop_height)
        self.ullage_head_pressure = calc_head_pressure(self.ullage.density, self.ullage_height)
        self.prop.P = self.ullage.P

        # add in other stuff like total energy

    def get_fluid_height(self, fluid_type):
        fluid_height = (4 * fluid_type.volume) / (pi * (self.OD - 2*self.wt))

        return fluid_height
    
    def update_volume(self):
        self.prop.dV()



def calc_choke_ratio(gamma):
    choke_ratio = (2 / (gamma + 1)) ** (gamma/(gamma - 1))

    return choke_ratio

def calc_compressible_mdot(gamma, P_total, P_down, CdA, T_total, R, density):

    critical_ratio = calc_choke_ratio(gamma)
    choke_ratio = P_down.to("Pa").magnitude / P_total.to("Pa").magnitude
    
    if choke_ratio < critical_ratio:
        mdot = CdA.to("m^2") * P_total.to("Pa") * ((gamma / (R * T_total.to("kelvin")))**0.5) * (2/(gamma + 1))**((gamma + 1)/(2*(gamma - 1)))
        mdot = mdot.to_base_units()

        return mdot

    else:
        mdot = calc_compressible_mdot(P_total, P_down, CdA, density)

        return mdot
        # need to find equation for compressible mdot and update

def calc_incompressible_mdot(P_up, P_down, CdA, density):

    mdot = CdA.to("m^2") * (2 * density.to("kg/m^3") * (P_up.to("Pa") - P_down.to("Pa")))**0.5


def calc_head_pressure(density, height):
    gravity = Q_(9.81, "m/s^2")
    head_pressure = density.to("kg/m^3").magnitude * gravity * height.to("m").magnitude

    return head_pressure.to("psi")



