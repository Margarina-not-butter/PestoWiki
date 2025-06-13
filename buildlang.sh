read -p "Please enter the name of the input TS file: " infile
read -p "Please enter the name of the generated QM file: " outfile
pyside6-lrelease "$infile.ts" -qm "translations/$outfile.qm"
