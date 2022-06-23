import os.path


class RepoInfo:
    def __init__(self, workspace, repoName):
        self.workspace = workspace
        self.name = repoName
        self.path = f"{self.workspace}/{self.name}"
        self.ignore = self.setIgnore()
        self.special = self.setSpecial()
        # Additional Info
        self.ignoreIgnore = True
        self.ignoreHidden = True
        self.addSpecial = True
        # File list
        self.fileList = []

    def setIgnore(self):
        ignore = f"{self.path}/.gitignore"
        if os.path.exists(ignore):
            return ignore
        else:
            return None

    def setSpecial(self):
        special = f"{self.path}/.smspecial"
        if os.path.exists(special):
            return special
        else:
            return None

    def setAddInfo(self, ignoreStat, hiddenStat):
        self.ignoreIgnore = ignoreStat
        self.ignoreHidden = hiddenStat
