# SPDX-License-Identifier: GPL-3.0-or-later

import bpy
import os
import re
import platform
import subprocess

from enum import Enum

from pathlib import Path
from bpy.app.handlers import persistent


class OS(Enum):
    WINDOWS = "Windows"
    MACOS = "MacOS"
    LINUX = "Linux"
    UNKNOWN = "Unknown"

    @staticmethod
    def detect_os():
        if os.name == 'nt':
            return OS.WINDOWS
        elif os.name == 'posix' and platform.system() == "Darwin":
            return OS.MACOS
        elif os.name == 'posix' and platform.system() == "Linux":
            return OS.LINUX
        else:
            return OS.UNKNOWN


def get_blend_file() -> Path:
    blend_file = Path(bpy.data.filepath)
    return blend_file


def open_current_dir() -> None:

    path = get_blend_file().parent

    match OS.detect_os():
        case OS.WINDOWS:
            os.startfile(path)
        case OS.MACOS:
            subprocess.Popen(["open", path])
        case OS.LINUX:
            subprocess.Popen(["xdg-open", path])


def increment_version(filename, suffix, increment=True):
    # Extract base suffix and determine digit length
    base_suffix_match = re.search(r'\D*', suffix)
    base_suffix = base_suffix_match.group() if base_suffix_match else ''
    digit_match = re.search(r'\d+$', suffix)
    digit_len = len(digit_match.group()) if digit_match else 3

    # Generate regex pattern based on base suffix
    pattern = rf"^(.*?)((?:{re.escape(base_suffix)}\d+)+)$"
    match = re.match(pattern, filename)

    if match:
        name, version_part = match.groups()
        versions = re.findall(rf"{re.escape(base_suffix)}(\d+)", version_part)

        if increment:
            directory = Path(bpy.data.filepath).parent

            # Try incrementing the last version
            new_versions = versions[:-1] + \
                [f"{int(versions[-1]) + 1:0{digit_len}d}"]
            new_ver = ''.join(f"{base_suffix}{v}" for v in new_versions)
            new_filename = f"{name}{new_ver}"

            # Check if the incremented filename already exists
            if (directory / f"{new_filename}.blend").exists():
                # If it exists, create a new branch
                new_versions = versions + ["1".zfill(digit_len)]
                new_ver = ''.join(f"{base_suffix}{v}" for v in new_versions)

            # Ensure the new filename is unique
            while (directory / f"{name}{new_ver}.blend").exists():
                last_version = int(new_versions[-1])
                new_versions[-1] = f"{last_version + 1:0{digit_len}d}"
                new_ver = ''.join(f"{base_suffix}{v}" for v in new_versions)
        else:
            new_ver = version_part
    else:
        name = filename
        new_ver = suffix

    return name, new_ver


@persistent
def load_handler(dummy):
    bpy.app.timers.register(update_file_list_when_ready)


@persistent
def save_handler(dummy):
    bpy.app.timers.register(update_file_list_when_ready)


def update_file_list_when_ready():
    if bpy.context.scene is None:
        return 0.1  # Try again in 0.1 seconds
    update_file_list(bpy.context)
    return None  # Don't repeat the timer


def update_file_list(context):
    scene = context.scene
    scene.file_list.clear()

    if not bpy.data.is_saved:
        return

    current_file = bpy.path.basename(bpy.data.filepath)
    directory = os.path.dirname(bpy.data.filepath)

    prefs = context.preferences.addons[__package__].preferences
    base_suffix = re.search(r'\D*', prefs.version_suffix).group()
    # Get published suffix from preferences
    published_suffix = prefs.publish_suffix

    # Get the base name of the current file (without extension)
    current_base_name = os.path.splitext(current_file)[0]

    # Remove version suffix and published suffix if present
    current_base_name = re.split(
        rf'({re.escape(base_suffix)}\d+)+', current_base_name)[0]
    if current_base_name.endswith(published_suffix):
        current_base_name = current_base_name[:-len(published_suffix)]

    # Update the file filtering to include published files
    files = [f for f in os.listdir(directory) if f.endswith('.blend') and
             (f.startswith(current_base_name) and
              (f == current_base_name + '.blend' or
               re.match(rf'{re.escape(current_base_name)}({re.escape(base_suffix)}\d+)+({re.escape(published_suffix)})?\.blend', f) or
               f == current_base_name + published_suffix + '.blend'))]

    # Sort files and group them
    sorted_files = sorted(files)
    file_structure = {}

    for file in sorted_files:
        parts = re.findall(
            rf"({re.escape(base_suffix)}\d+|{re.escape(published_suffix)})", file)
        if parts:
            # Remove the published suffix from the key
            key = ''.join([part for part in parts if part != published_suffix])
            if key not in file_structure:
                file_structure[key] = []
            file_structure[key].append(file)
        else:
            file_structure[''] = file_structure.get('', []) + [file]

    # Add files to the list with proper indentation
    for key, files in file_structure.items():
        indent = key.count(base_suffix)
        for file in files:
            item = scene.file_list.add()
            item.name = file
            item.indent = indent

    # Select the current file in the list
    for index, item in enumerate(scene.file_list):
        if item.name == current_file:
            scene.file_list_index = index
            break

    # Trigger a redraw of the UI
    for area in context.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()


def register():
    bpy.app.handlers.load_post.append(load_handler)
    bpy.app.handlers.save_post.append(save_handler)


def unregister():
    bpy.app.handlers.load_post.remove(load_handler)
    bpy.app.handlers.save_post.remove(save_handler)
