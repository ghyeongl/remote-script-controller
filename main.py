import os
import subprocess
import time
import csv
import discord
import multiprocessing
from zipfile import ZipFile


class Repository:
    def __init__(self, workspace, dirName):
        self.path = f"{workspace}/{dirName}"
        self.name = dirName
        self.p = None
        self.lock = False

    def startScript(self):
        command = ['python3', 'main.py']
        from subprocess import Popen, PIPE, STDOUT, CalledProcessError
        with Popen(command, cwd=self.path, stdout=PIPE, stderr=STDOUT, text=True) as s:
            parser.appendCsv(self.path, s.pid)
            print(f'[{self.path}] Script started: <pid: {s.pid}>')
            for line in s.stdout:
                print(line, end='')
        if s.returncode != 0:
            raise CalledProcessError(s.returncode, s.args)

    def stopScript(self):
        data = parser.readCsv()
        for line in data:
            if line[0] == self.path:
                subprocess.run(['kill', '-9', str(line[1])], capture_output=True)
                print(f'[{self.path}] Script terminated: <pid: {line[1]}>')

    def startProcess(self):
        if self.lock:
            print(f'[{self.path}] ProcessAlreadyLocked: {self.p}')
            return
        self.p = multiprocessing.Process(target=self.startScript, args=())
        self.p.start()
        self.lock = True
        print(f'[{self.path}] Process started: {self.p}')

    def stopProcess(self):
        self.stopScript()
        self.p.kill()
        time.sleep(1)
        self.lock = False
        print(f'[{self.path}] Process killed: {self.p}')


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
        for repo in self.reposList:
            updater = CodeUpdater(repo.name)
            updater.getFilesList()



class CmdlineManager:
    class Command:
        def __init__(self, msg):
            self.content = msg.content.split(' ')

    def __init__(self, reposManager):
        self.reposManager = reposManager
        self.command = None
        self.message = None

    async def setCommand(self, message):
        self.command = self.Command(message)
        self.message = message
        await self._provideCommand()

    async def _provideCommand(self):
        if self.command.content[0] == '$update':
            if self.command.content[1] == 'repository_list':
                self.reposManager.updateRepos()
                await self.message.channel.send('All repos are updated.')

            if self.command.content[1] == 'repository_code':
                self.reposManager.copyRepos()

        if self.command.content[0] == '$stop':
            if self.command.content[1] == 'all_repository':
                self.reposManager.stopRepos()
                await self.message.channel.send('All repos are stopped.')


class CsvParser:
    def __init__(self):
        self.filename = 'data.csv'

    def readCsv(self):
        f = open(self.filename, 'r', encoding='UTF-8')
        rdr = csv.reader(f)
        data = []
        for line in rdr:
            data.append([line[0], line[1]])
        f.close()
        return data

    def appendCsv(self, path, pid):
        f = open(self.filename, 'a', encoding='UTF-8', newline='')
        wr = csv.writer(f)
        wr.writerow([path, pid])
        f.close()

    def removeCsv(self, path, pid):
        data = self.readCsv()
        data.remove([path, pid])
        f = open(self.filename, 'w', encoding='UTF-8', newline='')
        wr = csv.writer(f)
        for line in data:
            wr.writerow(line)
        f.close()

    def writeCsv(self):
        f = open(self.filename, 'w', encoding='UTF-8', newline='')
        f.close()


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

            # for file in os.scandir(self.path):
            #     if file ==
        pass

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

            # .gitignore 에 있는 파일 제거
            if gitignore and self._detectIgnore(file):
                self.fileList.remove(file)

    def _detectIgnore(self, file) -> bool:
        with open(self.gitignore) as ignores:
            for item in ignores:
                if item.startswith("#"):
                    continue
                # 디렉토리를 포함할 경우
                if "/" in item:
                    sepItem = item.rsplit("/", maxsplit=1) #seperatedItem
                    dirI = sepItem.pop(0).split("*")
                    # 디렉토리
                    for i in dirI:
                        if not i in file: # 만약 파일에 해당 문법이 없으면 다음 아이템으로 진행
                            break
                    else:
                        if len(sepItem) == 0:
                            return True # 있으면 ignore
                        conI = sepItem.pop(0).split("*")
                        for i in conI:
                            if not i in file:
                                break
                        else:
                            return True
                # 디렉토리를 포함하지 않을 경우
                else:
                    sepItem = item.split("*")
                    for i in sepItem:
                        if not i in file: # 만약 파일에
                            break
                    else:
                        return True
        return False

    def _testIgnore(self):
        pass

    def pasteFiles(self):
        pass


parser = CsvParser()


def main():
    parser.writeCsv()
    print(f'[Script Management] System started: <pid: {os.getpid()}>')
    reposManager = ReposManager('Repository')
    cmdlineManager = CmdlineManager(reposManager)
    client = discord.Client()

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        if message.author.id == 398855441804820480:
            await cmdlineManager.setCommand(message)

    client.run(open('token.txt', 'r').read())


if __name__ == "__main__":
    main()
