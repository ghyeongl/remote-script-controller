import os.path
from management import AbsolutePath


class RepoInfo:
    def __init__(self, workspace, repoName):
        self.workspace = workspace
        self.name = repoName
        self.repoPath = f"{self.workspace}/{self.name}"
        self.aRepoPath = f"{AbsolutePath.curPath}/{self.repoPath}"
        self.originPath = ""
        self.originWorkspace = ""
        self.archPath = []
        self.ignore = self.setIgnore()
        self.special = self.setSpecial()
        # Additional Info
        self.ignoreIgnore = True
        self.ignoreHidden = True
        self.addSpecial = True
        self.doArchive = False
        # File list
        self.fileList = []

    def setIgnore(self):
        ignore = f"{self.originPath}/.gitignore"
        if os.path.exists(ignore):
            return ignore
        else:
            return None

    def setSpecial(self):
        special = f"{self.originPath}/.mgmtspecial"
        if os.path.exists(special):
            return special
        else:
            return None

    def setAddInfo(self, profile):
        self.ignoreIgnore = profile.key("ignoreStat")
        self.ignoreHidden = profile.key("hiddenStat")
        self.doArchive = profile.key("archiveStat")
        self.originPath = profile.key("remotePath")
