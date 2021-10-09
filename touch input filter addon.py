
import bpy, time
#from mathutils import Vector
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )


bl_info = {
    "name" : "Only allow pen input",
    "author" : "Rekliner",
    "version" : (0,4),
    "blender" : (2, 93, 0),
    "location": "View3D > Sidebar > TouchNav",
    "description" : "Blocks touchpad and mouse events when enabled",
    "warning" : "",
    "wiki_url" : "https://github.com/rekliner/blenderPenOnlyButton",
    "tracker_url" : "",
    "category" : "3D View"
}

last_pen_event = 0.0

class FilterPenInput(bpy.types.Operator):
    
    bl_idname = "opr.filter_pen_input"
    bl_label = "Filter Pen Input"
    bl_description = "Filter Pen Input"
    bl_options = {'REGISTER'}

    def modal(self, context, event):
        #global last_pen_event  #faster than property group?
        touchNav = context.scene.touchNav
        if event.is_tablet:
            #touchNav.last_pen_event = time.time()
            #last_pen_event = time.time()
            #print(touchNav.last_pen_event, event.type + " (" + str(event.mouse_x) + "," + str(event.mouse_y) + ")")
            return {'PASS_THROUGH'}  #this is still losing pen events if they come in too fast...blender just can't handle this
        if not touchNav.pen_only:
            return {'FINISHED'}

        if event.type != "TIMER" and event.type != "TIMER_REPORT":
            #touchNav.last_event = event.type + " (" + str(event.mouse_x) + "," + str(event.mouse_y) + ")" #" - " + event.value + " - " + str(event.is_tablet) + " - " + str(event.is_mouse_absolute)  + " - " + str(event.pressure) + " - "
            if event.type == "LEFTMOUSE" and context.area and context.area.type == "VIEW_3D" and context.region and context.region.type == "WINDOW" and self.mouse_in_view3d_window(context,event):
                #print(time.time() - touchNav.last_pen_event,time.time(),touchNav.last_pen_event,touchNav.pen_timeout)
                #if (event.type == "LEFTMOUSE") and ((time.time() - touchNav.last_pen_event < touchNav.pen_timeout) or (touchNav.pen_timeout > 600)):
                #if (event.type == "LEFTMOUSE"): # and ((time.time() - last_pen_event < touchNav.pen_timeout) or (touchNav.pen_timeout > 600)):
                    #touchNav.last_event = 'BLOCKED ' + touchNav.last_event  #force redraw of panel?
                    print('blocked', event.type + " (" + str(event.mouse_x) + "," + str(event.mouse_y) + ")")
                    return {'RUNNING_MODAL'}

                  
        return {'PASS_THROUGH'}


    def mouse_in_view3d_window(self, context, event):
        regions = dict()
        touchNav = context.scene.touchNav
        for region in bpy.context.area.regions:
            #print(event.mouse_x, event.mouse_y,region.type,region.width,region.height,region.x,region.y)
            regions[region.type] = region
        return (
            regions["TOOLS"].width < event.mouse_x < (regions["UI"].x if not touchNav.block_sidebar else regions["WINDOW"].width) and
            regions["WINDOW"].y < event.mouse_y < regions["HEADER"].y
        )


    def invoke(self, context, event):
        touchNav = context.scene.touchNav
        global last_pen_event

        if touchNav.pen_only is False:
            touchNav.pen_only = True
            #touchNav.
            last_pen_event = time.time()
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            touchNav.pen_only = False
            #context.window_manager.modal_handler_remove(self)
            return {'FINISHED'}



# 'N'Place a button in the menu that appears on the right side of VIEW 3D when you press a key
class OBJECT_PT_MKET(bpy.types.Panel):
    bl_label = "Input Mode"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "TouchNav"
    
    def draw(self, context):
        layout = self.layout
        touchNav = context.scene.touchNav
        if not touchNav.pen_only:
            layout.operator(FilterPenInput.bl_idname, text="Touch and Pen", icon="PLAY")
        else:
            layout.operator(FilterPenInput.bl_idname, text="Pen Only", icon="QUIT")
        layout.prop(touchNav, "block_sidebar", text="Block Sidebar")
        #layout.prop(touchNav, "pen_timeout", text="Re-enable timer")
        #layout.prop(touchNav, "last_event")
    
class TouchNavSettings(PropertyGroup):

    pen_only : BoolProperty(
        name="Touch Mode",
        description="Pen only or all inputs",
        default = False
        )

    block_sidebar : BoolProperty(
        name="Block Sidebar",
        description="Ignore the width taken up by the sidebar",
        default = False
        )

    pen_timeout : FloatProperty(
        name = "Pen timeout",
        description = "Seconds until touchscreen and mouse are re-enabled",
        default = 3.0,
        min = 0.01,
        max = 600.1
        )

    last_pen_event : FloatProperty(
        name = "Pen event",
        description = "Seconds from the epoch to the last pen event",
        default = 0.0,
        )

    last_event : StringProperty(name="Events",default="")

__classes__ = (
    FilterPenInput,OBJECT_PT_MKET,TouchNavSettings
)

def register():
    from bpy.utils import register_class
    for c in __classes__:
        register_class(c)

    bpy.types.Scene.touchNav = PointerProperty(type=TouchNavSettings)


def unregister():
    from bpy.utils import unregister_class
    for c in __classes__:
        unregister_class(c)


if __name__ == "__main__":
    register()