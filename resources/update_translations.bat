@echo off
set PLUGIN_NAME=customsupportsreborn
set I18N_DIR=i18n

pushd ..

echo Extracting translations from Python files...
python resources\extract_translations.py

echo Extracting translations from QML files...
for /f "delims=" %%a in ('dir /b /s *.qml') do (
    xgettext --package-name="%PLUGIN_NAME%" -o resources\%I18N_DIR%\%PLUGIN_NAME%.pot --join-existing --language=javascript --omit-header --from-code=UTF-8 -ki18n:1 -ki18nc:1c,2 -ki18np:1,2 -ki18ncp:1c,2,3 "%%a"
)

setlocal EnableDelayedExpansion

echo Updating .po files...
for /d %%a in (resources\%I18N_DIR%\*) do (
    set po_file=%%a\%PLUGIN_NAME%.po
    if exist "!po_file!" (
        echo Updating: !po_file!
        msgmerge --update "!po_file!" resources\%I18N_DIR%\%PLUGIN_NAME%.pot
    ) else (
        echo Creating: !po_file!
        copy resources\%I18N_DIR%\%PLUGIN_NAME%.pot "!po_file!"
    )
)

echo Compiling .mo files...
for /d %%a in (resources\%I18N_DIR%\*) do (
    set po_file=%%a\%PLUGIN_NAME%.po
    if exist "!po_file!" (
        set mo_file=%%a\LC_MESSAGES\%PLUGIN_NAME%.mo
        echo Compiling: !mo_file!
        if not exist "%%a\LC_MESSAGES" mkdir "%%a\LC_MESSAGES"
        msgfmt "!po_file!" -o "!mo_file!"
        if !errorlevel! NEQ 0 ( <--- Check errorlevel immediately after msgfmt
            echo msgfmt failed.
            set temp_po=%%a\%PLUGIN_NAME%.po~
            if exist "!temp_po!" (
                echo Deleting temporary file: !temp_po!
                del "!temp_po!"
            )
        )
    )
)


endlocal
popd

echo Done!
pause