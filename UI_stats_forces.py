import xp
import imgui # type: ignore
from XPPython3 import xp_imgui # type: ignore
import common

def create_Stats_Window(self):
    common.STATS_WINDOW_OPEN = True
    title = 'Forces Stats'
    if common.DEBUG > 1: print("Creating Stats Window")
    
    l, t, r, b = xp.getScreenBoundsGlobal()
    width = 450
    height = 300
    left_offset = 810
    top_offset = 210

    common.STATS_WINDOW = xp_imgui.Window(
        left=l + left_offset,
        top=t - top_offset,
        right=l + left_offset + width,
        bottom=t - (top_offset + height),
        visible=1,
        draw=self.draw_Stats_Window,
        refCon=common.STATS_WINDOW
    )
    common.STATS_WINDOW.setTitle(title)
    return

def draw_Stats_Window(self, windowID, refCon):
    if not common.STATS_WINDOW_OPEN:
        return
 
    imgui.text(f"callback time: {common.CALLBACKTIME} milliseconds")
    imgui.text(f"calibrate factor: {common.calibrate_factor_ms} m/s")
    imgui.separator()

    #common.data_array
    for entry in common.data_array:
        imgui.text( f"{entry[5]} >  { round( entry[7],2)}" )


    