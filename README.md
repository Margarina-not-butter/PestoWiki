# PestoWiki
Multi-platform customizable client for wikis written in Python using PySide6 (QT).

![image](https://github.com/user-attachments/assets/87efa733-7021-47a9-8341-acbb9196a892)

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
 - [ ] Share button

## How to compile
- Clone the repo and install `requirements.txt` in a venv (optional) with:
```
python -m venv .venv
pip install -r requirements.txt
```
- Generate `resources.py` using `buildresource.sh`. (Currently there are no scripts for compiling translations and resources files on Windows, but I guess that the commands from the scripts for Linux should work.)
- Optionally, compile it with PyInstaller:
```
python -m PyInstaller margarina.spec
```
It will be compiled to `./dist`.
