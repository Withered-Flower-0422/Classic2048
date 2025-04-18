import os
import sys
from pathlib import Path

base_path = Path(sys._MEIPASS if getattr(sys, "frozen", False) else os.path.curdir)

if __name__ == "__main__":
    print(base_path)
