import common
import xp
import imgui # type: ignore
from XPPython3 import xp_imgui # type: ignore

def create_About_Window(self):
    common.ABOUT_WINDOW_OPEN = True
    title = 'About Xplane Forces'
    l, t, r, b = xp.getScreenBoundsGlobal()
    width = 400
    height = 300
    left_offset = 110
    top_offset = 110

    common.ABOUT_WINDOW = xp_imgui.Window(
        left=l + left_offset,
        top=t - top_offset,
        right=l + left_offset + width,
        bottom=t - (top_offset + height),
        visible=1,
        draw=self.draw_About_Window,
        refCon=common.ABOUT_WINDOW
    )
    common.ABOUT_WINDOW.setTitle(title)
    return

def draw_About_Window(self, windowID, refCon):
    if not common.ABOUT_WINDOW_OPEN:
        return

    imgui.text("Test XPlane forces via dataref on a plane")
    imgui.text("Author: Alex Ferrer  @ 2014")
    imgui.text("https://github.com/alexferrer/xplane_forces/wiki")

    imgui.text("")

    # Debug Setting
    imgui.text("Debug Setting")
    imgui.same_line()
    imgui.text("Min")
    imgui.same_line()
    changed, common.DEBUG = imgui.slider_int("##DebugSetting", common.DEBUG, 0, 10)
    imgui.same_line()
    imgui.text("Max")
    if changed:
        print("Debug Setting", common.DEBUG)
