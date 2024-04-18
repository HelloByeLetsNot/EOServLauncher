import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io
import subprocess
import os
import zipfile
import threading
import webbrowser
import json

# Load the config from the JSON file
with open('config.json') as f:
    config = json.load(f)

class RoundButton(tk.Canvas):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.config(highlightthickness=0, background="#FFA07A")
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self.round_rectangle = self.create_round_rectangle(0, 0, self.width, self.height, radius=10, fill="", outline="")
        self.bind("<ButtonPress-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def create_round_rectangle(self, x1, y1, x2, y2, radius=10, **kwargs):
        points = [x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius, x2, y1 + radius,
                  x2, y2 - radius, x2, y2 - radius, x2, y2, x2 - radius, y2, x2 - radius, y2, x1 + radius, y2, x1 + radius, y2,
                  x1, y2, x1, y2 - radius, x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1, y1]

        return self.create_polygon(points, **kwargs, smooth=True)

    def on_click(self, event):
        self.itemconfig(self.round_rectangle, fill="#FF6347")
        self.update()
        self.master.after(100, lambda: self.itemconfig(self.round_rectangle, fill=""))
        self.invoke()

    def on_enter(self, event):
        self.itemconfig(self.round_rectangle, fill="#FF8C69")

    def on_leave(self, event):
        self.itemconfig(self.round_rectangle, fill="#FFA07A")

class DonationButton(RoundButton):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.text = "Donate"
        self.draw_text()

    def draw_text(self):
        self.create_text(self.width / 2, self.height / 2, text=self.text, font=("Arial", 10), fill="white")

    def invoke(self):
        webbrowser.open(config["donate_link"])

class UpdateButton(RoundButton):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.text = "Update Game"
        self.draw_text()

    def draw_text(self):
        self.create_text(self.width / 2, self.height / 2, text=self.text, font=("Arial", 10), fill="white")

    def invoke(self):
        threading.Thread(target=self.update_game).start()

    def update_status(self, status):
        self.delete("status_text")
        self.create_text(self.width / 2, self.height / 2 - 10, text=status, font=("Arial", 8), fill="white",
                         tag="status_text")

    def update_game(self):
        try:
            self.update_status("Updating...")
            print("Updating ...")

            local_version = self.load_local_version()
            remote_version = self.get_remote_version()

            if not remote_version or local_version != remote_version:
                self.update_status("Downloading update...")
                self.download_update()
                self.update_status("Update complete!")
                self.update_local_version(remote_version)
                messagebox.showinfo("Update Complete", "Game updated successfully.")
                subprocess.Popen([config["update"]["executable"]])
            else:
                self.update_status("No updates available.")
                subprocess.Popen([config["update"]["executable"]])

        except Exception as e:
            self.update_status(f"Error updating game: {e}")
            print("Error updating game:", e)

    def load_local_version(self):
        version_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "launcherdata", "version.txt")
        try:
            with open(version_file, "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            # If local version.txt file not found, download new client and create version.txt
            self.download_new_client()
            new_version = self.get_remote_version()
            self.create_local_version(new_version)
            return new_version

    def create_local_version(self, version):
        version_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "launcherdata", "version.txt")
        try:
            with open(version_file, "w") as file:
                file.write(version)
        except Exception as e:
            print("Error creating local version:", e)

    def get_remote_version(self):
        try:
            response = requests.get(config["update_link"])
            return response.text.strip()
        except Exception as e:
            print("Error getting remote version:", e)
            return ""

    def download_update(self):
        try:
            with requests.get(config["update_zip_link"], stream=True) as response:
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                bytes_written = 0
                with open("EORClient.zip", "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            bytes_written += len(chunk)
                            progress = min(int((bytes_written / total_size) * 100), 100)
                            self.update_status(f"Downloading... {progress}%")
                            self.update()

            with zipfile.ZipFile("EORClient.zip", "r") as zip_ref:
                for file in zip_ref.namelist():
                    if file != config["update"]["executable"] and not os.path.exists(
                            os.path.join(os.path.dirname(os.path.abspath(__file__)), file)):
                        zip_ref.extract(file, os.path.dirname(os.path.abspath(__file__)))

            os.remove("EORClient.zip")

        except Exception as e:
            print("Error downloading or extracting update:", e)

    def update_local_version(self, version):
        version_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "launcherdata", "version.txt")
        try:
            with open(version_file, "w") as file:
                file.write(version)
        except Exception as e:
            print("Error updating local version:", e)

    def download_new_client(self):
        try:
            with requests.get(config["new_client_zip_link"], stream=True) as response:
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                bytes_written = 0
                with open("EORClient.zip", "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            bytes_written += len(chunk)
                            progress = min(int((bytes_written / total_size) * 100), 100)
                            print(f"Downloading... {progress}%")
                            self.update_status(f"Downloading.. {progress}%")
                            self.update()

            with zipfile.ZipFile("EORClient.zip", "r") as zip_ref:
                for file in zip_ref.namelist():
                    if file != config["update"]["executable"] and not os.path.exists(
                            os.path.join(os.path.dirname(os.path.abspath(__file__)), file)):
                        zip_ref.extract(file, os.path.dirname(os.path.abspath(__file__)))

            os.remove("EORClient.zip")

        except Exception as e:
            print("Error downloading or extracting new client:", e)

INITIAL_WINDOW_HEIGHT = 600

root = tk.Tk()
root.title("Game Launcher")
root.geometry(f"800x{INITIAL_WINDOW_HEIGHT}")
root.minsize(800, INITIAL_WINDOW_HEIGHT)
root.maxsize(800, INITIAL_WINDOW_HEIGHT)

# Set the background image
try:
    background_response = requests.get(config["background_link"])
    background_image = Image.open(io.BytesIO(background_response.content))
    background_image = background_image.resize((800, INITIAL_WINDOW_HEIGHT), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_photo  # prevent garbage collection
except Exception as e:
    print("Error loading background image:", e)
    root.config(bg="white")

# Load and display news data
news_frame = tk.Frame(root)
news_frame.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

news_text = tk.Text(news_frame, width=50, height=10)
news_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(news_frame, command=news_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

news_text.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)

try:
    response = requests.get(config["news_link"])
    news = response.json()
    print("News data:", news)
except Exception as e:
    print("Error loading news:", e)

if news:
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

# Button frame
link_frame = tk.Canvas(root, bg="#FFA07A", highlightthickness=0, height=50, width=800)
link_frame.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

# Function to open website link
def open_website(event):
    webbrowser.open(config["website_link"])

# Function to open Discord link
def open_discord(event):
    webbrowser.open(config["discord_link"])

# Website button
website_button = RoundButton(link_frame, width=80, height=30)
website_button.create_text(website_button.width / 2, website_button.height / 2, text="Website", font=("Arial", 10),
                           fill="white")
website_button.place(relx=0.15, rely=0.5, anchor=tk.CENTER)
website_button.bind("<Button-1>", open_website)

# Discord button
discord_button = RoundButton(link_frame, width=80, height=30)
discord_button.create_text(discord_button.width / 2, discord_button.height / 2, text="Discord", font=("Arial", 10),
                           fill="white")
discord_button.place(relx=0.85, rely=0.5, anchor=tk.CENTER)
discord_button.bind("<Button-1>", open_discord)

# Donation button
donate_button = DonationButton(link_frame, width=120, height=40)
donate_button.place(relx=0.35, rely=0.5, anchor=tk.CENTER)

# Update button
update_button = UpdateButton(link_frame, width=120, height=40)
update_button.place(relx=0.65, rely=0.5, anchor=tk.CENTER)

root.mainloop()
