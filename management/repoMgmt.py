from management.profile import Profile
from management.repository2 import Repository


class RepoMgmt:
    def __init__(self, profile: Profile):
        self.origin = Repository(profile, 'origin')
        self.remote = Repository(profile, 'remote')

    def update(self):
        self.remote.update(self.origin.copyRepo)

    def rollback(self):
        self.remote.rollback(self.origin.copyRepo)

    def start(self):
        self.remote.start()

    def stop(self):
        self.remote.stop()

