import os
from UM.i18n import i18nCatalog

translations = {
    "en_US": {
        "CustomSupportsReborn": {
                "supportTypes:cylinder": "cylinder",
                "supportTypes:tube": "tube",
                "supportTypes:cube": "cube",
                "supportTypes:abutment": "abutment",
                "supportTypes:line": "line",
                "supportTypes:model": "model",
                "panel:remove_all": "Remove All",
                "panel:remove_last": "Remove Last",
                "panel:size": "Size",
                "panel:max_size": "Max Size",
                "panel:model": "Model",
                "panel:inner_size": "Inner Size",
                "panel:angle": "Angle",
                "panel:set_on_y": "Set on Y direction",
                "panel:set_on_main": "Set on main direction",
                "panel:model_mirror": "Rotate 180°",
                "panel:model_auto_orientate": "Auto Orientation",
                "panel:model_scale_main": "Scaling in main directions",
                "panel:abutment_equalize_heights": "Equalize Heights",
                "supportTypeLabels:cylinder": "Cylinder",
                "supportTypeLabels:tube": "Tube",
                "supportTypeLabels:cube": "Cube",
                "supportTypeLabels:abutment": "Abutment",
                "supportTypeLabels:line": "Line",
                "supportTypeLabels:model": "Model",
                "nodeNames:cylinder": "CustomSupportCylinder",
                "nodeNames:tube": "CustomSupportTube",
                "nodeNames:cube": "CustomSupportCube",
                "nodeNames:abutment": "CustomSupportAbutment",
                "nodeNames:line": "CustomSupportLine",
                "nodeNames:model": "CustomSupportModel",
                "model_warning_dialog:start": "Had to change setting",
                "model_warning_dialog:middle": "to",
                "model_warning_dialog:end": "for calculation purposes. You may want to change it back to its previous value.",
                "model_warning_dialog:title": "WARNING: Custom Supports Reborn",
                "support_placement_warning:start": "Had to change setting",
                "support_placement_warning:middle": "to",
                "support_placement_warning:end": "for support to work.",
                "support_placement_warning:title": "WARNING: Custom Supports Reborn"
        }
    }
}

class CustomSupportsRebornTranslations:
    def __init__(self):
        
        localedir = os.path.join(os.path.dirname(__file__), "locale")
        self.catalog = i18nCatalog("customsupportsreborn", localedir = localedir)
    
    def getTranslation(self, key):
        return self.catalog.i18n(key)
