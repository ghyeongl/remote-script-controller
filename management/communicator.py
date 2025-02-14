import os
import time

from management import paths


class Communicator:
    def __init__(self, identifier):
        self.id = identifier
        self.path = f"{paths.pipe}/{self.id}.txt"
        self.reset()
        if not os.path.exists(self.path):
            raise FileNotFoundError

    def write(self, contents):
        self.reset()
        self.append(contents)

    def append(self, contents):
        fp = open(self.path, 'a')
        fp.write(f"{contents}\n")

    def reset(self):
        fp = open(self.path, 'w')
        fp.close()

    def pop(self):
        self.wait()
        fp = open(self.path, 'r')
        data = fp.read().split('\n')[:-1]
        val = data.pop()
        self.reset()
        for line in data:
            self.append(line)
        return val

    def wait(self):
        fp = open(self.path, 'r')
        while fp.read() == '':
            fp = open(self.path, 'r')
