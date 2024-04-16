import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import requests
import os
import zipfile
import json
from PIL import Image, ImageTk
import io
import threading
import webbrowser

def launch_game():
    try:
        subprocess.Popen([config["launcher_exe_name"]])
    except FileNotFoundError:
        print("Error: Launcher exe not found!")

def update_game():
    try:
        response = requests.get(config["download_url"])
        with open("game_update.zip", "wb") as file:
            file.write(response.content)

        with zipfile.ZipFile("game_update.zip", "r") as zip_ref:
            zip_ref.extractall()

        os.remove("game_update.zip")

        print("Update complete!")
    except Exception as e:
        print("Error updating game:", e)

def display_news():
    try:
        with open(config["news_json_path"], "r") as file:
            news = json.load(file)
            news_text.config(state=tk.NORMAL)
            news_text.delete(1.0, tk.END)
            for item in news:
                news_text.insert(tk.END, f"{item['title']}:\n", "title")
                news_text.insert(tk.END, f"{item['content']}\n\n", "content")
            news_text.config(state=tk.DISABLED)

            news_text.tag_config("title", font=("Helvetica", 12, "bold"), foreground="blue")
            news_text.tag_config("content", font=("Helvetica", 10), foreground="black")

            num_lines = sum(1 for _ in news_text.get("1.0", "end").split("\n"))
            window_height = num_lines * 20

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
        background_url = config["background_image_url"]
        response = requests.get(background_url)
        img = Image.open(io.BytesIO(response.content))
        return img
    except Exception as e:
        print("Error loading background image:", e)
        return None

def load_icon():
    try:
        icon_path = config["icon_path"]
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
    webbrowser.open(link)

with open("config.json", "r") as config_file:
    config = json.load(config_file)

INITIAL_WINDOW_HEIGHT = 900

root = tk.Tk()
root.title("Game Launcher")
root.geometry(f"800x{INITIAL_WINDOW_HEIGHT}")

original_image = load_background_image()
if original_image:
    resized_image = original_image.resize((600, 400), Image.LANCZOS)
    resized_background_image = ImageTk.PhotoImage(resized_image)
    background_label = tk.Label(root, image=resized_background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    root.bind("<Configure>", resize_image)

icon_path = load_icon()
if icon_path:
    root.iconbitmap(icon_path)

button_frame = tk.Frame(root)
button_frame.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

launch_button = ttk.Button(button_frame, text="Launch Game", command=launch_game, style="TButton")
launch_button.pack(side=tk.LEFT, padx=10)

update_button = ttk.Button(button_frame, text="Update Game", command=background_tasks, style="TButton")
update_button.pack(side=tk.LEFT, padx=10)

news_frame = tk.Frame(root)
news_frame.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

news_text = tk.Text(news_frame, width=50, height=10)
news_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(news_frame, command=news_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

news_text.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)

display_news()

discord_label = tk.Label(root, text="Join our Discord", fg="blue", cursor="hand2")
discord_label.bind("<Button-1>", lambda event: open_link(config["discord_link"]))
discord_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

website_label = tk.Label(root, text="Visit our website", fg="blue", cursor="hand2")
website_label.bind("<Button-1>", lambda event: open_link(config["website_link"]))
website_label.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

root.mainloop()