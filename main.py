import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src import menu

if __name__ == "__main__":
    menu.start_menu()