#!/usr/bin/env python3
#
# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

import miktex.packaging.info.inifile
import miktex.packaging.info.md5
import miktex.packaging.info.texcatalogue
import miktex.packaging.settings.paths
import miktex.packaging.util.filesystem
import os
import subprocess
import sys

if (len(sys.argv) != 2):
    sys.exit("Usage: " + sys.argv[0] + " <package-name>")

package = sys.argv[1]
entry = miktex.packaging.info.texcatalogue.Entry(package)
if (entry.ctan_path == None):
    sys.exit("package '" + package + "' has no ctan_path")
source_dir = os.path.normpath(miktex.packaging.settings.paths.MIKTEX_CTAN + entry.ctan_path)
if (not os.path.isdir(source_dir)):
    sys.exit("'" + source_dir + "' is not a directory")
dest_dir = os.path.normpath(miktex.packaging.settings.paths.get_texmf_dir(package))
if (os.path.isdir(dest_dir)):
    miktex.packaging.util.filesystem.RemoveDirectory(dest_dir)
tdsutil = [miktex.packaging.settings.paths.TDSUTIL_EXECUTABLE]
tdsutil.append("--source-dir=" + source_dir)
tdsutil.append("--dest-dir=" + dest_dir)
tdsutil.append("--recipe=" + os.path.normpath(miktex.packaging.settings.paths.TDSUTIL_DEFAULT_RECIPE))
package_recipe_file = os.path.normpath(os.path.join(miktex.packaging.settings.paths.TDSUTIL_RECIPE_DIR, package + ".ini"))
if (os.path.isfile(package_recipe_file)):
    tdsutil.append("--recipe=" + package_recipe_file)
tdsutil.append("install")
tdsutil.append(package)
subprocess.call(tdsutil)
miktex.packaging.info.inifile.write_ini_file(package, entry, miktex.packaging.info.md5.try_get_md5(package))
