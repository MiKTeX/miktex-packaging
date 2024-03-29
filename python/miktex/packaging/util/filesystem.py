# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

"""
File system utilities.
"""

import os
import platform
import shutil
import subprocess


def explore_directories(directories: list):
    """Show directories in Windows Explorer or Emacs."""
    if platform.system() == "Windows":
        for d in directories:
            subprocess.call(["explorer", "/e,", "/root,", d])
    else:
        subprocess.call(["emacs"] + directories)


def move_directory(from_path: str, to_path:str):
    """Move a directory."""
    os.makedirs(to_path)
    shutil.move(from_path, to_path)


def remove_directory(path: str):
    """Remove a directory.  We need this because the Windows version of  shutil.rmtree() seems to be broken."""
    if platform.system() == "Windows":
        subprocess.call("rmdir /S /Q " + path, shell=True)
    else:
        shutil.rmtree(path)


def remove_empty_directories(parent_dir: str):
    for dir_path, dir_names, _ in os.walk(parent_dir):
        for d in dir_names:
            subdir = os.path.join(dir_path, d)
            try:
                os.removedirs(subdir)
            except:
                pass
