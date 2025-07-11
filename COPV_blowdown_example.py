import yjsprop as yp
import matplotlib.pyplot as plt
import numpy as np

from yjsprop import Q_

dt = Q_(0.01, "second")
time_end = 10 # s
time = Q_(0, "seconds")

gas_name = "Helium"
initial_P = Q_(5500, "psi")
initial_T = Q_(70, "degF")
initial_V = Q_(4071.5, "in^3")
CdA = Q_(0.0392, "in^2")
ambient=Q_(14.8, "psi")

output_unit = "psi"

tank = yp._0DGasNode(
    fluid_name=gas_name,
    P=initial_P,
    T=initial_T,
    volume=initial_V
)
    
time_trace = np.array([])
P_trace = np.array([])
mdot_trace = np.array([])
T_trace = np.array([])
    
while time.magnitude < time_end:

    mdot = yp.calc_compressible_mdot(
        gamma=tank.gamma,
        P_total=tank.P,
        T_total=tank.T,
        P_down=ambient,
        CdA=CdA,
        R=tank.R,
        density=tank.density
    )

    time_trace = np.append(time_trace, time.magnitude)
    P_trace = np.append(P_trace, tank.P.to(output_unit).magnitude)
    mdot_trace = np.append(mdot_trace, mdot.to("kg/s").magnitude)
    T_trace = np.append(T_trace, tank.T.to("degF").magnitude)

    dm = mdot * dt

    tank.dm(dm, "-")

    time += dt

# Pressure
fig1 = plt.figure()
plt.plot(time_trace, P_trace)
plt.xlabel("Time (sec)")
ylabel = "Pressure " + output_unit
plt.ylabel(ylabel)
plt.title("COPV Blowdown Pressure")

# Temperature
fig2 = plt.figure()
plt.plot(time_trace, T_trace)
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