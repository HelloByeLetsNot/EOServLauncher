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
import webbrowser

class RoundButton(tk.Canvas):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self.round_rectangle = self.create_round_rectangle(0, 0, self.width, self.height, radius=20, fill="#c0c0c0", outline="")
        self.bind("<ButtonPress-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.text = None

    def create_round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]

        return self.create_polygon(points, **kwargs, smooth=True)

    def on_click(self, event):
        self.itemconfig(self.round_rectangle, fill="#a0a0a0")
        self.update()
        self.master.after(100, lambda: self.itemconfig(self.round_rectangle, fill="#c0c0c0"))
        self.invoke()

    def on_enter(self, event):
        self.itemconfig(self.round_rectangle, fill="#d0d0d0")

    def on_leave(self, event):
        self.itemconfig(self.round_rectangle, fill="#c0c0c0")

class LaunchButton(RoundButton):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.text = "Launch Game"
        self.draw_text()

    def draw_text(self):
        self.create_text(self.width / 2, self.height / 2, text=self.text, font=("Arial", 12), fill="black")

    def invoke(self):
        try:
            subprocess.Popen([config["launcher_exe_name"]])
        except FileNotFoundError:
            print("Error: Launcher exe not found!")

class UpdateButton(RoundButton):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.text = "Update Game"
        self.draw_text()

    def draw_text(self):
        self.create_text(self.width / 2, self.height / 2, text=self.text, font=("Arial", 12), fill="black")

    def invoke(self):
        threading.Thread(target=self.update_game).start()
        threading.Thread(target=self.display_news).start()

    def update_game(self):
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

    def display_news(self):
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

with open("config.json", "r") as config_file:
    config = json.load(config_file)

INITIAL_WINDOW_HEIGHT = 900

root = tk.Tk()
root.title("Game Launcher")
root.geometry(f"800x{INITIAL_WINDOW_HEIGHT}")

background_image_url = config.get("background_image_url", "")
if background_image_url:
    try:
        response = requests.get(background_image_url)
        img = Image.open(io.BytesIO(response.content))
        resized_img = img.resize((600, 400), Image.LANCZOS)
        background_photo = ImageTk.PhotoImage(resized_img)
        background_label = tk.Label(root, image=background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Error loading background image:", e)

icon_path = config.get("icon_path", "")
if icon_path and os.path.exists(icon_path):
    root.iconbitmap(icon_path)

button_frame = tk.Frame(root)
button_frame.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

launch_button = LaunchButton(button_frame, width=120, height=40)
launch_button.pack(side=tk.LEFT, padx=10)

update_button = UpdateButton(button_frame, width=120, height=40)
update_button.pack(side=tk.LEFT, padx=10)

news_frame = tk.Frame(root)
news_frame.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

news_text = tk.Text(news_frame, width=50, height=10)
news_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(news_frame, command=news_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

news_text.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)

root.mainloop()