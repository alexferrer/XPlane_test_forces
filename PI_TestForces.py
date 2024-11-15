"""
  XPlane Forces tester
  Author: Alex Ferrer
  License: GPL
"""

import common
# thermal modeling tools
import math
import xp
from XPPython3.xp_typing import *
from XPPython3 import xp_imgui # type: ignore
import imgui  # type: ignore
import csv

#########################################################

# ------------------  T H E R M A L   S I M U L A T O R  ----------------------------

configForces   = 1
statsWindow    = 2
aboutForces   = 3
activatePlugin = 4

class PythonInterface:
    
    def read_csv_to_array(self,file_path):
        data = []
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data.append(row)
        return data
    
    def __init__(self):
        for _ in range(5):
            print()
        print("---------------------------------------------------------------- " )

        self.CGMenuItem = 0
        self.StatsWindowItem = 0
        self.AboutMenuItem = 0
        global myMenu      
        file_path = 'Resources/plugins/PythonPlugins/datarefs.csv'
        common.data_array = self.read_csv_to_array(file_path)[1:] #skip 1st line.. its the header



    def XPluginStart(self):
        self.Name = "TestForces"
        self.Sig = "AlexFerrer.Python.TestForces"
        self.Desc = "A plugin that reads and injects forces via dataref"

        # ----- menu stuff --------------------------
        mySubMenuItem = xp.appendMenuItem(
            xp.findPluginsMenu(), "Test Forces Tool", 0, 1)
        self.MyMenuHandlerCB = self.MyMenuHandlerCallback
        self.myMenu = xp.createMenu("Test Forces", xp.findPluginsMenu(), mySubMenuItem, self.MyMenuHandlerCB, 0)
        xp.appendMenuItem(self.myMenu, "Configure Forces", configForces, 1)
        xp.appendMenuItem(self.myMenu, "Activate Stats Window", statsWindow, 1)
        
        # -------------------------------------------------
        #          0          1       2      3      4        5           6                7          8            9
        # [dataref string  | type | scale | Low | High | description | dref pointer| Dref value | checkbox | change amount]
        if common.DEBUG > 1: print("Loading datarefs")
        for entry in common.data_array:
            if common.DEBUG > 1: print("> ",entry) 
            entry.append(xp.findDataRef(entry[0]))  # [6]  dataref pointer
            entry.append(xp.getDataf(entry[6]))     # [7]  current Dref value
            entry.append(False)                     # [8]  checkbox on/off
            entry.append(0)                         # [9]  amount to change dataref by
        #----------------------------------------------

        self.create_CG_Window()
        self.create_Stats_Window()

        self.runningTime = xp.findDataRef("sim/time/total_running_time_sec")   
        xp.registerFlightLoopCallback(self.FlightLoopCallback, 1.0, 0)
        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):    # Unregister the callbacks
        if common.DEBUG > 3 : print("XPPluginStop")
        xp.unregisterFlightLoopCallback(self.FlightLoopCallback, 0)
        xp.destroyMenu(self.myMenu)

    def XPluginEnable(self):
           return 1

    def XPluginDisable(self):
        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        pass

    def FlightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):
        # the actual callback, runs once every x period as defined
        
        # is the sim paused? , then skip
        runtime = xp.getDataf(self.runningTime)
        if common.sim_time == runtime:
            print("P ", end='')
            return 1
        common.sim_time = runtime
      
        METERS_PER_SECOND_TO_NEWTON = 10 # 1m/s = 1000N
        if common.CALIBRATE_MODE:
           for entry in common.data_array:
                label = entry[5]
                scale = float(entry[2])  # get scale factor
                amount = entry[9]  # get amount to change dataref by
                dataref = entry[6]
                curr_value = xp.getDataf(dataref)
                if entry[8]: #if checked on box
                     if common.DEBUG > 3 : print(f"label: {label}, Current Value: {curr_value}, Amount: {amount}, Scale: {scale}")
                     xp.setDataf(dataref, curr_value + (amount * scale * common.calibrate_factor_ms  ))  

                entry[7] = xp.getDataf(dataref)
        return common.CALLBACKTIME/1000

    # --------------------------------------------------------------------------------------------------
    #                     UI &  M E N U   S T U F F
    # --------------------------------------------------------------------------------------------------

    # About Window
    from UI_aboutForces import create_About_Window, draw_About_Window 
    # Stats window
    from UI_stats_forces import create_Stats_Window, draw_Stats_Window
    # Configure Glider 
    from UI_config_forces import create_CG_Window, draw_CG_Window

    def MyMenuHandlerCallback(self, inMenuRef, inItemRef):

        if (inItemRef == statsWindow):
            self.create_Stats_Window()

        if (inItemRef == configForces):
            if common.DEBUG > 2 : print("CGMenu : activate window ") 
            self.create_CG_Window()

        if (inItemRef == aboutForces):
            if common.DEBUG > 2 : print("CGMenu : about window ") 
            self.create_About_Window()

