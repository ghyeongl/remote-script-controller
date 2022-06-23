import time


class ReposManager:
    def __init__(self, space):
        self.reposList = []
        self.workspace = space
        self._getRepos()
        self._startRepos()

    def _getRepos(self):
        dirList = os.listdir(self.workspace)
        for dirName in dirList:
            path = f"{self.workspace}/{dirName}"
            if os.path.isdir(path) and 'main.py' in os.listdir(path):
                repo = Repository(self.workspace, dirName)
                self.reposList.append(repo)

    def _startRepos(self):
        for repo in self.reposList:
            repo.startProcess()

    def stopRepos(self):
        for repo in self.reposList:
            repo.stopProcess()
            self.reposList.remove(repo)

    def updateRepos(self):
        self.stopRepos()
        self._getRepos()
        self._startRepos()

    def copyRepos(self):
        before = time.time()
        for repo in self.reposList:
            updater = CodeUpdater(repo.name)
            updater.getFilesList()
        return round(time.time() - before, 3)