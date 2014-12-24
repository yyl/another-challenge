#!/usr/bin/python
import collections
from task import Task

class Elevator(object):
    def __init__(self, eid):
        self._id = eid
        self._cur_floor = 0
        self._destinations = collections.deque()
        self._direction = 0

    @property
    def cur_floor(self):
        return self._cur_floor

    @property
    def idle(self):
        return self._direction == 0
    
    # get the current destination
    @property
    def destination(self):
        if len(self._destinations) == 0:
            return None
        return self._destinations[-1]

    @property
    def status(self):
        return "elevator %d: current floor %d, destination %s" % \
                (self._id, self.cur_floor, self.destination)

    # add a destination to the queue
    def addDestination(self, dest):
        self._destinations.appendleft(dest)
        if self.destination > self._cur_floor:
            self._direction = 1
        else:
            self._direction = -1

    # assign a task
    def addTask(self, task):
        assert(isinstance(task, Task))
        if task.cur_floor != self.cur_floor:
            self.addDestination(task.cur_floor)
        self.addDestination(task.destination)

    def isUp(self):
        return self._direction == 1

    def isDown(self):
        return self._direction == -1

    def hasNext(self):
        return len(self._destinations) > 0
   
    # move elevator by one step
    def move(self):
        # move only if not idle
        if not self.idle:
            if self.isUp():
                self._cur_floor += 1
            else:
                self._cur_floor -= 1
            # check if meet destination
            if self._cur_floor == self._destinations[-1]:
                self._destinations.pop()
                self._direction = 0
                if self.hasNext():
                    if self._destinations[-1] > self._cur_floor:
                        self._direction = 1
                    else:
                        self._direction = -1
