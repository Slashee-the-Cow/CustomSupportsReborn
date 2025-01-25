# Reborn version copyright 2025 Slashee the Cow
# Copyright (c) 2022 5@xes
# Initialy Based on the SupportBlocker plugin by Ultimaker B.V., and licensed under LGPLv3 or higher.

from . import CustomSupportsReborn
from UM.i18n import i18nCatalog

i18n_catalog = i18nCatalog("customsupportsreborn")

def getMetaData():
    """Tell Cura all about CustomSupportsReborn"""
    return {
        "tool": {
            "name": i18n_catalog.i18nc("@tool:name", "Custom Supports Reborn"),
            "description": i18n_catalog.i18nc("@tool:tooltip", "Add several types of custom support"),
            "icon": "tool_icon.svg",
            "tool_panel": "qml/CustomSupportsReborn.qml",
            "weight": 8
        }
    }

def register(app):
    """Register tool so Cura can access it."""
    return { "tool": CustomSupportsReborn.CustomSupportsReborn() }
