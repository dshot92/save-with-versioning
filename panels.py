# SPDX-License-Identifier: GPL-3.0-or-later

import bpy

from .operators import (
    SWV_OT_SaveIncrement,
    SWV_OT_SavePublish
)


class SWV_UL_FileList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            text = " | " * item.indent + item.name
            row.label(text=text, icon='FILE_BLEND')

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
        filtered_indices = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item, items, "name", reverse=self.use_filter_sort_reverse)

        return filtered_indices, sorted_indices


class SWV_PG_FileItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    indent: bpy.props.IntProperty()


class SWV_PT_SaveWithVersioningPanel(bpy.types.Panel):
    bl_label = "Save with Versioning"
    bl_idname = "SWV_PT_SaveWithVersioningPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

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

    def draw(self, context):
        layout = self.layout
        layout.label(text="Set suffix")
        layout.prop(self, "version_suffix")
        layout.prop(self, "publish_suffix")


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


def register():
    for bl_class in classes:
        bpy.utils.register_class(bl_class)

    # Register file list properties
    bpy.types.Scene.file_list = bpy.props.CollectionProperty(
        type=SWV_PG_FileItem)
    bpy.types.Scene.file_list_index = bpy.props.IntProperty()

    bpy.types.VIEW3D_HT_header.append(save_versioning_button)


def unregister():
    for bl_class in reversed(classes):
        bpy.utils.unregister_class(bl_class)

    bpy.types.VIEW3D_HT_header.remove(save_versioning_button)

    # Unregister file list properties
    del bpy.types.Scene.file_list
    del bpy.types.Scene.file_list_index
