# Overview
This repo is a Teamfight Tactics bot

# Setup
This bot is built using Python 3. Install the Python requirements by running the following at the root of the project:
``` bash
pip install -r ./requirements.txt
```

It is recommended that you set up a [Python virtual environment](https://docs.python.org/3/library/venv.html) before running the pip install.

# Building
To build, run the following in PowerShell:

``` bash
pyinstaller --add-data ".\res;.\res" .\main.py
```

This will build the Python project to ./dist/main where the executable 'main.exe' can be used to run the bot.