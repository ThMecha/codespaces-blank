"""
Main handler for crop tool functionality.
"""

import sys
import os
import keyboard
from typing import Tuple, Optional

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.detection.crop_tool.editor import CropEditor, EnvKeySelector
from src.utils.env_manager import get_env_keys, save_to_env


class CropToolHandler:
    def __init__(self, hotkey: str = "shift+c"):
        """
        Initialize the crop tool handler.
        
        Args:
            hotkey (str): Keyboard hotkey to trigger the crop tool
        """
        self.hotkey = hotkey
        self.editor = CropEditor()
        
    def start_listening(self) -> None:
        """
        Start listening for the keyboard hotkey.
        """
        print(f"Crop Tool: Listening for {self.hotkey} hotkey...")
        keyboard.add_hotkey(self.hotkey, self._on_hotkey_triggered)
        
        # Keep the script running
        keyboard.wait()
        
    def _on_hotkey_triggered(self) -> None:
        """Handle hotkey press event."""
        print(f"Crop Tool: Hotkey {self.hotkey} triggered. Starting editor...")
        
        # Start the editor and get coordinates
        coords = self.editor.start_editor()
        if all(coords):  # Check if valid coordinates were selected
            self._save_coordinates(coords)
    
    def _save_coordinates(self, coords: Tuple[int, int, int, int]) -> None:
        """
        Save coordinates to .env file.
        
        Args:
            coords (Tuple[int, int, int, int]): Selected coordinates (x1, y1, x2, y2)
        """
        # Get existing keys
        env_keys = get_env_keys()
        
        # Show key selector dialog
        selector = EnvKeySelector(env_keys)
        key = selector.show_dialog()
        
        if key:
            # Format coordinates as comma-separated string
            coords_str = ",".join(map(str, coords))
            
            # Save to .env file
            save_to_env(key, coords_str)
            print(f"Crop Tool: Saved coordinates for '{key}': {coords_str}")
        else:
            print("Crop Tool: Operation cancelled.")
    
    @staticmethod
    def select_key() -> Optional[str]:
        """
        Show dialog to select an existing key.
        
        Returns:
            Optional[str]: Selected key or None if cancelled
        """
        env_keys = get_env_keys()
        selector = EnvKeySelector(env_keys)
        return selector.show_dialog()