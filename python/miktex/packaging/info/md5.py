# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

import os
import re
import subprocess

import miktex.packaging.settings.paths


def try_get_md5(package_id):
    texmf_parent = miktex.packaging.settings.paths.get_texmf_parent_dir(package_id)
    if not os.path.isdir(texmf_parent):
        return None
    output = subprocess.getoutput('"{}" "{}" --exclude=.tpm'.format(miktex.packaging.settings.paths.MD5WALK_EXECUTABLE,
                                                                    texmf_parent))
    return re.sub("\s+$", "", output)
