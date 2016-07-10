# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

import os
import platform
import shutil
import subprocess

def remove_directory(dir):
    if platform.system() == "Windows":
        subprocess.call("rmdir /S /Q " + dir, shell=True)
    else:
        shutil.rmtree(dir)

