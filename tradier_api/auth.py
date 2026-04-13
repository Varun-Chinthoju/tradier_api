"""Authentication utilities for Tradier API SDK."""

import os
import configparser
from pathlib import Path
from typing import Optional

try:
    import keyring
except ImportError:
    keyring = None

from .exceptions import AuthenticationError

CONFIG_DIR = Path.home() / ".config" / "tradier_api"
CONFIG_FILE = CONFIG_DIR / "config.ini"

def get_api_token() -> str:
    """
    Securely load the Tradier API token.
    Checks the following:
    1. Environment Variable (TRADIER_API_TOKEN)
    2. System Keyring
    3. Local secure config file (~/.config/tradier_api/config.ini)
    
    Returns:
        str: The API token.
    
    Raises:
        AuthenticationError: If the token cannot be found in any secure location.
    """
    # 1. Check environment variable
    token = os.environ.get("TRADIER_API_TOKEN")
    if token:
        return token
        
    # 2. Check system keyring
    if keyring is not None:
        try:
            token = keyring.get_password("tradier_api", "TRADIER_API_TOKEN")
            if token:
                return token
        except Exception:
            pass
            
    # 3. Check config file
    if CONFIG_FILE.exists():
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        if "auth" in config and "token" in config["auth"]:
            return config["auth"]["token"]
            
    raise AuthenticationError("Could not locate TRADIER_API_TOKEN. Set it as an env var, in keyring, or in config.ini")

def set_api_token(token: str, use_keyring: bool = True) -> None:
    """Save token securely."""
    if use_keyring and keyring is not None:
        keyring.set_password("tradier_api", "TRADIER_API_TOKEN", token)
    else:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        config = configparser.ConfigParser()
        config["auth"] = {"token": token}
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        with open(os.open(CONFIG_FILE, flags, 0o600), "w") as f:
            config.write(f)
