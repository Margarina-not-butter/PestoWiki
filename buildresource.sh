#!/bin/bash
input_dir="Client/langsource"
output_dir="Client/resources/translations"

mkdir -p "$output_dir"

for infile in "$input_dir"/*.ts; do
    if [[ ! -e "$infile" ]]; then
        echo "No .ts files found in $input_dir."
        exit 1
    fi

    filename=$(basename "$infile" .ts)
    outfile="${filename}.qm"

    pyside6-lrelease "$infile" -qm "$output_dir/$outfile"

    echo "Generated $output_dir/$outfile from $infile"
done

pyside6-rcc Client/resources/res.qrc -o Client/resources.py
