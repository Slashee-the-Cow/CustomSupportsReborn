import re
import os

def extract_strings(filepath, outfile):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return

    pattern = r"(?<!#)\s*catalog\.i18nc\(\"(.+?)\",\s*\"(.+?)\"\)"
    matches = re.findall(pattern, content)

    for context, message_id in matches:
        outfile.write(f'#: {filepath}\n')
        outfile.write(f'msgctxt "{context}"\n') # Add msgctxt
        outfile.write(f'msgid "{message_id}"\n')
        outfile.write(f'msgstr ""\n')
        outfile.write('\n')
        outfile.write('\n')

def find_python_files(root_dir):
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)

if __name__ == "__main__":
    plugin_root = "."
    with open("resources/i18n/customsupportsreborn.pot", "w", encoding="utf-8") as outfile:
        outfile.write('msgid ""\n')
        outfile.write('msgstr ""\n')
        outfile.write('"Project-Id-Version: PACKAGE VERSION\\n"\n')
        outfile.write('"Report-Msgid-Bugs-To: \\n"\n')
        outfile.write('"POT-Creation-Date: 2024-01-27 12:00+0000\\n"\n')
        outfile.write('"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n')
        outfile.write('"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n')
        outfile.write('"Language-Team: LANGUAGE <LL@li.org>\\n"\n')
        outfile.write('"Language: \\n"\n')
        outfile.write('"MIME-Version: 1.0\\n"\n')
        outfile.write('"Content-Type: text/plain; charset=UTF-8\\n"\n')
        outfile.write('"Content-Transfer-Encoding: 8bit\\n"\n')
        outfile.write('"Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\\n"\n')
        outfile.write('\n')
        for py_file in find_python_files(plugin_root):
            extract_strings(py_file, outfile)