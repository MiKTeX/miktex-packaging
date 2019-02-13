#!/usr/bin/env python3
#
# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

import os
import subprocess
import sys

import miktex.packaging.info.inifile
import miktex.packaging.info.md5
import miktex.packaging.info.texcatalogue
import miktex.packaging.settings.paths
import miktex.packaging.util.filesystem

# TODO: read from file
broken_tds_zip_files = [
  "cstypo"
]

special_tds_zip_files = {
    "babel": "/install/macros/latex/required/babel-base.tds.zip",
    "ltxbase": "/install/macros/latex/latex-base.tds.zip",
    "pgf": "/install/graphics/pgf/base/pgf.tds.zip",
    "tools": "/install/macros/latex/required/latex-tools.tds.zip"
}


def unpack_tds_zip_file(tds_zip_file, dst_dir):
    print("unpacking " + tds_zip_file + " to " + dst_dir)
    os.makedirs(dst_dir)
    subprocess.call([miktex.packaging.settings.paths.UNZIP_EXECUTABLE, "-qq", tds_zip_file, "-d", dst_dir])


def run_tdsutil(package, source, dst_dir):
    tdsutil = [miktex.packaging.settings.paths.TDSUTIL_EXECUTABLE,
               "--verbose",
               "--source=" + source,
               "--dest-dir=" + dst_dir,
               "--recipe=" + os.path.normpath(miktex.packaging.settings.paths.TDSUTIL_DEFAULT_RECIPE)]
    package_recipe_file = os.path.normpath(os.path.join(miktex.packaging.settings.paths.TDSUTIL_RECIPE_DIR,
                                                        package + ".ini"))
    if os.path.isfile(package_recipe_file):
        tdsutil.append("--recipe=" + package_recipe_file)
    tdsutil.append("install")
    tdsutil.append(package)
    subprocess.call(tdsutil)


def archive_source_files(package, dst_dir):
    source_file_dir = os.path.normpath(os.path.join(dst_dir, "source"))
    if not os.path.isdir(source_file_dir):
        return
    for suffix in [".cab", ".tar.bz2", ".tar.xz"]:
        to_be_removed = os.path.join(source_file_dir, package + "-src" + suffix)
        if os.path.isfile(to_be_removed):
            os.remove(to_be_removed)
    subprocess.call("{} -cJf {}-src.tar.xz *".format(miktex.packaging.settings.paths.TAR_EXECUTABLE, package),
                    cwd=source_file_dir,
                    shell=True)
    sub_dirs = []
    for entry in os.scandir(source_file_dir):
        if entry.is_dir():
            sub_dirs.append(entry.path)
    for subdir in sub_dirs:
        miktex.packaging.util.filesystem.remove_directory(subdir)


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: " + sys.argv[0] + " <package-name>")

    package = sys.argv[1]
    entry = miktex.packaging.info.texcatalogue.Entry(package)
    if not entry.is_free():
        sys.exit("package '" + package + "' has a license issue")
    if entry.ctan_path is None:
        sys.exit("package '" + package + "' has no ctan_path")
    source = os.path.normpath(miktex.packaging.settings.paths.MIKTEX_CTAN_MIRROR + entry.ctan_path)
    if not (os.path.isfile(source) or os.path.isdir(source)):
        sys.exit("'" + source + "' is not a file or directory")
    dst_dir = os.path.normpath(miktex.packaging.settings.paths.get_texmf_dir(package))
    if os.path.isdir(dst_dir):
        miktex.packaging.util.filesystem.remove_directory(dst_dir)
    special_tds_zip_file = special_tds_zip_files.get(package, None)
    if special_tds_zip_file is None:
        tds_zip_file = os.path.normpath('{}/install{}.tds.zip'.format(miktex.packaging.settings.paths.MIKTEX_CTAN_MIRROR,
                                                                      entry.ctan_path))
    else:
        tds_zip_file = os.path.normpath(miktex.packaging.settings.paths.MIKTEX_CTAN_MIRROR + special_tds_zip_file)
    if os.path.isfile(tds_zip_file) and package not in broken_tds_zip_files:
        unpack_tds_zip_file(tds_zip_file, dst_dir)
    else:
        run_tdsutil(package, source, dst_dir)
    miktex.packaging.util.filesystem.remove_empty_directories(dst_dir)
    archive_source_files(package, dst_dir)
    miktex.packaging.info.inifile.write_ini_file(package, entry, miktex.packaging.info.md5.try_get_md5(package))


if __name__ == "__main__":
    main()
