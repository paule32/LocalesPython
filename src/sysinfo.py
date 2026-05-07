# ---------------------------------------------------------------------------
# File:   sysinfo.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

import ctypes
import os
import platform
import sys
import tempfile

from pathlib import Path

# ---------------------------------------------------------------------------
# sys.argv[0] zeigt auf die gestartete EXE
# ---------------------------------------------------------------------------
def app_dir() -> Path:
    return Path(sys.argv[0]).resolve().parent

class SystemInfo:
    @staticmethod
    def system() -> str:
        return platform.system()
    
    @staticmethod
    def is_windows() -> bool:
        return SystemInfo.system() == "Windows"
    
    @staticmethod
    def is_linux() -> bool:
        return SystemInfo.system() == "Linux"
    
    @staticmethod
    def is_macos() -> bool:
        return SystemInfo.system() == "Darwin"
    
    @staticmethod
    def is_unix_like() -> bool:
        return SystemInfo.is_linux() or SystemInfo.is_macos()
    
    @staticmethod
    def is_64bit() -> bool:
        return sys.maxsize > 2**32
    
    @staticmethod
    def architecture() -> str:
        return platform.architecture()[0]
    
    @staticmethod
    def machine() -> str:
        return platform.machine()
    
    @staticmethod
    def python_version() -> str:
        return platform.python_version()
    
    @staticmethod
    def is_admin() -> bool:
        try:
            if SystemInfo.is_windows():
                return bool(ctypes.windll.shell32.IsUserAnAdmin())
            return os.geteuid() == 0
        except Exception:
            return False
    
    @staticmethod
    def home_dir() -> Path:
        return Path.home()
    
    @staticmethod
    def temp_dir() -> Path:
        return Path(tempfile.gettempdir())
    
    @staticmethod
    def app_data_dir(app_name: str = "MyApp") -> Path:
        if SystemInfo.is_windows():
            base = os.environ.get("APPDATA", str(SystemInfo.home_dir() / "AppData" / "Roaming"))
            return Path(base) / app_name
        
        if SystemInfo.is_macos():
            return SystemInfo.home_dir() / "Library" / "Application Support" / app_name
        
        base = os.environ.get("XDG_CONFIG_HOME", str(SystemInfo.home_dir() / ".config"))
        return Path(base) / app_name
    
    @staticmethod
    def documents_dir() -> Path:
        return SystemInfo.home_dir() / "Documents"
    
    @staticmethod
    def desktop_dir() -> Path:
        return SystemInfo.home_dir() / "Desktop"
    
    @staticmethod
    def downloads_dir() -> Path:
        return SystemInfo.home_dir() / "Downloads"
    
    @staticmethod
    def output_dir(language: str, app_name: str = "dBase2Many") -> Path:
        path = SystemInfo.app_data_dir(app_name) / "output" / language.lower()
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def executable_extension() -> str:
        return ".exe" if SystemInfo.is_windows() else ""
    
    @staticmethod
    def script_extension() -> str:
        return ".bat" if SystemInfo.is_windows() else ".sh"
    
    @staticmethod
    def null_device() -> str:
        return "NUL" if SystemInfo.is_windows() else "/dev/null"
    
    @staticmethod
    def summary() -> dict:
        return {
            "system"        : SystemInfo.system(),
            
            "is_windows"    : SystemInfo.is_windows(),
            "is_linux"      : SystemInfo.is_linux(),
            "is_macos"      : SystemInfo.is_macos(),
            "is_unix_like"  : SystemInfo.is_unix_like(),
            
            "is_64bit"      : SystemInfo.is_64bit(),
            "architecture"  : SystemInfo.architecture(),
            "machine"       : SystemInfo.machine(),
            
            "python_version": SystemInfo.python_version(),
            "is_admin"      : SystemInfo.is_admin(),
            
            "home_dir"      : str(SystemInfo.home_dir()),
            "temp_dir"      : str(SystemInfo.temp_dir()),
        }

if __name__ == "__main__":
    from pprint import pprint
    pprint(SystemInfo.summary())
