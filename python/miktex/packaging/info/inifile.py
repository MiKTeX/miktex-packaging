# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

import io
import os

from miktex.packaging.info import texcatalogue
from miktex.packaging.settings import paths


def get_ini_filename(package: str) -> str:
    return os.path.normpath(os.path.join(paths.MIKTEX_PACKAGE_STAGING_ROOT, package, "package.ini"))


def get_description_filename(package: str) -> str:
    return os.path.normpath(os.path.join(paths.MIKTEX_PACKAGE_STAGING_ROOT, package, "Description"))


class PackageInfo:
    def __init__(self, package_id: str):
        self.package = package_id
        self.externalname = package_id
        self.name = package_id
        self.title = None
        self.copyright_owner = None
        self.copyright_year = None
        self.version = None
        self.license_type = None
        self.ctan_path = None
        self.md5 = None
        self.description = None
        self.targetsystem = None
        filename = get_ini_filename(package_id)
        if os.path.isfile(filename):
            with io.open(filename, encoding="utf-8") as f:
                for line in f.readlines():
                    pair = line.strip().split("=")
                    if pair[0] == "externalname":
                        self.externalname = pair[1]
                    elif pair[0] == "name":
                        self.name = pair[1]
                    elif pair[0] == "title":
                        self.title = pair[1]
                    elif pair[0] == "copyright_owner":
                        self.copyright_owner = pair[1]
                    elif pair[0] == "copyright_year":
                        self.copyright_year = pair[1]
                    elif pair[0] == "version":
                        self.version = pair[1]
                    elif pair[0] == "license_type":
                        self.license_type = pair[1]
                    elif pair[0] == "ctan_path":
                        self.ctan_path = pair[1]
                    elif pair[0] == "md5":
                        self.md5 = pair[1]
                    elif pair[0] == "targetsystem":
                        self.targetsystem = pair[1]
        filename = get_description_filename(package_id)
        if os.path.isfile(filename):
            with io.open(filename, encoding="utf-8") as f:
                self.description = f.read()

    def write(self):
        lines = []
        if self.externalname:
            lines.append("externalname={}\n".format(self.externalname))
        if self.name:
            lines.append("name={}\n".format(self.name))
        if self.title:
            lines.append("title={}\n".format(self.title))
        if self.copyright_owner:
            lines.append("copyright_owner={}\n".format(self.copyright_owner))
        if self.copyright_year:
            lines.append("copyright_year={}\n".format(self.copyright_year))
        if self.version:
            lines.append("version={}\n".format(self.version))
        if self.license_type:
            lines.append("license_type={}\n".format(self.license_type))
        if self.ctan_path:
            lines.append("ctan_path={}\n".format(self.ctan_path))
        if self.md5:
            lines.append("md5={}\n".format(self.md5))
        if self.targetsystem:
            lines.append("targetsystem={}\n".format(self.targetsystem))
        with io.open(get_ini_filename(self.package), mode="w", encoding="utf-8") as f:
            f.writelines(lines)
        if self.description:
            with io.open(get_description_filename(self.package), mode="w", encoding="utf-8") as f:


def write_ini_file(package_id: str, entry: texcatalogue.Entry, md5_hash: str = None):
    """Write a package information file.

    Args:
        package_id (str): package identifier
        entry (miktex.packaging.info.texcatalogue.Entry): catalogue entry
        md5 (str, optional): MD5 digest. Defaults to None.
    """
    lines = []
    lines.append("externalname={}\n".format(package_id))
    if entry.name:
        lines.append("name={}\n".format(entry.name))
    else:
        lines.append("name={}\n".format(package_id))
    if entry.caption:
        lines.append("title={}\n".format(entry.caption))
    if entry.copyright_owner:
        lines.append("copyright_owner={}\n".format(entry.copyright_owner))
    if entry.copyright_year:
        lines.append("copyright_year={}\n".format(entry.copyright_year))
    if entry.version_number:
        lines.append("version={}\n".format(entry.version_number))
    if entry.license_type:
        lines.append("license_type={}\n".format(entry.license_type))
    if entry.ctan_path:
        lines.append("ctan_path={}\n".format(entry.ctan_path))
    if md5_hash:
        lines.append("md5={}\n".format(md5_hash))
    package_dir = os.path.normpath(os.path.join(
        paths.MIKTEX_PACKAGE_STAGING_ROOT, package_id))
    if not os.path.isdir(package_dir):
        os.mkdir(package_dir)
    with io.open(get_ini_filename(package_id), mode="w", encoding="utf-8") as f:
        f.writelines(lines)
    if entry.description:
        with io.open(get_description_filename(package_id), mode="w", encoding="utf-8") as f:
            f.write(entry.description)
