import multiprocessing
import subprocess
import time

from .communicator import Communicator


class Executer:
    def __init__(self, profile):
        self.profile = profile
        self.lock = False
        self.p = None
        self.subPid = None
        self.pipe = Communicator(self.profile.name)

    def start(self) -> bool:
        if self.lock:
            return False
        self.lock = True
        self.p = startProcess(self.profile, self.pipe)
        self.subPid = int(getFromPipe(self.pipe, 'subPid'))

    def stop(self):
        stopProcess(self.p, str(self.subPid))
        self.lock = False


def getFromPipe(pipe, identifier):
    time.sleep(1)
    val = pipe.pop().split('=')
    if val[0] == identifier:
        return val[1]


def startPyScript(profile, pipe):
    cmd = ['python3', 'main.py']
    from subprocess import Popen, PIPE, STDOUT, CalledProcessError
    with Popen(cmd, cwd=profile.remote.path, stdout=PIPE, stderr=STDOUT, text=True) as s:
        pipe.append(f"subPid={s.pid}")
        print(f'[{profile.name}] Script started: (pid: {s.pid})')
        for line in s.stdout:
            print(f"[{profile.name}] " + line, end='')
    if s.returncode != 0:
        raise CalledProcessError(s.returncode, s.args)


def _errOut(profile, stderr):
    for error in stderr:
        print(f"[{profile.name}] \033[31m" + error + "\033[0m", end='')


def startProcess(profile, pipe):
    p = multiprocessing.Process(target=startPyScript, args=(profile, pipe,))
    p.start()
    return p


def stopProcess(p, pid):
    subprocess.run(['kill', '-9', str(pid)], capture_output=True)
    p.kill()
