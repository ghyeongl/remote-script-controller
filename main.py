import os, subprocess
import time
import csv
import discord
import multiprocessing


class Repository:
    def __init__(self, path):
        self.path = path
        self.p = None
        self.lock = False

    def startScript(self):
        command = ['python3', 'main.py']
        from subprocess import Popen, PIPE, STDOUT, CalledProcessError
        with Popen(command, cwd=self.path, stdout=PIPE, stderr=STDOUT, text=True) as s:
            appendCsv(self.path, s.pid)
            print(f'[{self.path}] Script started: <pid: {s.pid}>')
            for line in s.stdout:
                print(line, end='')
        if s.returncode != 0:
            raise CalledProcessError(s.returncode, s.args)

    def stopScript(self):
        data = readCsv()
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
                repo = Repository(path)
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


class CmdlineManager:
    class Command:
        def __init__(self, msg):
            self.content = msg.split(' ')

    def __init__(self, reposManager):
        self.reposManager = reposManager
        self.command = None

    def setCommand(self, message):
        self.command = self.Command(message)
        self._provideCommand()

    def _provideCommand(self):
        if self.command.content[0] == '$update':
            if self.command.content[1] == 'repository_list':
                self.reposManager.updateRepos()

        if self.command.content[0] == '$stop':
            if self.command.content[1] == 'all_repository':
                self.reposManager.stopRepos()


def readCsv():
    f = open('data.csv', 'r', encoding='UTF-8')
    rdr = csv.reader(f)
    data = []
    for line in rdr:
        data.append([line[0], line[1]])
    f.close()
    return data


def appendCsv(path, pid):
    f = open('data.csv', 'a', encoding='UTF-8', newline='')
    wr = csv.writer(f)
    wr.writerow([path, pid])
    f.close()


def removeCsv(path, pid):
    data = readCsv()
    data.remove([path, pid])
    f = open('data.csv', 'w', encoding='UTF-8', newline='')
    wr = csv.writer(f)
    for line in data:
        wr.writerow(line)
    f.close()


def writeCsv():
    f = open('data.csv', 'w', encoding='UTF-8', newline='')
    f.close()

def main():
    writeCsv()
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
            cmdlineManager.setCommand(message.content)

    client.run(open('token.txt', 'r').read())


if __name__ == "__main__":
    main()

