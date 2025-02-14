import json
from management.profile import Profile
from management import paths


class Profiles:
    def __init__(self):
        self.file = paths.profilesF
        self.data = self._getData()
        self.profileList = self._getProfiles()

    def _getProfiles(self):
        profileList = [Profile(name, self.data[name]) for name in self.data]
        return profileList

    def _getData(self):
        with open(self.file) as f:
            data = json.load(f)
        return data
