# Game Launcher

The Game Launcher is a simple GUI application built with Tkinter in Python. It allows users to update and launch a game application, while also providing news updates fetched from a remote server.

## Features

- Background Image: The launcher displays a background image fetched from a URL.
- Update Button: Clicking this button triggers the download and update process for the game application.
- Launch Button: Clicking this button launches the game application if it exists.
- News Display: The launcher fetches news data from a remote server and displays it in a text box. Users can click on links within the text to visit corresponding web pages.

## Usage

1. **Clone the Repository**: Clone this repository to your local machine.

2. **Install Dependencies**: Install the required dependencies by running `pip install -r requirements.txt`.

3. **Edit Configuration**: Edit the `config.json` file to customize the launcher settings:
    - `"background_image_url"`: URL of the background image.
    - `"download_url"`: URL of the game update zip file.
    - `"news_json_path"`: Path to the news JSON file.
    - `"launcher_exe_name"`: Name of the game launcher executable.
    - `"discord_link"`: Link to join the Discord server.
    - `"website_link"`: Link to the game's website.
    - `"icon_path"`: Path to the icon file for the launcher window.

4. **Host News JSON**: Host the `news.json` file on a web server. Update the `"news_json_path"` in the `config.json` file with the appropriate URL.

5. **Run the Application**: Run the application by executing `python launcher.py`.

6. **Launcher Operation**:
    - Click the "Update Game" button to download and update the game application.
    - Once updated, click the "Launch Game" button to start the game application.
    - News updates are displayed in the text box. Click on links to visit relevant web pages.

## Hosting News JSON

To host the `news.json` file:
1. Create a JSON file named `news.json` with the desired news content.
2. Upload the `news.json` file to a web server or any file hosting service.
3. Obtain the URL of the hosted `news.json` file.
4. Update the `"news_json_path"` in the `config.json` file with the obtained URL.

## Customization

You can customize the launcher appearance, background image, and other settings by editing the `config.json` file.

## Dependencies

- Python 3.x
- tkinter
- Pillow
- aiohttp

## Notes

- Ensure an active internet connection to fetch the background image and news updates.
- The game launcher executable must be hosted at a specific URL for the update functionality to work properly.
- Adjust the URLs in the `config.json` file to match your server configurations.
- 
## How distribute as exe
To create an executable (exe) file from your Python script, you can use `pyinstaller`. Here's a step-by-step guide on how to do it:

### 1. Install `pyinstaller`

If you haven't already installed `pyinstaller`, you can do so using pip:

```
pip install pyinstaller
```

### 2. Create the Executable

Navigate to the directory containing your Python script (`main.py`) and run the following command:

```
pyinstaller --onefile main.py
```

This command will create a `dist` directory containing the executable file (`main.exe`) along with any necessary files.
directory to their desired name.

### Additional Notes

- Make sure to include any necessary image files or assets alongside the executable if they are referenced in the script.

- Users may need to adjust the file paths or additional configurations based on their specific requirements.

With these steps, users can easily turn your Python script into an executable file and customize it to their liking.

![EOServLauncher](https://github.com/HelloByeLetsNot/EOServLauncher/blob/main/eolauncher.png)