import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io
import zipfile
import threading
import webbrowser
import subprocess
import os
import json

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
        webbrowser.open(self.url)

class UpdateButton(RoundButton):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.text = "Update Game"
        self.draw_text()
        self.update_url = ""
        self.executable_name = ""

    def draw_text(self):
        self.create_text(self.width / 2, self.height / 2, text=self.text, font=("Arial", 10), fill="white")

    def invoke(self):
        threading.Thread(target=self.update_game).start()

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
                subprocess.Popen([self.executable_name])
            else:
                self.update_status("No updates available.")
                subprocess.Popen([self.executable_name])

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
            response = requests.get(self.update_url)
            return response.text.strip()
        except Exception as e:
            print("Error getting remote version:", e)
            return ""

    def download_update(self):
        try:
            with requests.get(self.update_url, stream=True) as response:
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
                    if file != self.executable_name and not os.path.exists(
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
            with requests.get(self.update_url, stream=True) as response:
                response.raise_for_status()

                with open(self.executable_name, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

        except Exception as e:
            print("Error downloading new client:", e)

class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Launcher")
        self.geometry("800x600")
        self.minsize(800, 600)
        self.maxsize(800, 600)
        self.load_config()
        self.load_background()
        self.load_news()
        self.create_buttons()

    def load_config(self):
        try:
            with open("config.json", "r") as config_file:
                self.config_data = json.load(config_file)
        except FileNotFoundError:
            print("Config file not found.")
            messagebox.showerror("Error", "Config file not found.")
            self.destroy()

    def load_background(self):
        try:
            background_url = self.config_data["background"]
            response = requests.get(background_url)
            image_data = response.content
            self.background_image = ImageTk.PhotoImage(Image.open(io.BytesIO(image_data)))
            self.background_label = tk.Label(self, image=self.background_image)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.background_label.image = self.background_image
        except Exception as e:
            print("Error loading background image:", e)
            messagebox.showerror("Error", "Failed to load background image.")

    def load_news(self):
        try:
            news_url = self.config_data["news"]
            response = requests.get(news_url)
            news_text = response.text
            self.news_text = tk.Text(self, wrap="word", font=("Arial", 12), padx=10, pady=10)
            self.news_text.insert(tk.END, news_text)
            self.news_text.config(state="disabled")
            self.news_text.place(relx=0.5, rely=0.1, anchor="center", relwidth=0.8, relheight=0.6)
        except Exception as e:
            print("Error loading news:", e)
            messagebox.showerror("Error", "Failed to load news.")

    def create_buttons(self):
        donate_button = DonationButton(self, width=120, height=40)
        donate_button.place(relx=0.2, rely=0.85, anchor="center")
        donate_button.url = self.config_data.get("donate", "")

        update_button = UpdateButton(self, width=120, height=40)
        update_button.place(relx=0.8, rely=0.85, anchor="center")
        update_button.update_url = self.config_data.get("update", {}).get("url", "")
        update_button.executable_name = self.config_data.get("update", {}).get("executable", "")

if __name__ == "__main__":
    app = Launcher()
    app.mainloop()
