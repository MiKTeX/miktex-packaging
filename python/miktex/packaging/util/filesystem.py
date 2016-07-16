# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

"""
File system utilities.
"""

import os
import platform
import shutil
import subprocess

def explore_directory(path):
    """Show a directory in Windows Explorer."""
    if platform.system() == "Windows":
        subprocess.call(["explorer", "/e,", "/root,", path])

def remove_directory(dir):
    """Remove a directory.  We need this because the Windows version of  shutil.rmtree() seems to be broken."""
    if platform.system() == "Windows":
        subprocess.call("rmdir /S /Q " + dir, shell=True)
    else:
        shutil.rmtree(dir)

def remove_empty_directories(parent_dir):
    for dirpath, dirnames, filenames in os.walk(parent_dir):
        for dir in dirnames:
            subdir = os.path.join(dirpath, dir)
            try:
                os.removedirs(subdir)
            except:
                pass
