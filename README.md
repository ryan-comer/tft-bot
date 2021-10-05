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

# Images
The bot is based on computer vision that looks for UI elements to determine where the bot is in the match loop. The res/ folder has images that the bot uses to look for on the screen. These images were captured using a specific System and League Client resolution, and might not work for you. To ensure the bot works, you need to take screen-grabs for each image in the res/ folder using the computer that the bot will run on.

# Running
When you run the bot, you will be presented with a UI that you use to manage the bot. Before clicking the start button, make sure the League client is up and you're sitting in the lobby for a TFT game. When you start the bot, the bot will click the start game button and the game loops will begin.