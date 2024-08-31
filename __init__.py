# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------------------
# Author: Daniele Stochino (dshot92)
# ----------------------------------------------------------


import importlib

from . import operators, panels, utils

modules = (
    operators,
    panels,
    utils,
)

if "bpy" in locals():
    importlib.reload(operators)
    importlib.reload(panels)
    importlib.reload(utils)


def register():
    for module in modules:
        importlib.reload(module)
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()
