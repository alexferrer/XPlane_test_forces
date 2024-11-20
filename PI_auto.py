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

    pid_roll  = PID(2, 1  , 0.001)
    pid_pitch = PID(2, 1, 0.01)
    pid_speed = PID(.1, .01, 0.01)

    def __init__(self):

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
        self.WING_LEVEL = 0      #wings level angle 
        self.current_pitch = 0
        self.current_roll = 0
        self.new_roll = 0
        self.new_pitch = 0

        self.auto_pitch = True
        self.pitch_scale = 200
        self.pid_pitch.SetPoint = 1
        self.TARGET_PITCH_ANGLE = 1

        self.auto_speed = True
        self.speed_scale = 1
        self.pid_speed.SetPoint = 100
        self.current_speed = 0
        self.new_target_pitch = 0
        self.TARGET_SPEED = 100
        self.speed_count = 0

        self.auto_roll = True
        self.roll_scale = 850
        self.pid_roll.SetPoint=0.0





    def XPluginStart(self):
        self.Name = "Auto Speed"
        self.Sig = "AlexFerrer.Python.AutoSpeed"
        self.Desc = "Aautopilot plugin that keeps glider flight speed constant"

        # Define an XPlane command 
        # It may be called from a menu item, a key stroke, or a joystick button
        #self.commandRef = xp.createCommand('alexferrer/xplane/auto_speed', 'Engage auto speed control')
        #xp.registerCommandHandler(self.commandRef, self.CommandHandler)
        
        # ----- menu stuff --------------------------
        mySubMenuItem = xp.appendMenuItem(
            xp.findPluginsMenu(), "Auto Speed", 0, 1)
        self.MyMenuHandlerCB = self.MyMenuHandlerCallback
        self.myMenu = xp.createMenu("Auto Speed", xp.findPluginsMenu(), mySubMenuItem, self.MyMenuHandlerCB, 0)
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
            if self.speed_count > 100:
                #print("adjust speed")
                self.speed_count = 0    
                self.current_speed = xp.getDataf(self.airspeed) * 1.852
                self.pid_speed.update(self.current_speed)
                self.new_target_pitch = self.pid_speed.output * self.speed_scale

                self.pid_pitch.clear()
                self.TARGET_PITCH_ANGLE = self.new_target_pitch * -1
                self.pid_pitch.SetPoint = self.TARGET_PITCH_ANGLE

            self.speed_count += 1
    


        if self.auto_pitch:
            self.current_pitch = xp.getDataf(self.PlanePitch) 
            self.pid_pitch.update(self.current_pitch)
            self.new_pitch = self.pid_pitch.output  * self.pitch_scale * 1
            xp.setDataf(self.pitch_Dref, self.new_pitch )

        if self.auto_roll:
            self.current_roll = xp.getDataf(self.PlaneRol)
            self.pid_roll.update(self.current_roll)
            self.new_roll = self.pid_roll.output * self.roll_scale
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
        height = 550
        left_offset = 110
        top_offset = 410

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
        changed, self.TARGET_SPEED = imgui.slider_int("##Cruise Speed", self.TARGET_SPEED, 0, 300)
        if changed:
            self.pid_speed.clear()
            self.pid_speed.SetPoint=self.TARGET_SPEED

        imgui.text("Target speed: " + str(self.pid_speed.SetPoint) )
        imgui.text("Current speed: " + str(round(self.current_speed,3)) + " kph")
        imgui.text("Current Error: " + str(round(self.pid_speed.SetPoint-self.current_speed,3)) + " kph")
        imgui.text("New Pitch setpoint: " + str(round(self.new_target_pitch,3)) )
        imgui.text("")



        imgui.text("Current setpoint: " + str(self.pid_pitch.SetPoint) )
        imgui.text("Current pitch: " + str(round(self.current_pitch,3)) )
        imgui.text("Current Error: " + str(round(self.pid_pitch.SetPoint-self.current_pitch,3)))
        imgui.text("New Pitch: " + str(round(self.new_pitch,3)) + " deg")
        imgui.text("")



        #imgui.text("Wing Level")
        #imgui.text("Current Roll: " + str(round(self.current_roll,3)) + " degrees")
        #imgui.text("New Roll: " + str(round(self.new_roll,3)) + " degrees")
        #imgui.separator()
        #imgui.text("")


        imgui.separator()
        imgui.text("Disable all forces at once")
        changed, self.PLUGIN_ENABLED = imgui.checkbox("Test Mode on/off",self.PLUGIN_ENABLED)

        changed, self.auto_speed = imgui.checkbox("Auto Speed",self.auto_speed)
        if changed:
           self.pid_speed.clear()
           if self.auto_speed:
              self.pid_speed.SetPoint=self.TARGET_SPEED

        changed, self.auto_pitch = imgui.checkbox("Auto Pitch",self.auto_pitch)
        if changed:
           self.pid_pitch.clear()
           if self.auto_pitch:
              self.pid_pitch.SetPoint=self.TARGET_PITCH_ANGLE


        changed, self.auto_roll = imgui.checkbox("Auto Roll",self.auto_roll)
        if changed:
           self.pid_roll.clear()
           if self.auto_roll:
              self.pid_roll.SetPoint=0.0





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
        imgui.text("Pitch Scale")
        changed, self.pitch_scale = imgui.slider_int("##Pitchcale", self.pitch_scale, 1, 1000)

        imgui.separator()
        imgui.text("Roll Scale")
        changed, self.roll_scale = imgui.slider_int("##RollScale", self.roll_scale, 100, 1000)

        imgui.separator()
        imgui.text("Callback Time")
        changed, self.CALLBACKTIME = imgui.slider_int("##CallbackTime", self.CALLBACKTIME, 1, 1000)
