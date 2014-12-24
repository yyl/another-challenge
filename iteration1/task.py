class Task(object):
    def __init__(self, cur_fl, dest):
        self._cur_fl = cur_fl
        self._dest = dest

    @property
    def destination(self):
        return self._dest

    @property
    def cur_floor(self):
        return self._cur_fl

    def __cmp__(self, other):
        return cmp(self.destination, other.destination)
