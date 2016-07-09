#!/usr/bin/env python3
#
# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

import miktex.packaging.info.inifile
import miktex.packaging.info.md5
import sys

if (len(sys.argv) != 2 and len(sys.argv) != 3):
    sys.exit("Usage: " + sys.argv[0] + " [-update] <package-name>")

if (sys.argv[1] == "-update"):
    if (len(sys.argv) != 3):
        sys.exit("missing package name")
    update_requested=True
    package=sys.argv[2]
else:
    if (len(sys.argv) != 2):
        sys.exit("invalid argument(s)")
    update_requested=False
    package=sys.argv[1]

md5 = miktex.packaging.info.md5.try_get_md5(package)

if (update_requested):
    if (md5 == None):
        sys.exit("TDS digest of package '" + package + "' could not be calculated")
    package_info = miktex.packaging.info.inifile.PackageInfo(package)
    package_info.md5 = md5
    package_info.write()
else:
    print(md5)
