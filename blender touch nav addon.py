bl_info = {
    "name": "Touch Navigation for 2D animation and tablets",
    "author": "Rekliner (github.com/rekliner)",
    "version": (1, 4, 5),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > TouchNav",
    "description": "So you'll need the keyboard less for quick 2d animation",
    "warning": "",
    "wiki_url": "https://github.com/rekliner/blenderTouchNav",
    "category": "3D View",
}
import bpy


class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "TouchNav"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)


# Roll Operators
class VIEW3D_OT_RollLeftViewTn(bpy.types.Operator):
    bl_idname = "opr.roll_left_view_tn"
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
    bl_idname = "opr.roll_right_view_tn"
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
        row.operator("opr.roll_left_view_tn", text="Left", icon="LOOP_BACK")
        row.operator("opr.roll_right_view_tn", text="Right", icon="LOOP_FORWARDS")
                
                
        ob = context.object
        gpd = ob.data
        gpl = False
        try:
            gpl = gpd.layers.active
        except:
            gpl = False
        

        row = layout.row()
        layer_rows = 7
        if gpl:
            col = row.column()
            col.template_list("GPENCIL_UL_layer", "", gpd, "layers", gpd.layers, "active_index",
                            rows=layer_rows, sort_reverse=True, sort_lock=True)

            col = row.column()
            sub = col.column(align=True)
            sub.operator("gpencil.layer_add", icon='ADD', text="")
            sub.operator("gpencil.layer_remove", icon='REMOVE', text="")

            sub.separator()

            sub.menu("GPENCIL_MT_layer_context_menu", icon='DOWNARROW_HLT', text="")

            if len(gpd.layers) > 1:
                col.separator()

                sub = col.column(align=True)
                sub.operator("gpencil.layer_move", icon='TRIA_UP', text="").type = 'UP'
                sub.operator("gpencil.layer_move", icon='TRIA_DOWN', text="").type = 'DOWN'

                col.separator()

                sub = col.column(align=True)
                sub.operator("gpencil.layer_isolate", icon='RESTRICT_VIEW_ON', text="").affect_visibility = True
                sub.operator("gpencil.layer_isolate", icon='LOCKED', text="").affect_visibility = False

        # Layer main properties
        row = layout.row()
        col = layout.column(align=True)

        if gpl:
            layout = self.layout
            layout.use_property_split = True
            layout.use_property_decorate = True
            col = layout.column(align=True)

            col = layout.row(align=True)
            col.prop(gpl, "blend_mode", text="Blend")

            col = layout.row(align=True)
            col.prop(gpl, "opacity", text="Opacity", slider=True)

            col = layout.row(align=True)
            col.prop(gpl, "use_lights")

        settings = context.tool_settings.gpencil_paint
        brush = settings.brush

        row = layout.row()
        large_preview = True
        if large_preview:
            row.column().template_ID_preview(settings, "brush", new="brush.add", rows=3, cols=8, hide_buttons=False)
        else:
            row.column().template_ID(settings, "brush", new="brush.add")
        col = row.column()
        col.menu("VIEW3D_MT_brush_context_menu", icon='DOWNARROW_HLT', text="")

        if brush is not None:
            col.prop(brush, "use_custom_icon", toggle=True, icon='FILE_IMAGE', text="")

            if brush.use_custom_icon:
                layout.prop(brush, "icon_filepath", text="")


        layout.template_ID(settings, "palette", new="palette.new")
        if settings.palette:
            layout.template_palette(settings, "palette", color=True)


        row = layout.row()
        col = row.column()
        col.prop(brush.gpencil_settings, "use_settings_stabilizer", text="Stabilize Stroke")
        row = layout.row()
        col = row.column()
        col.active = brush.gpencil_settings.use_settings_stabilizer
        col.prop(brush, "smooth_stroke_radius", text="Radius", slider=True)
        col.prop(brush, "smooth_stroke_factor", text="Factor", slider=True)

        if hasattr('gpd', 'onion_factor'):
            row = layout.row()
            col = row.column()
            col.prop(gpd, "onion_factor", text="Onion Skin", slider=True)





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