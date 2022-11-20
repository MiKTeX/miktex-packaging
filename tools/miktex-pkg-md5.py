#!/usr/bin/env python3
#
# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

import sys

from miktex.packaging.info import inifile
from miktex.packaging.info import md5

if len(sys.argv) != 2 and len(sys.argv) != 3:
    sys.exit("Usage: {} [-update] <package>".format(sys.argv[0]))

if sys.argv[1] == "-update":
    if len(sys.argv) != 3:
        sys.exit("missing package name")
    update_requested = True
    package_id = sys.argv[2]
else:
    if len(sys.argv) != 2:
        sys.exit("invalid argument(s)")
    update_requested = False
    package_id = sys.argv[1]

md5_hash = md5.try_get_md5_hash(package_id)

if update_requested:
    if not md5_hash:
        sys.exit("TDS digest of package '{}' could not be calculated".format(package_id))
    package_info = inifile.PackageInfo(package_id)
    package_info.md5 = md5_hash
    package_info.write()
else:
    print(md5_hash)
