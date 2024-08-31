# SPDX-License-Identifier: GPL-3.0-or-later

import bpy
from bpy.app.handlers import persistent

from .operators import (
    SWV_OT_SaveIncrement,
    SWV_OT_SavePublish
)

def update_panel(self, context):
    # Unregister the panel
    try:
        bpy.utils.unregister_class(SWV_PT_SaveWithVersioningPanel)
    except:
        pass
    
    # Update the bl_category
    prefs = context.preferences.addons[__package__].preferences
    SWV_PT_SaveWithVersioningPanel.bl_category = prefs.panel_category
    
    # Re-register the panel
    bpy.utils.register_class(SWV_PT_SaveWithVersioningPanel)

    # Save the preference
    context.preferences.addons[__package__].preferences.panel_category = prefs.panel_category

class SWV_UL_FileList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            text = " | " * (item.indent - 1) + item.name
            row.label(text=text, icon='FILE_BLEND')

            # Add publish icon if the file is published
            if item.is_published:
                row.label(text="", icon='ANTIALIASED')

            # Add a small button to open the file
            op = row.operator("swv.open_selected_file", text="",
                              icon='FILEBROWSER', emboss=True)
            op.filepath = item.name

    def filter_items(self, context, data, propname):
        items = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        # Default sort
        sorted_indices = helper_funcs.sort_items_by_name(items, "name")

        # Filter
        filtered_indices = helper_funcs.filter_items_by_name(
            self.filter_name, self.bitflag_filter_item, items, "name",
            reverse=self.use_filter_sort_reverse)

        return filtered_indices, sorted_indices


class SWV_PG_FileItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    indent: bpy.props.IntProperty()
    is_published: bpy.props.BoolProperty()


class SWV_PT_SaveWithVersioningPanel(bpy.types.Panel):
    bl_label = "Save with Versioning"
    bl_idname = "SWV_PT_SaveWithVersioningPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'  # Default category

    @classmethod
    def poll(cls, context):
        prefs = context.preferences.addons[__package__].preferences
        if hasattr(prefs, "panel_category"):
            cls.bl_category = prefs.panel_category
        else:
            cls.bl_category = "Tool"
        return True

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Add save buttons
        row = layout.row()
        row.operator("swv.save_increment", text="Increment", icon="PLUS")
        row.operator("swv.save_publish", text="Publish", icon="ANTIALIASED")

        # Add refresh button
        row = layout.row()

        # Open current directory button
        row.operator("swv.open_current_dir",
                     text="Open Current Directory", icon="FILE_FOLDER")

        row.operator("swv.refresh_file_list", text="", icon="FILE_REFRESH")

        # Add file list
        row = layout.row()
        row.template_list("SWV_UL_FileList", "", scene,
                          "file_list", scene, "file_list_index", rows=10)


class SWV_PT_VersioningAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    version_suffix: bpy.props.StringProperty(
        name="version_suffix",
        description="Suffix for the versioning",
        default="_v001"
    )

    publish_suffix: bpy.props.StringProperty(
        name="publish suffix",
        description="Suffix for the published file",
        default="_published"
    )

    panel_category: bpy.props.EnumProperty(
        name="Panel Category",
        description="Choose the category for the Save with Versioning panel",
        items=[
            ('Tool', "Tool", "Place panel in the Tool category"),
            ('Item', "Item", "Place panel in the Item category"),
        ],
        default='Tool',
        update=update_panel
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Set suffix")
        layout.prop(self, "version_suffix")
        layout.prop(self, "publish_suffix")
        layout.prop(self, "panel_category")


# Function to add the "Save With Versioning" button to the header
def save_versioning_button(self, context):
    self.layout.operator(
        SWV_OT_SaveIncrement.bl_idname,
        text="",
        icon="PLUS"
    )
    self.layout.operator(
        SWV_OT_SavePublish.bl_idname,
        text="",
        icon="ANTIALIASED"
    )


classes = (
    SWV_UL_FileList,
    SWV_PG_FileItem,
    SWV_PT_SaveWithVersioningPanel,
    SWV_PT_VersioningAddonPreferences,
)


@persistent
def load_handler(dummy):
    # Update panel category on file load
    bpy.app.timers.register(lambda: update_panel(None, bpy.context))

def register():
    for bl_class in classes:
        bpy.utils.register_class(bl_class)

    # Register file list properties
    bpy.types.Scene.file_list = bpy.props.CollectionProperty(
        type=SWV_PG_FileItem)
    bpy.types.Scene.file_list_index = bpy.props.IntProperty()

    bpy.types.VIEW3D_HT_header.append(save_versioning_button)

    bpy.app.handlers.load_post.append(load_handler)

    # Load saved preferences
    addon_prefs = bpy.context.preferences.addons[__package__].preferences
    if addon_prefs:
        update_panel(addon_prefs, bpy.context)

def unregister():
    for bl_class in reversed(classes):
        bpy.utils.unregister_class(bl_class)

    bpy.types.VIEW3D_HT_header.remove(save_versioning_button)

    # Unregister file list properties
    del bpy.types.Scene.file_list
    del bpy.types.Scene.file_list_index

    bpy.app.handlers.load_post.remove(load_handler)


def update_panel(self, context):
    # Unregister the panel
    try:
        bpy.utils.unregister_class(SWV_PT_SaveWithVersioningPanel)
    except:
        pass
    
    # Update the bl_category
    prefs = context.preferences.addons[__package__].preferences
    SWV_PT_SaveWithVersioningPanel.bl_category = prefs.panel_category
    
    # Re-register the panel
    bpy.utils.register_class(SWV_PT_SaveWithVersioningPanel)

    # Save the preference
    context.preferences.addons[__package__].preferences.panel_category = prefs.panel_category
