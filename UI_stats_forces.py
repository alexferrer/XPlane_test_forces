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
    height = 600
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

    imgui.separator()
    imgui.text("bargraph")
    #--------------------------
        # Draw bar graph
    values = [entry[7] for entry in common.data_array]
    labels = [entry[5] for entry in common.data_array]
    #imgui.plot_histogram("Forces", values, overlay_text=None, scale_min=0.0, scale_max=max(values), graph_size=(0, 80), stride=1)

    from array import array
    from random import random

    width = 44
    height = 200

    #------ values
    entry = common.data_array[2] #vert speed
    vlabel = "Vert Speed m/s"
    vspeed = entry[7]

    entry = common.data_array[7] #tot energy
    tlabel = "Tot Energy m/s"
    tspeed = entry[7] * 0.00508  # convert fpm to m/s

    entry = common.data_array[8]  #speed
    hlabel = "IAS kph" # entry[5]
    hspeed = entry[7] * 1.852 # convert to km/h

    imgui.columns(3, 'mixed')
    imgui.separator()
    imgui.text(vlabel)
    changed, values = imgui.v_slider_float(
        "vspeed",
        width, height, vspeed,
        min_value=-25, max_value=25,
        format="%0.3f", flags=imgui.SLIDER_FLAGS_NONE
    )

    imgui.next_column()
    imgui.text(tlabel)
    changed, values = imgui.v_slider_float(
        "##vslider2",
        width, height, tspeed,
        min_value=-20, max_value=20,
        format="%0.3f", flags=imgui.SLIDER_FLAGS_NONE
    )

    imgui.next_column()
    imgui.text(hlabel)
    changed, values = imgui.v_slider_float(
        "##vslider2",
        width, height, hspeed,
        min_value=0, max_value=300,
        format="%0.3f", flags=imgui.SLIDER_FLAGS_NONE
    )
