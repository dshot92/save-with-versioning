# SPDX-License-Identifier: GPL-3.0-or-later

import bpy
import re
from pathlib import Path


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


# Function to increment version numbers
def increment_version(filename, suffix, increment=True):
    # Extract the base suffix without digits and
    # determine digit length if any digits exist
    base_suffix_match = re.search(r'\D*', suffix)
    base_suffix = base_suffix_match.group() if base_suffix_match else ''
    digit_match = re.search(r'\d+$', suffix)
    # Default to 3 if no digits found
    digit_length = len(digit_match.group()) if digit_match else 3

    # Generate regex pattern based on base suffix
    pattern = rf"^(.*)({re.escape(base_suffix)})(\d+)$"
    match = re.match(pattern, filename)

    if match:
        # If the filename has a version number,
        # extract the name and version number
        name = match.group(1)
        version = int(match.group(3))

        # Increment number only if increment = true
        new_version = version + 1 if increment else version

        new_filename = name
        new_version = f"{base_suffix}{new_version:0{digit_length}d}"
    else:
        # If the filename does not have a version number,
        # use the provided suffix
        new_filename = filename
        new_version = suffix

    return new_filename, new_version


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

        self.report({"INFO"}, f"Saved {inc_path}.blend")

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

        self.report({"INFO"}, f"Published {inc_path}.blend")

        return {"FINISHED"}


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
)


# Register the add-on
def register():
    for bl_class in classes:
        bpy.utils.register_class(bl_class)

    # Add button right of Viewport Render Modes
    bpy.types.VIEW3D_HT_header.append(save_versioning_button)


# Unregister the add-on
def unregister():
    for bl_class in classes:
        bpy.utils.unregister_class(bl_class)

    # Remove button right of Viewport Render Modes
    bpy.types.VIEW3D_HT_header.remove(save_versioning_button)
