# Launches the game

import os, sys
from wss.game import main as run_game

# Add the directory containing this file (project root) to sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if __name__ == "__main__":
    run_game()
