# MargarinaWiki Desktop
Multi-platform customizable client for wikis written in Python using PySide6 (QT).

![image](https://github.com/user-attachments/assets/1bb47120-dc75-44e4-a9c5-041f3d1419ef)

## Features
 - [x] Editing shortcuts (bold, code, etc...)
 - [x] Navigation/edit mode
 - [x] Custom editing shorcuts
 - [x] Settings
 - [x] Change wiki address
 - [x] Option to disable passing links that are outside of wiki's address to system
 - [x] Go menu
 - [x] Translations
 - [x] JS injection
 - [x] Custom JS library with wiki related functions
 - [x] Favorites
 - [ ] Share button

## How to compile
First of all, clone the repo and install `requirements.txt` wth `pip install -r requirements.txt`.
Then run the following script:
### On Linux
Compile **all** the translation files with `buildlang.sh` (portuguese.ts > pt, english.ts > en, japanese.ts > jp), then generate `resources.py` using `buildresource.sh`.
```
python -m PyInstaller --windowed --icon=favicon.ico --name "MargarinaWikiDesktop" \
--add-data="resources.py:." \
--add-data="Updater.py:." \
--add-data="Settings.py:." \
--add-data="settings.ui:." \
--add-data="updater.ui:." \
mainwindow.py
```
### On Windows
Currently there are no scripts for compiling translations and resources files on Windows, but I guess that the commands from the scripts for Linux should work.
```
python -m PyInstaller --windowed --icon=favicon.ico --name "MargarinaWikiDesktop"^
 --add-data="resources.py;."^
 --add-data="Updater.py;."^
 --add-data="Settings.py;."^
 --add-data="settings.ui;."^
 --add-data="updater.ui;."^
 mainwindow.py
```
It will be compiled to `./dist`.
