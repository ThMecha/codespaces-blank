import os
import tkinter as tk
from tkinter import simpledialog, filedialog
from PIL import ImageGrab
from dotenv import load_dotenv, set_key
import keyboard

ENV_PATH = ".env"

# Helper to load all keys from .env
def get_env_keys():
    if not os.path.exists(ENV_PATH):
        return []
    load_dotenv(ENV_PATH)
    with open(ENV_PATH) as f:
        lines = f.readlines()
    keys = [line.split('=')[0] for line in lines if '=' in line]
    return keys

# GUI crop tool
def crop_tool():
    root = tk.Tk()
    root.withdraw()
    root.update()
    root.deiconify()
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.3)
    canvas = tk.Canvas(root, cursor="cross")
    canvas.pack(fill=tk.BOTH, expand=True)
    start = [0, 0]
    rect = [None]
    coords = [0, 0, 0, 0]

    def on_press(event):
        start[0], start[1] = event.x, event.y
        rect[0] = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline='red', width=2)

    def on_drag(event):
        canvas.coords(rect[0], start[0], start[1], event.x, event.y)

    def on_release(event):
        coords[0], coords[1], coords[2], coords[3] = start[0], start[1], event.x, event.y
        root.quit()

    canvas.bind('<ButtonPress-1>', on_press)
    canvas.bind('<B1-Motion>', on_drag)
    canvas.bind('<ButtonRelease-1>', on_release)
    root.mainloop()
    root.destroy()
    return coords

# Save crop to .env
def save_crop_to_env(key, coords):
    value = ','.join(map(str, coords))
    set_key(ENV_PATH, key, value)

# Dropdown for env keys
def select_env_key():
    keys = get_env_keys()
    if not keys:
        print("No keys in .env")
        return None
    root = tk.Tk()
    root.withdraw()
    key = simpledialog.askstring("Select Key", f"Available keys: {', '.join(keys)}\nEnter key:")
    root.destroy()
    return key

# Main logic: listen for Shift+C
print("Listening for Shift+C...")
while True:
    keyboard.wait('shift+c')
    print("Capture triggered!")
    coords = crop_tool()
    key = simpledialog.askstring("Save Crop", "Enter a name for this crop:")
    if key:
        save_crop_to_env(key, coords)
        print(f"Saved crop as {key} in .env")
    # Show dropdown for selection
def show_dropdown():
    key = select_env_key()
    if key:
        print(f"Selected key: {key}")

# Uncomment to test dropdown
# show_dropdown()
