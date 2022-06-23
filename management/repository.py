import time
import subprocess
import multiprocessing
from csvParser import CsvParser


class Repository:
    def __init__(self, workspace, dirName, parser):
        self.path = f"{workspace}/{dirName}"
        self.name = dirName
        self.p = None
        self.lock = False
        self.parser = CsvParser()

    def startScript(self):
        command = ['python3', 'main.py']
        from subprocess import Popen, PIPE, STDOUT, CalledProcessError
        with Popen(command, cwd=self.path, stdout=PIPE, stderr=STDOUT, text=True) as s:
            self.parser.appendCsv(self.path, s.pid)
            print(f'[{self.path}] Script started: <pid: {s.pid}>')
            for line in s.stdout:
                print(f"[{self.name}] " + line, end='')
        if s.returncode != 0:
            raise CalledProcessError(s.returncode, s.args)

    def stopScript(self):
        data = self.parser.readCsv()
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
