bl_info = {
    "name": "Touch Navigation for 2D animation and tablets",
    "author": "Rekliner (github.com/rekliner)",
    "version": (1, 3, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > Tool Tab",
    "description": "So you'll need the keyboard less for quick 2d animation",
    "warning": "",
    "wiki_url": "https://github.com/rekliner/blenderTouchNav",
    "category": "3D View",
}
import bpy


class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)


# Roll Operators
class VIEW3D_OT_RollLeftViewTn(bpy.types.Operator):
    bl_idname = "opr.roll_left_view1"
    bl_label = "Roll Left View"
    bl_description = "Roll the view Left"

    def execute(self, context):
        if context.space_data.region_3d.view_perspective == 'CAMERA':
            spacedata = bpy.context.space_data
            spacedata.show_object_viewport_camera = False
            bpy.ops.view3d.view_axis(type='FRONT')
        bpy.ops.view3d.view_roll(angle=-0.261799)
        return {'FINISHED'}


class VIEW3D_OT_RollRightViewTn(bpy.types.Operator):
    bl_idname = "opr.roll_right_view1"
    bl_label = "Roll Right View"
    bl_description = "Roll the view Right"

    def execute(self, context):
        #if bpy.ops.view3d.view_camera.poll()
        if context.space_data.region_3d.view_perspective == 'CAMERA':
            spacedata = bpy.context.space_data
            spacedata.show_object_viewport_camera = False
            bpy.ops.view3d.view_axis(type='FRONT')
        bpy.ops.view3d.view_roll(angle=0.261799)
        return {'FINISHED'}


class TouchNav(View3DPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_touch_nav"
    bl_label = "Touchscreen Buttons"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("ED_OT_undo", text="Undo")
        row = layout.row()
        row.label(text="Rotate View")
        row = layout.row()
        row.operator("opr.roll_left_view1", text="Left", icon="LOOP_BACK")
        row.operator("opr.roll_right_view1", text="Right", icon="LOOP_FORWARDS")

classes = (
    TouchNav,
    VIEW3D_OT_RollLeftViewTn,
    VIEW3D_OT_RollRightViewTn,
    )


# Register
def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()