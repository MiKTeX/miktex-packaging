#!/usr/bin/env python3
#
# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

"""
Retrieve FILES.byname and CTAN.sites from CTAN and compare each file to
the previous version.  Finally show the differences (if there are any).
"""

import miktex.packaging.settings.paths
import os
import platform
import shutil
import subprocess
import sys

def retrieve_file(ctan_rsync_host, file_to_get):
    subprocess.call([ miktex.packaging.settings.paths.RSYNC_EXECUTABLE,
                      "-aqz",
                      "--no-perms",
                      "--times",
                      ctan_rsync_host + "::CTAN/" + file_to_get,
                      "."])

def show_file(file):
    if platform.system() == "Windows":
        subprocess.Popen([ "notepad.exe", file ])
    else:
        subprocess.call([ "more", file ])

def compare_to_previous_version(file):
    prev_file = file + ".prev"
    if os.path.isfile(prev_file):
        diff_file = file + ".diff.txt"
        diff_output = open(diff_file, "wb")
        subprocess.call([ miktex.packaging.settings.paths.DIFF_EXECUTABLE, "-c2", prev_file, file ],
                        stdout=diff_output)
        diff_output.close()
        statinfo = os.stat(diff_file)
        if statinfo.st_size > 0:
            if platform.system() == "Windows":
                subprocess.call([ miktex.packaging.settings.paths.UNIX2DOS_EXECUTABLE, "-q", diff_file ])
            show_file(diff_file)
    shutil.copyfile(file, prev_file)

if len(sys.argv) != 1:
    sys.exit("Usage: " + sys.argv[0])

rsync_host="ftp.dante.de"
retrieve_file(rsync_host, "FILES.byname")
compare_to_previous_version("FILES.byname")
retrieve_file(rsync_host, "CTAN.sites")
compare_to_previous_version("CTAN.sites")
