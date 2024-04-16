import tkinter as tk
from tkinter import ttk
import subprocess
import requests
import os
import zipfile
import json
from PIL import Image, ImageTk
import io
import threading

def launch_game():
    try:
        subprocess.Popen(["Restart.exe"])  # Replace with actual path to Restart.exe
    except FileNotFoundError:
        print("Error: Restart.exe not found!")

def update_game():
    try:
        # Download EORClient.zip
        url = "http://endless-online-restart.com/downloads/EORClient.zip"
        response = requests.get(url)
        with open("EORClient.zip", "wb") as file:
            file.write(response.content)

        # Unzip EORClient.zip
        with zipfile.ZipFile("EORClient.zip", "r") as zip_ref:
            zip_ref.extractall()  # Extract in the same folder as the launcher

        os.remove("EORClient.zip")  # Remove the downloaded zip file

        print("Update complete!")
    except Exception as e:
        print("Error updating game:", e)

def display_news():
    try:
        # Load news from JSON file
        with open("news.json", "r") as file:
            news = json.load(file)
            news_text.config(state=tk.NORMAL)
            news_text.delete(1.0, tk.END)
            for item in news:
                news_text.insert(tk.END, f"{item['title']}:\n", "title")
                news_text.insert(tk.END, f"{item['content']}\n\n", "content")
            news_text.config(state=tk.DISABLED)

            # Apply styles to title and content
            news_text.tag_config("title", font=("Helvetica", 12, "bold"), foreground="blue")
            news_text.tag_config("content", font=("Helvetica", 10), foreground="black")

            # Calculate required window height based on number of lines
            num_lines = sum(1 for _ in news_text.get("1.0", "end").split("\n"))
            window_height = num_lines * 20  # Adjust 20 according to your font size

            # Adjust window size based on content
            root.geometry(f"800x{window_height}")
    except FileNotFoundError:
        print("News file not found!")
    except Exception as e:
        print("Error loading news:", e)

def resize_image(event):
    global resized_image, resized_background_image
    new_width = event.width
    new_height = event.height
    resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
    resized_background_image = ImageTk.PhotoImage(resized_image)
    background_label.config(image=resized_background_image)

def load_background_image():
    try:
        background_url = "https://cdn.discordapp.com/attachments/1058522584192397394/1066115319187386559/image.png?ex=662c2443&is=6619af43&hm=9d19574e4301882c3825840b6619c1bc2498064a7e446fbab461e19a58cf3399&"
        response = requests.get(background_url)
        img = Image.open(io.BytesIO(response.content))
        return img
    except Exception as e:
        print("Error loading background image:", e)
        return None

def load_icon():
    try:
        icon_path = "icon.ico"
        if os.path.exists(icon_path):
            return icon_path
        else:
            print("Icon file not found.")
            return None
    except Exception as e:
        print("Error loading icon:", e)
        return None

def background_tasks():
    threading.Thread(target=update_game).start()
    threading.Thread(target=display_news).start()

def open_link(link):
    # Replace [discord_link] and [website_link] with actual URLs
    # Example: 
    # link = "https://discord.gg/example"
    # link = "https://www.example.com"
    pass  # Add code to open the link in the default web browser

# Set the initial window height
INITIAL_WINDOW_HEIGHT = 900

root = tk.Tk()
root.title("Game Launcher")

# Set the window size
root.geometry(f"800x{INITIAL_WINDOW_HEIGHT}")

# Load background image
original_image = load_background_image()
if original_image:
    resized_image = original_image.resize((600, 400), Image.LANCZOS)
    resized_background_image = ImageTk.PhotoImage(resized_image)
    background_label = tk.Label(root, image=resized_background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    root.bind("<Configure>", resize_image)

# Load window icon
icon_path = load_icon()
if icon_path:
    root.iconbitmap(icon_path)

# Frame for Launch and Update buttons
button_frame = tk.Frame(root)
button_frame.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

# Launch Game button
launch_button = ttk.Button(button_frame, text="Launch Game", command=launch_game, style="TButton")
launch_button.pack(side=tk.LEFT, padx=10)

# Update Game button
update_button = ttk.Button(button_frame, text="Update Game", command=background_tasks, style="TButton")
update_button.pack(side=tk.LEFT, padx=10)

# News Text Window
news_frame = tk.Frame(root)
news_frame.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

news_text = tk.Text(news_frame, width=50, height=10)
news_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(news_frame, command=news_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

news_text.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)

# Display News
display_news()

# Links to Discord and Website
discord_label = tk.Label(root, text="Join our Discord at: [link]", fg="blue", cursor="hand2")
discord_label.bind("<Button-1>", lambda event: open_link("[discord_link]"))
discord_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

website_label = tk.Label(root, text="Visit our website at: [link]", fg="blue", cursor="hand2")
website_label.bind("<Button-1>", lambda event: open_link("[website_link]"))
website_label.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

root.mainloop()