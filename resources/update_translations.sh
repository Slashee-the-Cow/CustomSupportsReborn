#!/bin/bash

PLUGIN_NAME="customsupportsreborn"
I18N_DIR="i18n"

pushd ..

echo "Extracting translations from Python files..."
python resources/extract_translations.py

echo "Extracting translations from QML files..."
find . -name "*.qml" -print0 | while IFS= read -r -d $'\0' qml_file; do
  xgettext --package-name="$PLUGIN_NAME" -o resources/"$I18N_DIR"/"$PLUGIN_NAME".pot \
    --join-existing --language=javascript --from-code=UTF-8 \
    -ki18n:1 -ki18nc:1c,2 -ki18np:1,2 -ki18ncp:1c,2,3 "$qml_file"
done

echo "Updating .po files..."
find resources/"$I18N_DIR" -type d -print0 | while IFS= read -r -d $'\0' locale_dir; do
  po_file="$locale_dir/$PLUGIN_NAME.po"
  if [ ! -f "$po_file" ]; then
    echo "Creating: $po_file"
    cp resources/"$I18N_DIR"/"$PLUGIN_NAME".pot "$po_file"
  else
    echo "Updating: $po_file"
    msgmerge --update "$po_file" resources/"$I18N_DIR"/"$PLUGIN_NAME".pot
  fi
done

echo "Compiling .mo files..."
find resources/"$I18N_DIR" -type d -print0 | while IFS= read -r -d $'\0' locale_dir; do
  po_file="$locale_dir/$PLUGIN_NAME.po"
  if [ -f "$po_file" ]; then
    mo_file="$locale_dir/LC_MESSAGES/$PLUGIN_NAME.mo"
    echo "Compiling: $mo_file"
    mkdir -p "$locale_dir/LC_MESSAGES" # Create directory if it doesn't exist
    msgfmt "$po_file" -o "$mo_file"
    if [ $? -ne 0 ]; then
      echo "msgfmt failed."
    fi
  fi
done

popd

echo "Done!"