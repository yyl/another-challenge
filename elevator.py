#!/usr/bin/python
import collections
from task import Task

class Elevator(object):
    def __init__(self, eid):
        self._id = eid
        self._capacity = 10
        self._size = 0
        self._cur_floor = 0
        self._tasks = collections.defaultdict(list)
        self._destinations = collections.deque()
        self._direction = 0

    @property
    def cur_floor(self):
        return self._cur_floor
    
    @property
    def capacity(self):
        return self._capacity

    @property
    def size(self):
        return self._size

    @property
    def idle(self):
        return self._direction == 0
    
    @property
    def destination(self):
        if len(self._destinations) == 0:
            return None
        return self._destinations[-1]

    @property
    def status(self):
        return "elevator %d: current floor %d, destination %s, %d tasks" % \
                (self._id, self.cur_floor, self.destination, self.size)

    def addDestination(self, dest):
        self._destinations.appendleft(dest)
        if self.destination > self._cur_floor:
            self._direction = 1
        else:
            self._direction = -1

    def addTask(self, task):
        assert(isinstance(task, Task))
        self._tasks[task.destination].append(task)
        self._size += 1
        if self.idle:
            if self.cur_floor != task.cur_floor:
                self.addDestination(task.cur_floor)
            self.addDestination(task.destination)
        print "elevator %d takes %s" % (self._id, task)
   
    # return True if the elevator is full
    def isFull(self):
        return self._size == self._capacity

    def isUp(self):
        return self._direction == 1

    def isDown(self):
        return self._direction == -1

    def hasNext(self):
        return len(self._destinations) > 0
    
    # check if the given task is within the current trip
    def within(self, task):
        if self.isUp():
            return self.cur_floor == task.cur_floor and self.destination >= task.destination
        if self.isDown():
            return self.cur_floor == task.cur_floor and self.destination <= task.destination

    # move elevator by one step
    def move(self):
        # move only if not idle
        if not self.idle:
            if self.isUp():
                self._cur_floor += 1
            else:
                self._cur_floor -= 1
            # release current floor
            arrived = self._tasks.pop(self._cur_floor, None)
            if arrived:
                self._size -= len(arrived)
                print "elevator %d release %d tasks at floor %d" % \
                        (self._id, len(arrived), self.cur_floor)
            # check if meet destination
            if self._cur_floor == self.destination:
                self._destinations.pop()
                self._direction = 0
                if self.hasNext():
                    if self._destinations[-1] > self.cur_floor:
                        self._direction = 1
                    else:
                        self._direction = -1
