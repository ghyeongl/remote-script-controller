import os
import shutil
from datetime import datetime
from zipfile import ZipFile
from .repoInfo import RepoInfo
from management import AbsolutePath


class CodeUpdater:
    def __init__(self, repoInfo: RepoInfo):
        self.info = repoInfo

    def do(self):
        self.getFilesList()
        self.updateRepository()

    def getFilesList(self):
        self.info.fileList = self.scanFiles(self.info.originWorkspace, self.info.name)
        self._ignoreFiles()
        self._addFiles(self.info.originWorkspace)

    def updateRepository(self):
        savePath = self.zipFiles(self.info.originWorkspace, AbsolutePath.Temp)
        archPath = self.zipFiles(self.info.aRepoPath, AbsolutePath.Archive)
        self.info.archPath.append(archPath)

        shutil.rmtree(self.info.aRepoPath)
        self.unzipFiles(savePath, AbsolutePath.Repository)

    def zipFiles(self, fromSpace, toSpace):
        curTime = datetime.now()
        filename = f"{self.info.name}_{curTime.strftime('%y%m%d_%H%M%S')}.zip"
        os.chdir(toSpace)
        with ZipFile(filename, 'x') as zipObj:
            os.chdir(fromSpace)
            for file in self.info.fileList:
                zipObj.write(file)
        os.chdir(AbsolutePath.curPath)
        return f"{toSpace}/{filename}"

    def unzipFiles(self, fromWorks, toPath):
        ZipFile(fromWorks).extractall(toPath)

    def scanFiles(self, where, folders):
        files = []
        curPath = f"{where}/{folders}"
        for i in os.listdir(f"{curPath}"):
            if os.path.isdir(f"{curPath}/{i}"):
                for j in self.scanFiles(where, f"{folders}/{i}"):
                    files.append(j)
            else:
                files.append(f"{folders}/{i}")
        return files

    def _ignoreFiles(self):
        files = self.info.fileList.copy()
        for file in files:
            # .으로 시작하는 파일 제거
            for f in file.split("/"):
                if self.info.ignoreHidden and f.startswith("."):
                    self.info.fileList.remove(file)
                    break
            else:
                # .gitignore 에 있는 파일 제거
                if self.info.ignoreIgnore and detectLists(self.info.ignore, file):
                    self.info.fileList.remove(file)
        print(self.info.fileList)

    def _addFiles(self, where):
        files = self.scanFiles(where, self.info.name)
        for file in files:
            if self.info.addSpecial and detectLists(self.info.special, file):
                if file not in self.info.fileList:
                    self.info.fileList.add(file)
        print(self.info.fileList)


def detectLists(spec, file):
    if spec is None:
        return False
    with open(spec) as ignores:
        for item in ignores:
            item = item.replace("\n", "")
            # 주석일 경우
            if item.startswith("#"):
                continue
            # 디렉토리를 포함할 경우
            if "/" in item:
                sepItem = item.rsplit("/", maxsplit=1) #seperatedItem
                if detectDir(sepItem.pop(0), file):
                    if len(sepItem) == 0 or sepItem[0] == '':
                        return True
                    if detectFile(sepItem[0], file):
                        return True
            # 디렉토리를 포함하지 않을 경우
            else:
                if detectFile(item, file):
                    return True
    return False


def detectDir(item, file):
    if item == '':
        return False
    dirI = item.split("*")
    while '' in dirI:
        dirI.remove('')
    for i in dirI:
        if not (i in file):
            return False
    return True


def detectFile(item, file):
    if item == '':
        return False
    sepItem = item.split("*")
    while '' in sepItem:
        sepItem.remove('')
    if len(sepItem) == 0:
        return False
    for i in sepItem:
        if not (i in file):
            return False
    return True
