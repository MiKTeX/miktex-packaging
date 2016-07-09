import os
import platform
import subprocess
import shutil

def RemoveDirectory(dir):
    if (platform.system() == "Windows"):
        subprocess.call("rmdir /S /Q " + dir, shell=True)
    else:
        shutil.rmtree(dir)

