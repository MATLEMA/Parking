import subprocess

subprocess.call(['pip', 'install', '-r', 'requirements.txt'])

if __name__ == "__main__" :

    from body_objet import Main

    appli = Main()