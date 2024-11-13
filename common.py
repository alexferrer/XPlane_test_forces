''' 
  Auth: Alex Ferrer @ 2014
  Updated Oct 2024
'''
#-------------------------------------
# debug mode  0 = off , 1= stats, 2 = some, 3 = more, 4 = all 
DEBUG = 0
PLUGIN_ENABLED = True 
CALLBACKTIME = 1

#Sim time
sim_time=0
data_array = []

CALIBRATE_MODE = False  # set calibration mode on/off to generate fake thermal to adjust lift factor

calibrate_factor_ms = 1

# Thermal Config Window
CG_WINDOW_OPEN = True
CG_WINDOW = None
# Stats Window
STATS_WINDOW_OPEN = True
STATS_WINDOW = None
# About Window
ABOUT_WINDOW_OPEN = True
ABOUT_WINDOW = None

