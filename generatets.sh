#!/bin/bash
languages=("english" "portuguese" "japanese")
mkdir "Client/resources/translations/"

for lang in "${languages[@]}"; do
    filename="${lang}"
    pyside6-lupdate Client/margarina.py Client/form.ui Client/settings.ui Client/Settings.py -ts "Client/langsource/$filename.ts"
    echo "Generated $filename.ts for language: $lang"
done
