import numpy as np

from numpy.typing import NDArray

# Data Analysis Tools
# 1. Duty cycle calculator
# 2. Calculate C* Efficiency - options to set a rolling window, throat expanded C* eff
# 3. LTTB Downsampling
# 4. Savgol Filtering
# 5. Cumulative and Instantaneous Isp
# 6. Collapse Factor - multiple methods
# 7. MR
# 8. Incompressible CdA
# 9. Compressible CdA
# 10. Injector Stiffness
# 11. Valve Timings


def calc_duty_cycle(
    window_time : str,
    data : NDArray[np.float64],
        
) -> NDArray[np.float64]:
    '''
    Calculate the rolling duty cycle for a signal.

    Args:

    Returns:

    '''

def calc_cstar_eff(
    
) -> NDArray[np.float64]:
    '''
    Calcualte the C* Efficiency of an Engine. Options for Throat Expanded C* Eff, and for Data Sampling
    '''

def downsample(
    datapoints : int,
    data : NDArray[np.float64]
) -> NDArray[np.float64]:
    '''
    Reduce the number of datapoints with Least-Triangle-Three-Buckets (LTTB).
    '''

def savgol_filter(
        
) -> NDArray[np.float64]:
    '''
    Use a Savitzky-Golay Filter to smooth the data.
    '''

    pass

def Isp(
    thrust : NDArray[np.float64],
    mdot : NDArray[np.float64],
    mode : str

) -> NDArray[np.float64]:
    '''
    Get the Cumulative or Instantaneous Isp of the Engine
    '''

    pass

def calc_collapse_factor(
    
) -> NDArray[np.float64]:
    '''
    Calculate the collapse factor of the pressurant gas. Three methods:
    1) Instantaneous Collapse Factor -> Ideal vs. Real Gas Mdot
    2) Cumulative Collapse Factor -> Ideal Total Gas Mass vs. Real Total Gas Mass into Tank
    3) 

    '''
    pass

def calc_MR(
    ox_mdot : NDArray[np.float64],
    fu_mdot : NDArray[np.float64],
) -> NDArray[np.float64]:
    '''
    Calculate the MR (Oxidizer to Fuel Ratio) by dividing OX Mdot / FU Mdot.

    '''
    pass

def calc_incompressible_CdA(
        
) -> NDArray[np.float64]:
    '''
    Calculate the incompressible CdA. Output a least-squared fit value or timeseries.
    '''

    pass

def calc_compressible_CdA(
        
) ->  NDArray[np.float64]:
    
    '''
    Calculate the compressible CdA. Output a least-squared fit value or timeseries.
    '''

    pass

def calc_inj_stiffness(
    P_up :  NDArray[np.float64],
    Pc : NDArray[np.float64],
        
) -> NDArray[np.float64]:
    '''
    Calculate injector stiffness timeseries.
    '''

    DP = P_up - Pc
    stiffness = DP / Pc
    
    return stiffness

def calc_valve_timings(
        
) -> NDArray[np.float64]:
    '''
    Calculate the valve OPEN/CLOSE time. 
    '''