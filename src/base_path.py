import os
import sys
from pathlib import Path

is_dev_env: bool = not hasattr(sys, "frozen")
base_path = Path(sys._MEIPASS if getattr(sys, "frozen", False) else os.path.curdir)  # type: ignore

if __name__ == "__main__":
    print(base_path)
