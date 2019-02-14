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

import miktex.packaging.info.texcatalogue
import miktex.packaging.settings.paths
import miktex.packaging.util.filesystem

if len(sys.argv) != 2:
    sys.exit("Usage: " + sys.argv[0] + " <package-name>")

package = sys.argv[1]
directories = []
entry = miktex.packaging.info.texcatalogue.Entry(package)
if entry.ctan_path is not None:
    ctan_dir = os.path.normpath(miktex.packaging.settings.paths.MIKTEX_CTAN_MIRROR + entry.ctan_path)
    if os.path.isdir(ctan_dir):
        directories.append(ctan_dir)
package_dir = miktex.packaging.settings.paths.get_package_dir(package)
if os.path.isdir(package_dir):
    directories.append(package_dir)
if directories:
    miktex.packaging.util.filesystem.explore_directories(directories)
