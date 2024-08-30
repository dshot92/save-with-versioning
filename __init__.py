# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------------------
# Author: Daniele Stochino (dshot92)
# ----------------------------------------------------------

from . import (
    operators,
    panels
)


if "bpy" in locals():
    import importlib

    reloadable_modules = [
        "operators"
        "panels"
    ]

    for module in reloadable_modules:
        if module in locals():
            importlib.reload(locals()[module])


def register():
    operators.register()
    panels.register()


def unregister():
    panels.unregister()
    operators.unregister()
