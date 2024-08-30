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


@persistent
def load_handler(dummy):
    bpy.app.timers.register(update_file_list_when_ready)


def update_file_list_when_ready():
    if bpy.context.scene is None:
        return 10  # Try again in 10 seconds
    update_file_list(bpy.context)
    return None  # Don't repeat the timer


def update_file_list(context):
    scene = context.scene
    scene.file_list.clear()

    if not bpy.data.is_saved:
        return

    current_file = bpy.path.basename(bpy.data.filepath)
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
                main_file = f"{base}_v{main_version}.blend"
                if main_file not in file_structure:
                    file_structure[main_file] = []
                file_structure[main_file].append(file)
            else:
                file_structure[file] = []
        else:
            file_structure[file] = []

    # Add files to the list with proper indentation
    for main_file, sub_files in file_structure.items():
        item = scene.file_list.add()
        item.name = main_file
        item.indent = 0

        for sub_file in sub_files:
            sub_item = scene.file_list.add()
            sub_item.name = sub_file
            sub_item.indent = 1

    # Select the current file in the list
    for index, item in enumerate(scene.file_list):
        if item.name == current_file:
            scene.file_list_index = index
            break

    # Trigger a redraw of the UI
    for area in context.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()
