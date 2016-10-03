# Licensed to you under the MIT license.  See the LICENSE file in the
# project root for more information.

import miktex.packaging.settings.paths
import os
import re
import sys
import xml.etree.ElementTree as ET

def get_entry_filename(ctan_package):
    return os.path.normpath(os.path.join(miktex.packaging.settings.paths.MIKTEX_TEX_CATALOGUE, ctan_package[0], ctan_package + ".xml"))

def normalize(s):
    s = re.sub("^\s+", "", s)
    s = re.sub("\s+$", "", s)
    s = re.sub("\s\s+", " ", s)
    return s

# Maps MiKTeX package names (key) to CTAN package names (value).
# TODO: read from file
ctan_packages = {
    "cmcyralt": "cmcyralt-ltx",
    "finbib": "finplain",
    "pstricks": "pstricks-base",
    "tools": "latex-tools",
    "ltxbase": "latex-base"
}

non_free_licenses = {
    "nocommercial",
    "other-nonfree",
    "nosell"
}

class Entry:
    def __init__(self, package):
        ctan_package = ctan_packages.get(package, package)
        filename = get_entry_filename(ctan_package)
        if os.path.isfile(filename):
            tree = ET.parse(filename)
            ele = tree.find("./name")
            if ele == None:
                self.name = ctan_package
            else:
                self.name = normalize(ET.tostring(ele, encoding="unicode", method="text"))
            ele = tree.find("./caption");
            if ele == None:
                self.caption = None
            else:
                self.caption = normalize(ET.tostring(ele, encoding="unicode", method="text"))
            ele = tree.find("./description")
            if ele == None:
                self.description = None
            else:
                self.description = normalize(ET.tostring(ele, encoding="unicode", method="text"))
            ele = tree.find("./copyright")
            if ele == None:
                self.copyright_owner = None
                self.copyright_year = None
            else:
                self.copyright_owner = ele.get("owner")
                self.copyright_year = ele.get("year")
            ele = tree.find("./license")
            if ele == None:
                self.license_type = None
            else:
                self.license_type = ele.get("type")
            ele = tree.find("./version")
            if ele == None:
                self.version_number = None
            else:
                self.version_number = ele.get("number")
            ele = tree.find("./ctan")
            if ele == None:
                self.ctan_path = None
            else:
                self.ctan_path = ele.get("path")
        else:
            self.name = ctan_package
            self.caption = None
            self.description = None
            self.copyright_owner = None
            self.copyright_year = None
            self.license_type = None
            self.version_number = None
            self.ctan_path = None

    def is_free(self):
        if self.license_type == None:
            return True
        return not self.license_type in non_free_licenses
