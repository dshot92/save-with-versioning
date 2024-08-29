# SPDX-License-Identifier: GPL-3.0-or-later

import bpy
import re
from pathlib import Path
import os


# Add-on preferences class
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


def increment_version(filename, suffix, increment=True):
    # Extract base suffix and determine digit length
    base_suffix_match = re.search(r'\D*', suffix)
    base_suffix = base_suffix_match.group() if base_suffix_match else ''
    digit_match = re.search(r'\d+$', suffix)
    digit_len = len(digit_match.group()) if digit_match else 3
    # Generate regex pattern based on base suffix
    pattern = rf"^(.*)({re.escape(base_suffix)})(\d+)(_\d+)?$"
    match = re.match(pattern, filename)
    if match:
        name, _, version_str, subversion = match.groups()
        ver = int(version_str)
        if increment:
            directory = Path(bpy.data.filepath).parent
            existing_files = list(directory.glob(f"{name}{base_suffix}*"))
            version_pattern = rf"{re.escape(base_suffix)}(\d+)(_\d+)?"
            versions = [
                (int(m.group(1)), int(m.group(2)[1:]) if m.group(2) else 0)
                for f in existing_files
                if (m := re.search(version_pattern, f.stem))
            ]
            max_ver, max_subver = max(versions) if versions else (ver, 0)
            if ver < max_ver:
                new_subver = 1
                while (ver, new_subver) in versions:
                    new_subver += 1
                new_ver = f"{base_suffix}{ver:0{digit_len}d}_{new_subver:03d}"
            else:
                new_ver = f"{base_suffix}{ver + 1:0{digit_len}d}"
        else:
            new_ver = f"{base_suffix}{ver:0{digit_len}d}"
            if subversion:
                new_ver += subversion
        new_filename = name
    else:
        new_filename = filename
        new_ver = suffix
    return new_filename, new_ver


# Operator class to save the blend file with Increased Versioning and Publish
class SWV_OT_SaveIncrementOperator(bpy.types.Operator):
    bl_idname = "wm.save_increment_publish"
    bl_label = "Save Increment Publish"
    bl_description = "Save file and increment the version number"

    @classmethod
    def poll(cls, context):
        # Check if file is saved
        return bpy.data.is_saved

    def execute(self, context):
        # Get the file path, name and directory
        filepath = Path(bpy.data.filepath)
        filename = filepath.stem
        directory = filepath.parent

        # Get the user-defined suffix from preferences
        prefs = context.preferences.addons[__name__].preferences
        version_suffix = prefs.version_suffix

        # Increment the version number in the filename
        filename, incremented_version = increment_version(
            filename, version_suffix)

        # Save the current with incremented version_suffix
        inc_path = f"{filename}{incremented_version}.blend"
        new_filepath = directory / inc_path
        bpy.ops.wm.save_as_mainfile(filepath=str(new_filepath))

        self.report({"INFO"}, f"Saved {inc_path}")

        return {"FINISHED"}


# Operator class to save the blend file with Increased Versioning and Publish
class SWV_OT_SavePublishOperator(bpy.types.Operator):
    bl_idname = "wm.save_publish"
    bl_label = "Save Publish"
    bl_description = "Make copy of current file to published file"

    @classmethod
    def poll(cls, context):
        # Check if file is saved
        return bpy.data.is_saved

    def execute(self, context):
        # Get the file path, name and directory
        filepath = Path(bpy.data.filepath)
        filename = filepath.stem
        directory = filepath.parent

        # Get the user-defined suffixes from preferences
        prefs = context.preferences.addons[__name__].preferences
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

        return {"FINISHED"}


class SWV_UL_FileList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon='FILE_BLEND')


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
        row.operator(SWV_OT_SaveIncrementOperator.bl_idname, text="Save Increment", icon="PLUS")
        row.operator(SWV_OT_SavePublishOperator.bl_idname, text="Save Publish", icon="ANTIALIASED")

        # Add file list
        layout.template_list("SWV_UL_FileList", "", scene, "file_list", scene, "file_list_index")

        # Add refresh button
        layout.operator(SWV_OT_RefreshFileList.bl_idname, text="Refresh File List", icon="FILE_REFRESH")


# New operator to refresh the file list
class SWV_OT_RefreshFileList(bpy.types.Operator):
    bl_idname = "swv.refresh_file_list"
    bl_label = "Refresh File List"
    bl_description = "Refresh the list of versioned files"

    def execute(self, context):
        update_file_list(context)
        return {'FINISHED'}


def update_file_list(context):
    scene = context.scene
    scene.file_list.clear()

    if not bpy.data.is_saved:
        return

    directory = os.path.dirname(bpy.data.filepath)
    files = [f for f in os.listdir(directory) if f.endswith('.blend')]
    
    # Sort files and group them
    sorted_files = sorted(files)
    file_structure = {}

    for file in sorted_files:
        parts = os.path.splitext(file)[0].rsplit('_v', 1)
        if len(parts) == 2:
            base, version = parts
            if '_' in version:
                main_version, sub_version = version.split('_')
                if f"{base}_v{main_version}" not in file_structure:
                    file_structure[f"{base}_v{main_version}"] = []
                file_structure[f"{base}_v{main_version}"].append(file)
            else:
                file_structure[file] = []
        else:
            file_structure[file] = []

    # Add files to the list with proper indentation
    for main_file, sub_files in file_structure.items():
        item = scene.file_list.add()
        item.name = main_file + '.blend'
        item.indent = 0

        for sub_file in sub_files:
            sub_item = scene.file_list.add()
            sub_item.name = sub_file
            sub_item.indent = 1

# Function to add the "Save With Versioning" button to the header
def save_versioning_button(self, context):
    self.layout.operator(
        SWV_OT_SaveIncrementOperator.bl_idname, text="", icon="PLUS")
    self.layout.operator(SWV_OT_SavePublishOperator.bl_idname,
                         text="", icon="ANTIALIASED")

classes = (
    SWV_PT_VersioningAddonPreferences,
    SWV_OT_SaveIncrementOperator,
    SWV_OT_SavePublishOperator,
    SWV_UL_FileList,
    SWV_PG_FileItem,
    SWV_PT_SaveWithVersioningPanel,
    SWV_OT_RefreshFileList,  # Add this new class
)


# Register the add-on
def register():
    for bl_class in classes:
        bpy.utils.register_class(bl_class)

    # Register file list properties
    bpy.types.Scene.file_list = bpy.props.CollectionProperty(type=SWV_PG_FileItem)
    bpy.types.Scene.file_list_index = bpy.props.IntProperty()

    bpy.types.VIEW3D_HT_header.append(save_versioning_button)

    # Initial update of the file list
    bpy.app.timers.register(lambda: update_file_list(bpy.context))


# Unregister the add-on
def unregister():
    for bl_class in reversed(classes):
        bpy.utils.unregister_class(bl_class)

    bpy.types.VIEW3D_HT_header.remove(save_versioning_button)

    # Unregister file list properties
    del bpy.types.Scene.file_list
    del bpy.types.Scene.file_list_index

