[Português Brasileiro](README-PT.md)

# PestoWiki
Multi-platform customizable client for wikis written in Python using PySide6 (QT).

_PestoWiki is mostly tested in my MediaWiki instance, the default shortcuts are designed for MediaWiki but can be changed as needed. Any in compatibilities with DokuWiki or other wiki softwares can be added as an issue in this repo's issues tab_

![Screenshot_20250628_172806](https://github.com/user-attachments/assets/0d5afeba-cfd3-403a-8405-b3f4a0153645)

## Features
 - [x] Editing shortcuts (bold, code, etc...)
 - [x] Navigation/edit mode (toggle user-select)
 - [x] Custom editing shorcuts
 - [x] Settings
 - [x] Change wiki address
 - [x] Option to disable passing links that are outside of wiki's address to system
 - [x] Go menu
 - [x] Translations
 - [x] JS injection
 - [x] Custom JS library with wiki related functions
 - [x] Favorites
 - [x] Check for updates
 - [x] Share button (_Browsing > Copy current page's address_)

## How to compile
- Clone the repo and install `requirements.txt` in a venv (optional) with:
```
python -m venv .venv
pip install -r requirements.txt
```
- Generate `resources.py` using `buildresource.sh`. (It works just fine with Git Bash on Windows.)

## Packaging

<img src="https://github.com/user-attachments/assets/86185670-548b-49ce-b14e-2b8652855660" width="150" align="right"/>

### AppImage
For packaging Pesto into an AppImage you'll need AppImageTool. To package it just run `yourappimagetool.AppImage PestoWiki.AppDir`, this will produce an AppImage without any dependencies, you'll have to figure this manually if you want those (create an AppImage from the output of PyInstaller - guide below). The system running the AppImage will need `PySide6` and `requests` Python modules installed.

### With PyInstaller
PyInstaller will generate a HUGE (~400mb) folder with a single binary and all the dependencies in a folder that should be shipped with the binary for it to work (you can package the dependencies folder together with the binary but that will be a great hit on performance, as it will have to unpack everything when the app is launched). The repo already has a `spec` file that is used by PyInstaller to build the application, you can build it with the following command:
```
python -m PyInstaller pesto.spec
```
It will be compiled to `./dist`.

### For MacOS users
Currently I cannot support releases for any MacOS versions as it's not an friendly enviroment for developers who have no iDevices available. Feel free to share MacOS builds you made yourself to me and I will link them here.
