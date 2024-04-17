# EoServ Client Launcher

The EoServ Client Launcher is a Client Updater and Luancher with a news feature. It is a simple GUI application built with Tkinter in Python. It allows users to update and launch a client application, while also providing news updates fetched from a remote server.

## Features

- Background Image: The app displays a background image fetched from a URL.
- Update Button: Clicking this button triggers the download and update process for the client application.
- Launch Button: Clicking this button launches the client application if it exists.
- Progress Bar: Shows the progress of the download and update process.
- News Display: The app fetches news data from a remote server and displays it in a text box. Users can click on links within the text to visit corresponding web pages.

## Usage

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Run the application by executing `python main.py`.
3. Upon launch, the app will display the background image along with news updates fetched from a remote server.
4. Click the "Update" button to download and update the client application.
5. Once updated, click the "Launch" button to start the client application.
6. News updates are displayed in the text box, where users can click on links to visit relevant web pages.

## Dependencies

- Python 3.x
- tkinter
- Pillow
- aiohttp

## Notes

- Ensure an active internet connection to fetch the background image and news updates.
- The client application must be hosted at a specific URL for the update functionality to work properly.
- Adjust the URLs in the code to match your server configurations.
- Change the config.json url to your config.json. 




![EOServLauncher](https://github.com/HelloByeLetsNot/EOServLauncher/blob/main/Updatedbuttons.png)



## How to edit and distribute as exe
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

### 3. Customize the Background Image, Download Link, and Exe Name

To customize these elements, users can edit the following lines in the Python script (`main.py`):

1. **Background Image**: Replace the URL in the `load_background` method with the desired background image URL.

2. **Download Link**: Edit the URL in the `download_and_update` method to point to the desired download link for the client application.

3. **Exe Name**: After creating the executable, users can rename it by simply renaming the generated `main.exe` file in the `dist` directory to their desired name.

### Additional Notes

- Make sure to include any necessary image files or assets alongside the executable if they are referenced in the script.

- Users may need to adjust the file paths or additional configurations based on their specific requirements.

With these steps, users can easily turn your Python script into an executable file and customize it to their liking.
