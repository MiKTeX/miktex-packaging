#!/usr/bin/env python3
#
# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

import os
import subprocess
import sys

from miktex.packaging.info import inifile
from miktex.packaging.info import md5
from miktex.packaging.info import texcatalogue
from miktex.packaging.settings import paths
from miktex.packaging.util import filesystem

# TODO: read from file
broken_tds_zip_files = [
    "cstypo"
]

special_tds_zip_files = {
    "babel": "/install/macros/latex/required/babel-base.tds.zip",
    "latex-amsmath-dev": "/install/macros/latex-dev/required/latex-amsmath-dev.tds.zip",
    "latex-base-dev": "/install/macros/latex-dev/latex-base-dev.tds.zip",
    "latex-firstaid": "/install/macros/latex/required/latex-firstaid.tds.zip",
    "latex-firstaid-dev": "/install/macros/latex-dev/required/latex-firstaid-dev.tds.zip",
    "latex-graphics-dev": "/install/macros/latex-dev/required/latex-graphics-dev.tds.zip",
    "latex-tools-dev": "/install/macros/latex-dev/required/latex-tools-dev.tds.zip",
    "ltxbase": "/install/macros/latex/latex-base.tds.zip",
    "pgf": "/install/graphics/pgf/base/pgf.tds.zip",
    "tools": "/install/macros/latex/required/latex-tools.tds.zip",
}


def unpack_tds_zip_file(tds_zip_file: str, dst_dir: str):
    print("unpacking {} to {}".format(tds_zip_file, dst_dir))
    os.makedirs(dst_dir)
    subprocess.call([paths.UNZIP_EXECUTABLE, "-o",
                     "-qq", tds_zip_file, "-d", dst_dir])


def run_tdsutil(package_id: str, source: str, dst_dir: str):
    default_recipe_file = os.path.normpath(paths.TDSUTIL_DEFAULT_RECIPE)
    tdsutil = [
        paths.TDSUTIL_EXECUTABLE,
        "--dest-dir={}".format(dst_dir),
        "--recipe={}".format(default_recipe_file),
        "--source={}".format(source),
        "--verbose",
    ]
    package_recipe_file = os.path.normpath(os.path.join(
        paths.TDSUTIL_RECIPE_DIR, "{}.ini".format(package_id)))
    if os.path.isfile(package_recipe_file):
        tdsutil.append("--recipe={}".format(package_recipe_file))
    tdsutil.append("install")
    tdsutil.append(package_id)
    subprocess.call(tdsutil)


def archive_source_files(package_id: str, dst_dir: str):
    source_file_dir = os.path.normpath(os.path.join(dst_dir, "source"))
    if not os.path.isdir(source_file_dir):
        return
    for suffix in [".cab", ".tar.bz2", ".tar.xz"]:
        to_be_removed = os.path.join(
            source_file_dir, package_id + "-src" + suffix)
        if os.path.isfile(to_be_removed):
            os.remove(to_be_removed)
    subprocess.call("{} -cJf {}-src.tar.xz *".format(paths.TAR_EXECUTABLE,
                                                     package_id), cwd=source_file_dir, shell=True)
    sub_dirs = []
    for entry in os.scandir(source_file_dir):
        if entry.is_dir():
            sub_dirs.append(entry.path)
    for subdir in sub_dirs:
        filesystem.remove_directory(subdir)


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: {} <package>".format(sys.argv[0]))
    package_id = sys.argv[1]
    entry = texcatalogue.Entry(package_id)
    if not entry.is_free():
        sys.exit("package '{}' has a license issue".format(package_id))
    if not entry.ctan_path:
        sys.exit("package '{}' has no ctan_path".format(package_id))
    source = os.path.normpath(paths.MIKTEX_CTAN_MIRROR + entry.ctan_path)
    if not (os.path.isfile(source) or os.path.isdir(source)):
        sys.exit("'{}' is neither a file or a directory".format(source))
    dst_dir = os.path.normpath(paths.get_texmf_dir(package_id))
    if os.path.isdir(dst_dir):
        filesystem.remove_directory(dst_dir)
    special_tds_zip_file = special_tds_zip_files.get(package_id, None)
    if special_tds_zip_file:
        tds_zip_file = os.path.normpath(
            paths.MIKTEX_CTAN_MIRROR + special_tds_zip_file)
    else:
        tds_zip_file = os.path.normpath(
            "{}/install{}.tds.zip".format(paths.MIKTEX_CTAN_MIRROR, entry.ctan_path))
    if os.path.isfile(tds_zip_file) and package_id not in broken_tds_zip_files:
        unpack_tds_zip_file(tds_zip_file, dst_dir)
    else:
        run_tdsutil(package_id, source, dst_dir)
    filesystem.remove_empty_directories(dst_dir)
    archive_source_files(package_id, dst_dir)
    inifile.write_ini_file(package_id, entry, md5.try_get_md5_hash(package_id))


if __name__ == "__main__":
    main()
