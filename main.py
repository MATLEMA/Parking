from utils import *
from GUI import *

if __name__ == "__main__" :

    import subprocess

    # pip install -r requirements.txt sur le terminal
    subprocess.call(['pip', 'install', '-r', 'requirements.txt'])
    
    appli = Main()