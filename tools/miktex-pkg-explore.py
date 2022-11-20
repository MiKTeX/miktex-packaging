#!/usr/bin/env python3
#
# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

"""
For a given package, view the contents of
a) the package staging directory, and
b) the CTAN directory
in two system file viewer windows.
"""

import os
import sys

from miktex.packaging.info import texcatalogue
from miktex.packaging.settings import paths
from miktex.packaging.util import filesystem

if len(sys.argv) != 2:
    sys.exit("Usage: {} <package>".format(sys.argv[0]))

package_id = sys.argv[1]
directories_to_explore = []
entry = texcatalogue.Entry(package_id)
if entry.ctan_path:
    ctan_dir = os.path.normpath(paths.MIKTEX_CTAN_MIRROR + entry.ctan_path)
    if os.path.isdir(ctan_dir):
        directories_to_explore.append(ctan_dir)
package_dir = paths.get_package_dir(package_id)
if os.path.isdir(package_dir):
    directories_to_explore.append(package_dir)
if directories_to_explore:
    filesystem.explore_directories(directories_to_explore)
