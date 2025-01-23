from UM.i18n import i18nCatalog

class CustomSupportsRebornTranslations:
    def __init__(self):
        self.catalog = i18nCatalog("customsupportsreborn", {
            "en": {
                "CustomSupportsReborn": {
                    "supportTypes": {
                        "cylinder": "cylinder",
                        "tube": "tube",
                        "cube": "cube",
                        "abutment": "abutment",
                        "line": "line",
                        "model": "model"
                    },
                    "panel": {
                        "remove_all": "Remove All",
                        "remove_last": "Remove Last",
                        "size": "Size",
                        "max_size": "Max Size",
                        "model": "Model",
                        "inner_size": "Inner Size",
                        "angle": "Angle",
                        "set_on_y": "Set on Y direction",
                        "set_on_main": "Set on main direction",
                        "model_mirror": "Rotate 180°",
                        "model_auto_orientate": "Auto Orientation",
                        "model_scale_main": "Scaling in main directions",
                        "abutment_equalize_heights": "Equalize Heights"
                    },
                    "supportTypeLabels": {
                        "cylinder": "Cylinder",
                        "tube": "Tube",
                        "cube": "Cube",
                        "abutment": "Abutment",
                        "line": "Line",
                        "model": "Model"
                    },
                    "nodeNames": {
                        "cylinder": "CustomSupportCylinder",
                        "tube": "CustomSupportTube",
                        "cube": "CustomSupportCube",
                        "abutment": "CustomSupportAbutment",
                        "line": "CustomSupportLine",
                        "model": "CustomSupportModel"
                    },
                    "model_warning_dialog": {
                        "start": "Had to change setting",
                        "middle": "to",
                        "end": "for calculation purposes. You may want to change it back to its previous value.",
                        "title": "WARNING: Custom Supports Reborn"
                    },
                    "support_placement_warning": {
                        "start": "Had to change setting",
                        "middle": "to",
                        "end": "for support to work.",
                        "title": "WARNING: Custom Supports Reborn"
                    }
                }
            }
        })
    
    def getTranslation(self, key):
        return self.catalog.i18n(key)