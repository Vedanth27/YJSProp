import yjsprop as yp
import matplotlib.pyplot as plt
import numpy as np

from yjsprop import Q_

tank_height = Q_(4, "ft")
OD = Q_(10, "in")
wt = Q_(0.125, "in")
ullage_frac = Q_(0.05, "")
prop_name = "Oxygen"
mode = "PressGas"
prop_T = Q_(-320, "degF")
ullage_P = Q_(450, "psi")
ullage_T = Q_(80, "degF")
ullage_name = "Helium"

# fluid changes
# need to add rocketprops to yjspprop to access RP1 and other stuff

OX_tank = yp.Tank(
    height=tank_height,
    OD=OD,
    wt=wt,
    ullage_frac=ullage_frac,
    prop_name=prop_name,
    mode=mode,
    prop_T=prop_T,
    ullage_P=ullage_P,
    ullage_T=ullage_T,
    ullage_name=ullage_name
)

dt = Q_(0.01, "second")
prop_mass_end = 0 # when to end the sim - when no prop mass left in tank
time = Q_(0, "second")
ambient = Q_(14.8, "psi")

CdA = Q_(3.43E-5, "m^2")

time_trace = np.array([])
prop_P_trace = np.array([])
mdot_trace = np.array([])
prop_T_trace = np.array([])
ullage_T_trace = np.array([])


while OX_tank.prop.mass.magnitude > prop_mass_end:
    # calc mdot
    # 
    mdot = yp.calc_incompressible_mdot(
        P_up=OX_tank.prop.P,
        P_down=ambient,
        CdA=CdA,
        density=OX_tank.prop.density
    )

    time_trace = np.append(time_trace, time.magnitude)
    prop_P_trace = np.append(prop_P_trace, OX_tank.prop.P.to("psi").magnitude)
    mdot_trace = np.append(mdot_trace, mdot.to("kg/s").magnitude)
    prop_T_trace = np.append(prop_T_trace, OX_tank.prop.T.to("degF").magnitude)
    ullage_T_trace = np.append(ullage_T_trace, OX_tank.ullage.T.to("psi").magnitude)

    dm = mdot * dt
    OX_tank.prop.dm(dm, "-", OX_tank.prop.density)

    time += dt

# Ullage Temperature
fig1 = plt.figure()
plt.plot(time_trace, ullage_T_trace)
plt.xlabel("Time (sec)")
ylabel = "Temperature (F)"
plt.ylabel(ylabel)
plt.title("COPV Blowdown Pressure")

# Propellant Pressure
fig1 = plt.figure()
plt.plot(time_trace, prop_P_trace)
plt.xlabel("Time (sec)")
ylabel = "Pressure (psia)"
plt.ylabel(ylabel)
plt.title("COPV Blowdown Pressure")

# Propellant Temperature
fig2 = plt.figure()
plt.plot(time_trace, prop_T_trace)
plt.xlabel("Time (sec)")
ylabel = "Temperature (F)"
plt.ylabel(ylabel)
plt.title("COPV Blowdown Temperature")

# Mdot
fig3 = plt.figure()
plt.plot(time_trace, mdot_trace)
plt.xlabel("Time (sec)")
ylabel = "Mdot (kg/s)"
plt.ylabel(ylabel)
plt.title("COPV Blowdown Mdot")

plt.show()