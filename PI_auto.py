"""
  XPlane Forces tester
  Author: Alex Ferrer
  License: GPL
"""
import math
import xp
from XPPython3.xp_typing import *
from XPPython3 import xp_imgui # type: ignore
import imgui  # type: ignore
from ivPID import PID 
# ------------------  T H E R M A L   S I M U L A T O R  ----------------------------

aboutWindow   = 1
activatePlugin = 2


class PythonInterface:      

    pid_speed = PID(1.2, 1, 0.001)
    pid_roll = PID(1.2, 1, 0.001)
    pid_roll.SetPoint=0.0

    def __init__(self):
        for _ in range(5):
            print()
        print("---------------------------------------------------------------- " )

        self.CGMenuItem = 0
        self.StatsWindowItem = 0
        self.AboutMenuItem = 0
        global myMenu      

        self.sim_time = 0
        self.DEBUG = 0
        self.CALLBACKTIME = 100   
        self.PLUGIN_ENABLED = True
        self.ABOUT_WINDOW_OPEN = True
        self.ABOUT_WINDOW = None
        self.CRUISE_SPEED = 100
        self.WING_LEVEL = 0      #wings level angle 
        self.current_airspeed = 0
        self.current_roll = 0
        self.s_scale = 1 # scale of correction
        self.r_scale = 1 # scale of correction
        self.new_roll = 0
        self.new_pitch = 0
        self.auto_roll = True
        self.auto_speed = True

    def XPluginStart(self):
        self.Name = "Auto Speed"
        self.Sig = "AlexFerrer.Python.AutoSpeed"
        self.Desc = "A plugin that keeps glider flight speed constant"

        # Define an XPlane command 
        # It may be called from a menu item, a key stroke, or a joystick button
        #self.commandRef = xp.createCommand('alexferrer/xplane/auto_speed', 'Engage auto speed control')
        #xp.registerCommandHandler(self.commandRef, self.CommandHandler)
        
        # ----- menu stuff --------------------------
        mySubMenuItem = xp.appendMenuItem(
            xp.findPluginsMenu(), "Auto Speed", 0, 1)
        self.MyMenuHandlerCB = self.MyMenuHandlerCallback
        self.myMenu = xp.createMenu("Auto Speed", xp.findPluginsMenu(), mySubMenuItem, self.MyMenuHandlerCB, 0)
        #xp.appendMenuItem(self.myMenu, "Configure Forces", configForces, 1)
        #xp.appendMenuItem(self.myMenu, "Activate Stats Window", statsWindow, 1)
        xp.appendMenuItem(self.myMenu, "About", aboutWindow, 1)
        xp.appendMenuItem(self.myMenu, "Activate Plugin", activatePlugin, 1)    
        # -------------------------------------------------
        self.PlaneHdg   = xp.findDataRef("sim/flightmodel/position/psi")  # plane heading
        self.PlaneRol   = xp.findDataRef("sim/flightmodel/position/phi")  # plane roll
        self.PlanePitch = xp.findDataRef("sim/flightmodel/position/theta")  # plane pitch

        self.lift_Dref = xp.findDataRef('sim/flightmodel/forces/fnrml_plug_acf')
        self.roll_Dref = xp.findDataRef('sim/flightmodel/forces/L_plug_acf')
        self.pitch_Dref = xp.findDataRef('sim/flightmodel/forces/M_plug_acf')
        self.thrust_Dref = xp.findDataRef('sim/flightmodel/forces/faxil_plug_acf')
        self.runningTime = xp.findDataRef("sim/time/total_running_time_sec")                                     
        self.runningTime = xp.findDataRef("sim/time/total_running_time_sec")   
        self.airspeed = xp.findDataRef("sim/flightmodel/position/indicated_airspeed")

        #----------------------------------------------
        self.create_About_Window()
        xp.registerFlightLoopCallback(self.FlightLoopCallback, 1.0, 0)
        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):    # Unregister the callbacks
        if self.DEBUG > 3 : print("Auto XPPluginStop")
        xp.unregisterFlightLoopCallback(self.FlightLoopCallback, 0)
        xp.destroyMenu(self.myMenu)

    def XPluginEnable(self):
           return 1

    def XPluginDisable(self):
        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        pass

    def FlightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):      
        # is the plugin enabled? , then skip
        if not self.PLUGIN_ENABLED:
            return 1
        
        # is the sim paused? , then skip
        runtime = xp.getDataf(self.runningTime)
        if self.sim_time == runtime:
            print("p ", end='')
            return 1
        self.sim_time = runtime

        
        if self.auto_speed:
            current_pitch = xp.getDataf(self.PlanePitch)
            self.current_airspeed = xp.getDataf(self.airspeed) * 1.852
            self.pid_speed.update(self.current_airspeed)
            self.new_pitch = self.pid_speed.output  *5
            xp.setDataf(self.pitch_Dref, self.new_pitch)
            #if self.DEBUG > 3 : print("newpitch = ",int(new_pitch) )

        if self.auto_roll:
            self.current_roll = xp.getDataf(self.PlaneRol)
            self.pid_roll.update(self.current_roll)
            self.new_roll = self.pid_roll.output*100
            xp.setDataf(self.roll_Dref, self.new_roll)

       

        return self.CALLBACKTIME/1000

    # --------------------------------------------------------------------------------------------------
    #                     UI &  M E N U   S T U F F
    # --------------------------------------------------------------------------------------------------

    def MyMenuHandlerCallback(self, inMenuRef, inItemRef):

        if (inItemRef == aboutWindow):
            if self.DEBUG > 2 : print("CGMenu : about window ") 
            if self.DEBUG > 2 : self.create_About_Window()
        
        if (inItemRef == activatePlugin):
            if self.DEBUG > 2 : print("CGMenu : activate plugin ") 
            self.PLUGIN_ENABLED = not self.PLUGIN_ENABLED
            if self.DEBUG > 2 : print("Plugin Enabled: ", self.PLUGIN_ENABLED)


    #-----------------------------------------------------------------
    def create_About_Window(self):
        self.ABOUT_WINDOW_OPEN = True
        title = 'About Xplane Forces'
        l, t, r, b = xp.getScreenBoundsGlobal()
        width = 400
        height = 450
        left_offset = 110
        top_offset = 810

        self.ABOUT_WINDOW = xp_imgui.Window(
            left=l + left_offset,
            top=t - top_offset,
            right=l + left_offset + width,
            bottom=t - (top_offset + height),
            visible=1,
            draw=self.draw_About_Window,
            refCon=self.ABOUT_WINDOW
        )
        self.ABOUT_WINDOW.setTitle(title)
        return

    def draw_About_Window(self, windowID, refCon):
        if not self.ABOUT_WINDOW_OPEN:
            return

        imgui.text("Auto Speed")
        imgui.text("Author: Alex Ferrer  @ 2014")
        imgui.text("")

        imgui.text("Cruise Speed")
        changed, self.CRUISE_SPEED = imgui.slider_int("##Cruise Speed", self.CRUISE_SPEED, 70, 250)
        if changed:
            self.pid_speed.SetPoint=self.CRUISE_SPEED
        imgui.text("Current Speed: " + str(round(self.current_airspeed,3)) + " kph")
        imgui.text("New Pitch: " + str(round(self.new_pitch,3)) + " deg")
        imgui.text("")


        imgui.text("Wing Level")
        imgui.text("Current Roll: " + str(round(self.current_roll,3)) + " degrees")
        imgui.text("New Roll: " + str(round(self.new_roll,3)) + " degrees")
        imgui.separator()
        imgui.text("")
        imgui.separator()
        imgui.text("Disable all forces at once")
        changed, self.PLUGIN_ENABLED = imgui.checkbox("Test Mode on/off",self.PLUGIN_ENABLED)
        changed, self.auto_speed = imgui.checkbox("Auto Speed",self.auto_speed)
        changed, self.auto_roll = imgui.checkbox("Auto Roll",self.auto_roll)

        imgui.separator()
        imgui.text("")
        # Debug Setting
        imgui.text("Debug Setting")
        imgui.same_line()
        imgui.text("Min")
        imgui.same_line()
        changed, self.DEBUG = imgui.slider_int("##DebugSetting", self.DEBUG, 0, 10)
        imgui.same_line()
        imgui.text("Max")
        if changed:
            print("Debug Setting", self.DEBUG)
        imgui.separator()
        imgui.text("Callback Time")
        changed, self.CALLBACKTIME = imgui.slider_int("##CallbackTime", self.CALLBACKTIME, 1, 1000)
