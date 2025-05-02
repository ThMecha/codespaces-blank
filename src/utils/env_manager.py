"""
Utilities for managing environment variables.
"""
import os
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv, set_key

ENV_PATH = ".env"

def load_env_variables() -> Dict[str, str]:
    """
    Load all environment variables from .env file.
    
    Returns:
        Dict[str, str]: Dictionary of environment variables
    """
    if not os.path.exists(ENV_PATH):
        # Create empty .env file if it doesn't exist
        open(ENV_PATH, 'a').close()
    
    load_dotenv(ENV_PATH)
    env_vars = {}
    
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    
    return env_vars

def get_env_keys() -> List[str]:
    """
    Get all keys from .env file.
    
    Returns:
        List[str]: List of environment variable keys
    """
    env_vars = load_env_variables()
    return list(env_vars.keys())

def get_env_value(key: str) -> Optional[str]:
    """
    Get value for a specific key from .env file.
    
    Args:
        key (str): Environment variable key
        
    Returns:
        Optional[str]: Value of the environment variable or None if not found
    """
    env_vars = load_env_variables()
    return env_vars.get(key)

def save_to_env(key: str, value: str) -> None:
    """
    Save a key-value pair to .env file.
    
    Args:
        key (str): Environment variable key
        value (str): Environment variable value
    """
    set_key(ENV_PATH, key, value)

def parse_coords(coords_str: str) -> Tuple[int, int, int, int]:
    """
    Parse coordinates string from .env file.
    
    Args:
        coords_str (str): Coordinates as comma-separated string
        
    Returns:
        Tuple[int, int, int, int]: Tuple of (x1, y1, x2, y2)
    """
    try:
        x1, y1, x2, y2 = map(int, coords_str.split(','))
        return x1, y1, x2, y2
    except (ValueError, AttributeError):
        return 0, 0, 0, 0