#!/bin/bash
languages=("english" "portuguese" "japanese")
mkdir "Client/resources/translations/"

for lang in "${languages[@]}"; do
    filename="${lang}_translations"
    pyside6-lupdate Client/mainwindow.py Client/form.ui Client/settings.ui Client/Settings.py -ts "Client/resources/translations/$filename.ts"
    echo "Generated $filename.ts for language: $lang"
done
