import time
import os
from .repository import Repository
from .codeUpdater import CodeUpdater
from .repoInfo import RepoInfo


class ReposManager:
    def __init__(self, space='Repository'):
        self.reposList = []
        self.workspace = space
        self.initRepos()

    def initRepos(self):
        self._getRepos()
        self._startRepos()

    def updateRepos(self):
        self.stopRepos()
        self._getRepos()
        self._startRepos()

    def _getRepos(self):
        dirList = os.listdir(self.workspace)
        for dirName in dirList:
            path = f"{self.workspace}/{dirName}"
            if dirName.startswith("."):
                continue
            if os.path.isdir(path) and 'main.py' in os.listdir(path):
                repoInfo = RepoInfo(self.workspace, dirName)
                # TODO: add profile parser and save it
                repo = Repository(repoInfo)
                self.reposList.append(repo)

    def _startRepos(self):
        for repo in self.reposList:
            repo.startProcess()

    def stopRepos(self):
        for repo in self.reposList:
            repo.stopProcess()
            self.reposList.remove(repo)

    def copyRepos(self):
        before = time.time()
        for repo in self.reposList:
            updater = CodeUpdater(repo.info)
            updater.getFilesList()
        return round(time.time() - before, 3)
