# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

import miktex.packaging.settings.paths
import os
import re
import subprocess

def try_get_md5(package):
    texmf_parent = miktex.packaging.settings.paths.get_texmf_parent_dir(package)
    if not os.path.isdir(texmf_parent):
        return None
    output = subprocess.getoutput('"' + miktex.packaging.settings.paths.MD5WALK_EXECUTABLE + '" "' + texmf_parent + '" --exclude=.tpm')
    return re.sub("\s+$", "", output)
