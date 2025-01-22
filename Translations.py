from UM.i18n import i18nCatalog

class CustomSupportsRebornTranslations:
    def __init__(self):
        self.catalog = i18nCatalog("customsupportsreborn", {
            "en": {
                "CustomSupportsReborn": {
                    "panel": {
                        "remove_all": "Remove All"
                    },
                    "supportTypes": {
                        "cylinder": "Cylinder",
                        "tube": "Tube",
                        "cube": "Cube",
                        "abutment": "Abutment",
                        "line": "Line",
                        "model": "Model"
                    },
                    "nodeNames": {
                        "cylinder": "CustomSupportCylinder"
                    }
                }
            }
        })
    
    def getTranslation(self, key):
        return self.catalog.i18n(key)