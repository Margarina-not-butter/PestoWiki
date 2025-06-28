#!/bin/bash
fileslocation="Client"
files=("margarina.py" "resources.py" "Settings.py" "ui_form.py"  "settings.ui") 
outputdir="PestoWiki.AppDir/usr/bin"
mkdir "$outputdir"

for file in "${files[@]}"; do
    old="$fileslocation/$file"
    new="$outputdir/$file"
    cp "$old" "$new"
    echo "Copied to $new ($file)"
done
