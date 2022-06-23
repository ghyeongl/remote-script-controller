import os
from zipfile import ZipFile


class CodeUpdater:
    def __init__(self, repo_name: str):
        self.name = repo_name
        self.workspace = "/Users/ghyeong/Spaces/Work/Devs/Lang-Python"
        self.path = f"{self.workspace}/{self.name}"
        self.gitignore = f"{self.path}/.gitignore"
        # self.path = "/srv/dev-disk-by-label-usb/sd/Spaces/Work/Devs/Lang-Python"
        self.fileList = []

    # from local Synced (/srv/dev-disk-by-label-usb/sd/Spaces/Work/Devs/Lang-Python)
    # to Sync folder (/srv/dev-disk-by-label-usb/sd/Sync/rslsync/PI0-Repo/Script_Management/Repository)
    def getFilesList(self, gitignore=True):
        self._scanFiles(self.name)
        print(self.fileList)
        self._ignoreFiles(gitignore)
        print(self.fileList)

    def copyFiles(self):
        with ZipFile('sample2.zip', 'w') as zipObj2:
            for folderName, subFolders, filenames in os.walk(self.path):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    zipObj2.write(filePath, os.path.basename(filePath))

    def _scanFiles(self, folders):
        for i in os.listdir(f"{self.workspace}/{folders}/"):
            if os.path.isdir(f"{self.workspace}/{folders}/{i}/"):
                self._scanFiles(f"{folders}/{i}")
            else:
                self.fileList.append(f"{folders}/{i}")

    def _ignoreFiles(self, gitignore):
        if not os.path.exists(self.gitignore):
            return -1
        files = self.fileList.copy()
        for file in files:
            # .으로 시작하는 파일 제거
            for f in file.split("/"):
                if f.startswith("."):
                    self.fileList.remove(file)
                    break
            else:
                # .gitignore 에 있는 파일 제거
                if gitignore and self._detectIgnore(file):
                    self.fileList.remove(file)

    def _detectIgnore(self, file) -> bool:
        with open(self.gitignore) as ignores:
            for item in ignores:
                item = item.replace("\n", "")
                # 주석일 경우
                if item.startswith("#"):
                    continue
                # 디렉토리를 포함할 경우
                if "/" in item:
                    sepItem = item.rsplit("/", maxsplit=1) #seperatedItem
                    if self._detectDirIgnore(sepItem.pop(0), file):
                        if len(sepItem) == 0 or sepItem[0] == '':
                            return True
                        if self._detectFileIgnore(sepItem[0], file):
                            return True
                # 디렉토리를 포함하지 않을 경우
                else:
                    if self._detectFileIgnore(item, file):
                        return True
        return False

    def _detectDirIgnore(self, item, file):
        if item == '':
            return False
        dirI = item.split("*")
        while '' in dirI:
            dirI.remove('')
        for i in dirI:
            if not (i in file):
                return False
        return True

    def _detectFileIgnore(self, item, file):
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

    def pasteFiles(self):
        pass