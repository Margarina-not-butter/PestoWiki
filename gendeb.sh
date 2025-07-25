#!/bin/bash
fileslocation="Client"
files=("margarina.py" "resources.py" "Settings.py" "ui_form.py"  "settings.ui") 
outputdir="debian/pestowiki"


for file in "${files[@]}"; do
    old="$fileslocation/$file"
    new="$outputdir/$file"
    cp "$old" "$new"
    echo "Copied to $new ($file)"
done
chmod -R 755 debian
chmod +x "$outputdir/margarina.py"
cd debian
pwd
dpkg-buildpackage -us -uc
