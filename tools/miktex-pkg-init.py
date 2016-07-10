#!/usr/bin/env python3
#
# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

import miktex.packaging.info.inifile
import miktex.packaging.info.md5
import miktex.packaging.info.texcatalogue
import sys

if len(sys.argv) != 2:
    sys.exit("Usage: " + sys.argv[0] + " <package-name>")

package = sys.argv[1]
entry = miktex.packaging.info.texcatalogue.Entry(package)
miktex.packaging.info.inifile.write_ini_file(package, entry, miktex.packaging.info.md5.try_get_md5(package))
