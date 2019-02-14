#!/usr/bin/env python3
#
# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

"""
Retrieve FILES.byname and CTAN.sites from CTAN and compare each file to
the previous version.  Finally show the differences (if there are any).
"""

import os
import platform
import shutil
import subprocess
import sys

import miktex.packaging.settings.paths


def _retrieve_file(ctan_rsync_host, file_to_get):
    subprocess.call([miktex.packaging.settings.paths.RSYNC_EXECUTABLE,
                     "-aqz",
                     "--no-perms",
                     "--times",
                     ctan_rsync_host + "::CTAN/" + file_to_get,
                     "."])


def _show_files(files):
    if platform.system() == "Windows":
        for f in files:
            subprocess.Popen(["notepad.exe", f])
    else:
        subprocess.call(["emacs"] + files)


def _compare_to_previous_version(file):
    prev_file = file + ".prev"
    result = None
    if os.path.isfile(prev_file):
        diff_file = file + ".diff.txt"
        diff_output = open(diff_file, "wb")
        subprocess.call([miktex.packaging.settings.paths.DIFF_EXECUTABLE, "-c2", prev_file, file],
                        stdout=diff_output)
        diff_output.close()
        stat_info = os.stat(diff_file)
        if stat_info.st_size > 0:
            if platform.system() == "Windows":
                subprocess.call([miktex.packaging.settings.paths.UNIX2DOS_EXECUTABLE, "-q", diff_file])
            result = diff_file
    shutil.copyfile(file, prev_file)
    return result


if len(sys.argv) != 1:
    sys.exit("Usage: " + sys.argv[0])

_rsync_host = "ftp.dante.de"
_retrieve_file(_rsync_host, "FILES.byname")
_to_be_shown = []
_file = _compare_to_previous_version("FILES.byname")
if _file:
    _to_be_shown.append(_file)
_retrieve_file(_rsync_host, "CTAN.sites")
_file = _compare_to_previous_version("CTAN.sites")
if _file:
    _to_be_shown.append(_file)
if _to_be_shown:
    _show_files(_to_be_shown)
