# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

import os
import re
import subprocess

from miktex.packaging.settings import paths


def try_get_md5_hash(package_id: str) -> str:
    """Get the MD5 hash of a package.

    Args:
        package_id (str): identifies the package

    Returns:
        str: the MD5 hash or None, if the package directory does not exist.
    """
    texmf_parent = paths.get_texmf_parent_dir(
        package_id)
    if not os.path.isdir(texmf_parent):
        return None
    output = subprocess.getoutput(
        '"{}" "{}" --exclude=.tpm'.format(paths.MD5WALK_EXECUTABLE, texmf_parent))
    return re.sub(r"\s+$", "", output)
