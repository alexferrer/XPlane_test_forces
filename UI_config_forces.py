import common
import xp
import imgui #type: ignore
from XPPython3 import xp_imgui # type: ignore

def create_CG_Window(self):
    common.CG_WINDOW_OPEN = True
    title = 'Configure Forces'
    if common.DEBUG > 1:
        print("Creating CG Window")
    
    l, t, r, b = xp.getScreenBoundsGlobal()
    width = 600
    height = 500
    left_offset = 110
    top_offset = 310

    common.CG_WINDOW = xp_imgui.Window(
        left=l + left_offset,
        top=t - top_offset,
        right=l + left_offset + width,
        bottom=t - (top_offset + height),
        visible=1,
        draw=self.draw_CG_Window,
        refCon=common.CG_WINDOW
    )
    common.CG_WINDOW.setTitle(title)
    return

def draw_CG_Window(self, windowID, refCon):
    if not common.CG_WINDOW_OPEN:
        common.CALIBRATE_MODE = False
        return
    
    imgui.text("Test the effect of forces on the aircract ")
    imgui.text("Adjust the forces, select on/off and see the effect on the aircraft")
    imgui.separator()
    imgui.text("Set value multiplier for all forces")
    changed, common.calibrate_factor_ms = imgui.slider_int("Test Factor" , common.calibrate_factor_ms , 0, 100) 
    imgui.text("Set the flightloop callback time for the simulator")
    changed, common.CALLBACKTIME = imgui.slider_int("Callback time msecs", common.CALLBACKTIME, 1, 1000)
    imgui.text("")
    imgui.text("Disable all forces at once")
    changed, common.CALIBRATE_MODE = imgui.checkbox("Test Mode on/off",common.CALIBRATE_MODE)
    imgui.separator()
    

    imgui.columns(2, 'test_factors')
    i = 0
    for entry in common.data_array:
        i += 1
        # [9] how much to change the dataref by
        # [3] minimum value
        # [4] maximum value
        imgui.text(f"{entry[3]}")
        imgui.same_line()
        changed, entry[9] = imgui.slider_int(f"##{i}", entry[9], int(entry[3]), int(entry[4]))
        imgui.same_line()
        imgui.text(f"{entry[4]}")
        imgui.next_column()
        changed, entry[8] = imgui.checkbox(entry[5], entry[8])
        imgui.next_column()
    imgui.columns(1)

    imgui.separator()
    for _ in range(7):
        imgui.text("")

    imgui.text("You may configure datarefs.csv to add other datarefs to test")

    return