# SPDX-License-Identifier: GPL-3.0-or-later

import bpy
from pathlib import Path
import os

from .utils import (
    increment_version,
    update_file_list,
    load_handler,
    open_current_dir,
)


# Operator class to save the blend file with Increased Versioning and Publish
class SWV_OT_SaveIncrement(bpy.types.Operator):
    bl_idname = "swv.save_increment"
    bl_label = "Save Increment"
    bl_description = "Save file and increment the version number"

    @ classmethod
    def poll(cls, context):
        # Check if file is saved
        return bpy.data.is_saved

    def execute(self, context):
        # Get the file path, name and directory
        filepath = Path(bpy.data.filepath)
        filename = filepath.stem
        directory = filepath.parent

        # Get the user-defined suffix from preferences
        prefs = context.preferences.addons[__package__].preferences
        version_suffix = prefs.version_suffix

        # Increment the version number in the filename
        filename, incremented_version = increment_version(
            filename, version_suffix)

        # Save the current with incremented version_suffix
        inc_path = f"{filename}{incremented_version}.blend"
        new_filepath = directory / inc_path
        bpy.ops.wm.save_as_mainfile(filepath=str(new_filepath))

        self.report({"INFO"}, f"Saved {inc_path}")

        # Refresh the file list
        update_file_list(context)

        return {"FINISHED"}


# Operator class to save the blend file with Increased Versioning and Publish
class SWV_OT_SavePublish(bpy.types.Operator):
    bl_idname = "swv.save_publish"
    bl_label = "Save Publish"
    bl_description = "Make copy of current file to published file"

    @ classmethod
    def poll(cls, context):
        # Check if file is saved
        return bpy.data.is_saved

    def execute(self, context):
        # Get the file path, name and directory
        filepath = Path(bpy.data.filepath)
        filename = filepath.stem
        directory = filepath.parent

        # Get the user-defined suffixes from preferences
        prefs = context.preferences.addons[__package__].preferences
        version_suffix = prefs.version_suffix
        publish_suffix = prefs.publish_suffix

        filename, incremented_version = increment_version(
            filename, version_suffix, increment=False)

        # Update the published file
        published_filepath = directory / f"{filename}{publish_suffix}.blend"
        bpy.ops.wm.save_as_mainfile(filepath=str(published_filepath))

        # Save the current with incremented version_suffix
        inc_path = f"{filename}{incremented_version}.blend"
        new_filepath = directory / inc_path
        bpy.ops.wm.save_as_mainfile(filepath=str(new_filepath))

        self.report({"INFO"}, f"Published {inc_path}")

        # Refresh the file list
        update_file_list(context)

        return {"FINISHED"}


class SWV_UL_FileList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            if item.indent == 0:
                row.label(text=item.name, icon='FILE_BLEND')
            else:
                row.label(text="- " + item.name, icon='FILE_BLEND')

            # Add a small button to open the file
            op = row.operator("swv.open_selected_file", text="",
                              icon='FILEBROWSER', emboss=True)
            op.filepath = item.name


class SWV_PG_FileItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    indent: bpy.props.IntProperty()


class SWV_OT_RefreshFileList(bpy.types.Operator):
    bl_idname = "swv.refresh_file_list"
    bl_label = "Refresh File List"
    bl_description = "Refresh the list of versioned files"

    def execute(self, context):
        update_file_list(context)
        return {'FINISHED'}


class SWV_OT_OpenSelectedFile(bpy.types.Operator):
    bl_idname = "swv.open_selected_file"
    bl_label = "Open Selected File"
    bl_description = "Open the selected file in the current Blender instance"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        directory = os.path.dirname(bpy.data.filepath)
        full_path = os.path.join(directory, self.filepath)

        if not os.path.exists(full_path):
            self.report({'ERROR'}, f"File not found: {full_path}")
            return {'CANCELLED'}

        bpy.ops.wm.open_mainfile(
            'INVOKE_DEFAULT',
            filepath=full_path,
            display_file_selector=False)

        return {'FINISHED'}


class SVM_OT_open_current_dir(bpy.types.Operator):
    bl_idname = "swv.open_current_dir"
    bl_label = "Open Current Directory"
    bl_description = "Open Current Directory"

    @classmethod
    def poll(cls, context):
        saved = bpy.context.blend_data.is_saved
        if not saved:
            cls.poll_message_set(
                "Blend file is not saved. Please save the file first.")
        return saved

    def execute(self, context):

        open_current_dir()

        return {'FINISHED'}


classes = (
    SWV_OT_SaveIncrement,
    SWV_OT_SavePublish,
    SWV_UL_FileList,
    SWV_PG_FileItem,
    SWV_OT_RefreshFileList,
    SWV_OT_OpenSelectedFile,
    SVM_OT_open_current_dir,
)


# Register the add-on
def register():
    for bl_class in classes:
        bpy.utils.register_class(bl_class)

    # Register file list properties
    bpy.types.Scene.file_list = bpy.props.CollectionProperty(
        type=SWV_PG_FileItem)
    bpy.types.Scene.file_list_index = bpy.props.IntProperty()

    # Add load handler
    bpy.app.handlers.load_post.append(load_handler)

    # Initial update of the file list
    bpy.app.timers.register(lambda: update_file_list(bpy.context))


# Unregister the add-on
def unregister():
    for bl_class in reversed(classes):
        bpy.utils.unregister_class(bl_class)

    # Remove load handler
    bpy.app.handlers.load_post.remove(load_handler)

    # Unregister file list properties
    del bpy.types.Scene.file_list
    del bpy.types.Scene.file_list_index
