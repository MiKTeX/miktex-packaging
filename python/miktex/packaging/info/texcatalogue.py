# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

import os
import re
import xml.etree.ElementTree as ElementTree

import miktex.packaging.settings.paths


def get_entry_filename(ctan_package):
    return os.path.normpath(os.path.join(miktex.packaging.settings.paths.MIKTEX_TEX_CATALOGUE,
                                         ctan_package[0],
                                         ctan_package + ".xml"))


def normalize(s):
    s = re.sub("^\s+", "", s)
    s = re.sub("\s+$", "", s)
    s = re.sub("\s\s+", " ", s)
    return s


# Maps MiKTeX package identifiers (key) to CTAN package identifiers (value).
# TODO: read from file
ctan_packages = {
    "cmcyralt": "cmcyralt-ltx",
    "finbib": "finplain",
    "pstricks": "pstricks-base",
    "tools": "latex-tools",
    "ltxbase": "latex-base",
    "cyrillic": "latex-cyrillic",
}

non_free_licenses = {
    "nocommercial",
    "other-nonfree",
    "nosell"
}


class Entry:
    def __init__(self, package_id):
        ctan_package_id = ctan_packages.get(package_id, package_id)
        filename = get_entry_filename(ctan_package_id)
        if os.path.isfile(filename):
            tree = ElementTree.parse(filename)
            ele = tree.find("./name")
            if ele is None:
                self.name = ctan_package_id
            else:
                self.name = normalize(ElementTree.tostring(ele, encoding="unicode", method="text"))
            ele = tree.find("./caption")
            if ele is None:
                self.caption = None
            else:
                self.caption = normalize(ElementTree.tostring(ele, encoding="unicode", method="text"))
            ele = tree.find("./description")
            if ele is None:
                self.description = None
            else:
                self.description = normalize(ElementTree.tostring(ele, encoding="unicode", method="text"))
            ele = tree.find("./copyright")
            if ele is None:
                self.copyright_owner = None
                self.copyright_year = None
            else:
                self.copyright_owner = ele.get("owner")
                self.copyright_year = ele.get("year")
            ele = tree.find("./license")
            if ele is None:
                self.license_type = None
            else:
                self.license_type = ele.get("type")
            ele = tree.find("./version")
            if ele is None:
                self.version_number = None
            else:
                self.version_number = ele.get("number")
            ele = tree.find("./ctan")
            if ele is None:
                self.ctan_path = None
            else:
                self.ctan_path = ele.get("path")
        else:
            self.name = ctan_package_id
            self.caption = None
            self.description = None
            self.copyright_owner = None
            self.copyright_year = None
            self.license_type = None
            self.version_number = None
            self.ctan_path = None

    def is_free(self):
        if self.license_type is None:
            return True
        return self.license_type not in non_free_licenses
