import subprocess
import sys
import os

main_script = os.path.join(os.path.dirname(__file__), 'bot/Main.py')
subprocess.Popen([sys.executable, main_script])
sys.exit()