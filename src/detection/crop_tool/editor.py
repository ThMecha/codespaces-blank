"""
Crop editor GUI for selecting screen regions.
"""

import tkinter as tk
from tkinter import simpledialog, ttk
from PIL import ImageGrab, Image, ImageTk
import os
import sys
from typing import Tuple, List, Optional

class CropEditor:
    def __init__(self):
        """Initialize the crop editor GUI."""
        self.root = None
        self.canvas = None
        self.start_x = 0
        self.start_y = 0
        self.rect_id = None
        self.screenshot = None
        self.screenshot_tk = None
        self.coords = [0, 0, 0, 0]  # x1, y1, x2, y2
        
    def take_screenshot(self) -> None:
        """Capture the entire screen."""
        self.screenshot = ImageGrab.grab()
        
    def start_editor(self) -> Tuple[int, int, int, int]:
        """
        Start the crop editor GUI.
        
        Returns:
            Tuple[int, int, int, int]: Selected coordinates (x1, y1, x2, y2)
        """
        self.take_screenshot()
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Crop Editor")
        self.root.attributes('-fullscreen', True)
        
        # Convert PIL image to Tkinter PhotoImage
        self.screenshot_tk = ImageTk.PhotoImage(self.screenshot)
        
        # Create canvas with screenshot as background
        self.canvas = tk.Canvas(
            self.root, 
            width=self.screenshot.width, 
            height=self.screenshot.height,
            cursor="cross"
        )
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.screenshot_tk)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind canvas events
        self.canvas.bind('<ButtonPress-1>', self._on_press)
        self.canvas.bind('<B1-Motion>', self._on_drag)
        self.canvas.bind('<ButtonRelease-1>', self._on_release)
        
        # Instructions label
        instructions = tk.Label(
            self.root,
            text="Click and drag to select an area. Press ESC to cancel.",
            bg="white",
            fg="black",
            font=("Arial", 12)
        )
        instructions.place(x=10, y=10)
        
        # Bind escape key to cancel
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
        self.root.mainloop()
        
        return tuple(self.coords)
    
    def _on_press(self, event) -> None:
        """Handle mouse button press event."""
        self.start_x, self.start_y = event.x, event.y
        # Remove previous rectangle if it exists
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        # Create new rectangle
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, 
            self.start_x, self.start_y,
            outline='red', width=2
        )
        
    def _on_drag(self, event) -> None:
        """Handle mouse drag event."""
        if self.rect_id:
            self.canvas.coords(
                self.rect_id,
                self.start_x, self.start_y,
                event.x, event.y
            )
            
            # Display coordinates
            self._update_coord_display(event.x, event.y)
            
    def _on_release(self, event) -> None:
        """Handle mouse button release event."""
        # Store the final coordinates
        x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
        x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)
        
        self.coords = [x1, y1, x2, y2]
        self.root.quit()
        
    def _update_coord_display(self, current_x: int, current_y: int) -> None:
        """Update coordinate display during selection."""
        width = abs(current_x - self.start_x)
        height = abs(current_y - self.start_y)
        
        # Find top-left coordinates
        x = min(self.start_x, current_x)
        y = min(self.start_y, current_y)
        
        # Remove previous text if it exists
        self.canvas.delete("coord_text")
        
        # Display coordinates
        text = f"Position: ({x}, {y}), Size: {width}×{height}"
        self.canvas.create_text(
            10, 40,
            text=text,
            anchor=tk.NW,
            fill="red",
            font=("Arial", 12),
            tags="coord_text"
        )


class EnvKeySelector:
    def __init__(self, keys: List[str]):
        """
        Initialize the environment key selector.
        
        Args:
            keys (List[str]): List of existing keys in .env file
        """
        self.keys = keys
        self.selected_key = None
        
    def show_dialog(self) -> Optional[str]:
        """
        Show a dialog for selecting or creating a new environment key.
        
        Returns:
            Optional[str]: Selected or created key, or None if canceled
        """
        dialog = tk.Toplevel()
        dialog.title("Select or Create Position Key")
        dialog.geometry("400x250")
        dialog.grab_set()  # Make dialog modal
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Frame for existing keys
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        ttk.Label(frame, text="Select an existing key or create a new one:").pack(pady=5)
        
        # Existing keys listbox
        listbox = tk.Listbox(frame)
        listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Populate listbox
        for key in self.keys:
            listbox.insert(tk.END, key)
        
        # New key frame
        new_key_frame = ttk.Frame(frame)
        new_key_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(new_key_frame, text="New key:").pack(side=tk.LEFT)
        new_key_var = tk.StringVar()
        entry = ttk.Entry(new_key_frame, textvariable=new_key_var)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Buttons frame
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        def on_select():
            selection = listbox.curselection()
            if selection:
                self.selected_key = self.keys[selection[0]]
                dialog.destroy()
        
        def on_create():
            new_key = new_key_var.get().strip()
            if new_key:
                self.selected_key = new_key
                dialog.destroy()
        
        ttk.Button(button_frame, text="Select", command=on_select).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Create", command=on_create).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Double-click to select
        listbox.bind('<Double-1>', lambda e: on_select())
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return self.selected_key