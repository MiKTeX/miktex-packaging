# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

import codecs
import os

import miktex.packaging.info.texcatalogue
import miktex.packaging.settings.paths


def get_ini_filename(package):
    return os.path.normpath(os.path.join(miktex.packaging.settings.paths.MIKTEX_PACKAGE_ROOT, package, "package.ini"))


def get_description_filename(package):
    return os.path.normpath(os.path.join(miktex.packaging.settings.paths.MIKTEX_PACKAGE_ROOT, package, "Description"))


class PackageInfo:
    def __init__(self, package):
        self.package = package
        self.externalname = package
        self.name = package
        self.title = None
        self.copyright_owner = None
        self.copyright_year = None
        self.version = None
        self.license_type = None
        self.ctan_path = None
        self.md5 = None
        self.description = None
        self.targetsystem = None
        filename = get_ini_filename(package)
        if os.path.isfile(filename):
            f = codecs.open(filename, "r", "utf-8")
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
            f.close()
        filename = get_description_filename(package)
        if os.path.isfile(filename):
            f = codecs.open(filename, "r", "utf-8")
            self.description = f.read()

    def write(self):
        f = codecs.open(get_ini_filename(self.package), "w", "utf-8")
        if self.externalname is not None:
            f.write("externalname=" + self.externalname + "\n")
        if self.name is not None:
            f.write("name=" + self.name + "\n")
        if self.title is not None:
            f.write("title=" + self.title + "\n")
        if self.copyright_owner is not None:
            f.write("copyright_owner=" + self.copyright_owner + "\n")
        if self.copyright_year is not None:
            f.write("copyright_year=" + self.copyright_year + "\n")
        if self.version is not None:
            f.write("version=" + self.version + "\n")
        if self.license_type is not None:
            f.write("license_type=" + self.license_type + "\n")
        if self.ctan_path:
            f.write("ctan_path=" + self.ctan_path + "\n")
        if self.md5 is not None:
            f.write("md5=" + self.md5 + "\n")
        if self.targetsystem is not None:
            f.write("targetsystem=" + self.targetsystem + "\n")
        f.close()
        if self.description is not None:
            f = codecs.open(get_description_filename(self.package), "w", "utf-8")
            f.write(self.description)
            f.close()


def write_ini_file(package, entry, md5=None):
    package_dir = os.path.normpath(os.path.join(miktex.packaging.settings.paths.MIKTEX_PACKAGE_ROOT, package))
    if not os.path.isdir(package_dir):
        os.mkdir(package_dir)
    f = codecs.open(get_ini_filename(package), "w", "utf-8")
    f.write("externalname=" + package + "\n")
    if entry.name is None:
        f.write("name=" + package + "\n")
    else:
        f.write("name=" + entry.name + "\n")
    if entry.caption is not None:
        f.write("title=" + entry.caption + "\n")
    if entry.copyright_owner is not None:
        f.write("copyright_owner=" + entry.copyright_owner + "\n")
    if entry.copyright_year is not None:
        f.write("copyright_year=" + entry.copyright_year + "\n")
    if entry.version_number is not None:
        f.write("version=" + entry.version_number + "\n")
    if entry.license_type is not None:
        f.write("license_type=" + entry.license_type + "\n")
    if entry.ctan_path is not None:
        f.write("ctan_path=" + entry.ctan_path + "\n")
    if md5 is not None:
        f.write("md5=" + md5 + "\n")
    f.close()
    if entry.description is not None:
        f = codecs.open(get_description_filename(package), "w", "utf-8")
        f.write(entry.description)
        f.close()
