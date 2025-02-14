from management.profiles import Profiles
from management.repoMgmt import RepoMgmt


class ReposMgmt:
    def __init__(self):
        self.profiles = Profiles()
        self.repoMgmtList = self._getRepos()

    def startRepos(self):
        for repo in self.repoMgmtList:
            repo.start()

    def stopRepos(self):
        for repo in self.repoMgmtList:
            repo.stop()

    def updateRepos(self):
        self.stopRepos()
        self.__init__()
        self.startRepos()

    def _getRepos(self):
        repoMgmtList = [RepoMgmt(p) for p in self.profiles.profileList]
        return repoMgmtList
