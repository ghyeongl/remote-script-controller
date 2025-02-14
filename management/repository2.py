from .profile import Profile, Info
from .fileMgmt import FileMgmt, FileInfo
from .executer import Executer


class Repository:
    def __init__(self, profile, location):
        self.profile = profile
        self.profile.location = location
        self.fileMgmt = FileMgmt(self.profile)
        self.executer = Executer(self.profile)

    def start(self):
        self.executer.start()

    def stop(self):
        self.executer.stop()

    def copy(self) -> FileInfo:
        return self.fileMgmt.copy()

    def archive(self) -> FileInfo:
        return self.fileMgmt.archive()

    def update(self, new: FileInfo):
        self.fileMgmt.update(new)

    def rollback(self, old: FileInfo):
        self.fileMgmt.rollback(old)
