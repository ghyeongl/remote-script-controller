import os.path


class Profile:
    def __init__(self, name, data):
        self.name = name
        self.location = ""
        self.origin = Info(data['origin'], self.name)
        self.remote = Info(data['remote'], self.name)

        self.ignoreIgnore = data['ignoreIgnore']
        self.ignoreHidden = data['ignoreHidden']
        self.addSpecial = data['addSpecial']
        self.doArchive = data['doArchive']

        self.oIgnore = setIgnore(self.origin)
        self.rIgnore = setIgnore(self.remote)
        self.oSpecial = setSpecial(self.origin)
        self.rSpecial = setSpecial(self.remote)
        self.archPath = []


class Info:
    def __init__(self, data, name):
        self.base = data['base']
        self.workspace = data['workspace']
        self.path = f"{self.base}/{self.workspace}/{name}"


def setIgnore(info):
    ignore = f"{info.path}/.gitignore"
    if os.path.exists(ignore):
        return ignore
    else:
        return None


def setSpecial(info):
    special = f"{info.path}/.mgmtspecial"
    if os.path.exists(special):
        return special
    else:
        return None
