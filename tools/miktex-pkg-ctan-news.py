#!/usr/bin/env python3
#
# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

"""
Retrieve FILES.byname and CTAN.sites from CTAN and compare each file to
the previous version.  Finally show the differences (if there are any).
"""

import io
import os
import platform
import shutil
import subprocess
import sys

from miktex.packaging.settings import paths


def _retrieve_file(ctan_rsync_host: str, file_to_get: str):
    subprocess.call([paths.RSYNC_EXECUTABLE,
                     "-aqz",
                     "--no-perms",
                     "--times",
                     "{}::CTAN/{}".format(ctan_rsync_host, file_to_get),
                     "."])


def _show_files(files: list):
    if platform.system() == "Windows":
        for f in files:
            subprocess.Popen(["notepad.exe", f])
    else:
        subprocess.call(["emacs"] + files)


def _compare_to_previous_version(file: str) -> str:
    prev_file = "{}.prev".format(file)
    result = None
    if os.path.isfile(prev_file):
        diff_file = "{}.diff.txt".format(file)
        with io.open(diff_file, mode="w", encoding="utf-8") as diff_output:
            subprocess.call([paths.DIFF_EXECUTABLE, "-c2", prev_file, file],
                            stdout=diff_output)
        stat_info = os.stat(diff_file)
        if stat_info.st_size > 0:
            if platform.system() == "Windows":
                subprocess.call(
                    [paths.UNIX2DOS_EXECUTABLE, "-q", diff_file])
            result = diff_file
    shutil.copyfile(file, prev_file)
    return result


if len(sys.argv) != 1:
    sys.exit("Usage: {}".format(sys.argv[0]))

#_rsync_host = "ftp.dante.de"
_rsync_host = "rsync.dante.ctan.org"
_retrieve_file(_rsync_host, "FILES.byname")
_to_be_shown = []
_diff_output = _compare_to_previous_version("FILES.byname")
if _diff_output:
    _to_be_shown.append(_diff_output)
_retrieve_file(_rsync_host, "CTAN.sites")
_diff_output = _compare_to_previous_version("CTAN.sites")
if _diff_output:
    _to_be_shown.append(_diff_output)
if _to_be_shown:
    _show_files(_to_be_shown)
