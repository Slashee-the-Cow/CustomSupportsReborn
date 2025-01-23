import polib
from Translations import translations

po = polib.POFile()

for lang, data in translations.items():
    for plugin_name, translations_data in data.items():
        for key, value in translations_data.items():
            entry = polib.POEntry(
                msgid=key,
                msgstr="",  # Leave msgstr empty for now
            )
            po.append(entry)

po.save("customsupportsreborn.pot")