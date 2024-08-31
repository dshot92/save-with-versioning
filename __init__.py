# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------------------
# Author: Daniele Stochino (dshot92)
# ----------------------------------------------------------

import bpy

from . import (
    operators,
    panels,
    utils
)


if "bpy" in locals():
    import importlib
    importlib.reload(operators)
    importlib.reload(panels)
    importlib.reload(utils)


def register():
    operators.register()
    panels.register()
    utils.register()


def unregister():
    utils.unregister()
    panels.unregister()
    operators.unregister()
