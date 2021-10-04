# Overview
This repo is a Teamfight Tactics bot

# Setup
This bot is built using Python 3. Install the Python requirements by running the following at the root of the project:
``` bash
pip install -r ./requirements.txt
```

Currently, using virtual environments is not working with pyinstaller, so you have to install the dependencies in your main environment.

# Building
To build, run the following in PowerShell:

``` bash
pyinstaller --add-data ".\res;.\res" .\main.py
```

This will build the Python project to ./dist/main where the executable 'main.exe' can be used to run the bot.