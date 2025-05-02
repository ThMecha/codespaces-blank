#!/usr/bin/env python3
"""
Main entry point for the crop tool application.
"""

import os
import sys
import argparse
from src.detection.crop_tool.handler import CropToolHandler

def main():
    """Main entry point for the crop tool."""
    parser = argparse.ArgumentParser(
        description='Screen region selection and crop tool.'
    )
    
    parser.add_argument(
        '--hotkey', 
        default='shift+c',
        help='Hotkey to trigger the crop tool (default: shift+c)'
    )
    
    parser.add_argument(
        '--select-only', 
        action='store_true',
        help='Only show the selection dialog without capturing screen regions'
    )
    
    args = parser.parse_args()
    
    if args.select_only:
        # Just show the selection dialog
        selected_key = CropToolHandler.select_key()
        if selected_key:
            print(f"Selected key: {selected_key}")
        else:
            print("No key selected or operation cancelled.")
    else:
        # Start the crop tool with the specified hotkey
        handler = CropToolHandler(hotkey=args.hotkey)
        
        print(f"Starting crop tool with hotkey: {args.hotkey}")
        print("Press Ctrl+C to exit")
        
        try:
            handler.start_listening()
        except KeyboardInterrupt:
            print("\nCrop tool terminated.")
        except Exception as e:
            print(f"Error: {e}")
            return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())