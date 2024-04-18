# Game Launcher

Welcome to the Game Launcher repository! This launcher is a Python application designed to facilitate easy access to game updates, news, and donation options for players.

## Features

- **Update Game:** Check for and download game updates effortlessly.
- **News Feed:** Stay up-to-date with the latest news and announcements.
- **Donation Button:** Support the development of the game through donations.
- **Customizable Configuration:** Edit URLs and other settings via a `config.json` file.

## Getting Started

To get started with the Game Launcher, follow these steps:

## Editing the Configuration
The Game Launcher application uses a config.json file to store configuration parameters such as URLs for background images, news data, donation links, and update information. Follow the steps below to edit the configuration:

Open the config.json file located in the same directory as the launcher.py script.

Modify the values of the following keys according to your requirements:
"background": URL of the background image.
"news": URL of the JSON file containing news data.
"donate": URL of the donation link.
"update": Object containing update information:
"url": URL of the update file (zip archive).
"executable": Name of the executable file to be launched after updating.
Save the config.json file after making changes.
Creating an Executable with auto-py-to-exe
The Game Launcher application can be converted into an executable using auto-py-to-exe, a graphical user interface-based application that converts Python scripts into Windows executables.

## Follow the steps below to create an executable using auto-py-to-exe:

Install auto-py-to-exe:


pip install auto-py-to-exe

Open auto-py-to-exe by running the following command in your terminal:

auto-py-to-exe

In the auto-py-to-exe window, follow these steps:

Click on the "Browse" button and select the launcher.py script.
Configure the settings such as the output directory and other options according to your preferences.
Click on the "Convert .py to .exe" button to start the conversion process.
Once the process is complete, the executable file will be generated in the specified output directory.
You can now distribute the generated executable file to users who can run the Game Launcher application without needing Python installed.
Running the Game Launcher
After creating the executable, users can simply double-click on the generated executable file to run the Game Launcher application. The launcher will load the configuration from the config.json file and display the launcher interface with the specified background image, news data, and buttons for donation and updating the game.

