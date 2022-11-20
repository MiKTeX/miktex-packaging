#!/usr/bin/env python3
#
# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

"""
For a given package, update files 'package.ini' and 'Description' in
the staging directory.
"""

import sys

from miktex.packaging.info import inifile
from miktex.packaging.info import md5
from miktex.packaging.info import texcatalogue

if len(sys.argv) != 2:
    sys.exit("Usage: {} <package>".format(sys.argv[0]))

package_id = sys.argv[1]
entry = texcatalogue.Entry(package_id)
inifile.write_ini_file(package_id, entry, md5.try_get_md5_hash(package_id))
