#!/usr/bin/python

from Queue import PriorityQueue
import collections
from elevator import Elevator
from task import Task

class Controller(object):
    def __init__(self, num_elevator, max_floor):
        self._capacity = num_elevator
        self._maxfl = max_floor
        # initialize all elevators
        self._elevators = {}
        for i in xrange(num_elevator):
            self._elevators[i] = Elevator(i)
        # a priority queue on each floor
        self._task_queue = collections.defaultdict(PriorityQueue)

    @property
    def capacity(self):
        return self._capacity
    
    @property
    def max_floor(self):
        return self._maxfl

    def elevator_status(self, eid):
        return self._elevators[eid].status

    @property
    def status(self):
        print "==== elevator status ===="
        for i in xrange(self.capacity):
            print self.elevator_status(i)

    def __str__(self):
        return "cotroller: %d elevators, %d floors" % \
                (self.capacity, self.max_floor)

    def receiveTask(self, task):
        assert(isinstance(task, Task))
        if task.destination > self.max_floor - 1 or task.destination < 0:
            print "Error: destination out of range"
            exit(0)
        self._task_queue[task.cur_floor].put(task)

    def assignTask(self, elevator):
        assigned = False
        for i in xrange(elevator.cur_floor, -1, -1):
            if not self._task_queue[i].empty():
                task = self._task_queue[i].get()
                elevator.addTask(task)
                assigned = True
                break
        if not assigned:
            for i in xrange(elevator.cur_floor+1, self.max_floor):
                if not self._task_queue[i].empty():             
                    task = self._task_queue[i].get()
                    elevator.addTask(task)
                    assigned = True
                    break
        
    def iter_idle_elevators(self):
        idle_elevators = []
        for i in xrange(self.capacity):
            if self._elevators[i].idle:
                idle_elevators.append(self._elevators[i])
        # sort idle elevators based on their current floor
        idle_elevators.sort(key=lambda x:x.cur_floor)
        for i in xrange(len(idle_elevators)):
            yield idle_elevators[i]

    def iter_working_elevators(self):
        for i in xrange(self.capacity):
            if not self._elevators[i].idle:
                yield self._elevators[i]

    def tick(self):
        # for every working elevator, make a step
        for e in self.iter_working_elevators():
            e.move()
        # for every idle elevator, take assignment,
        # or make towards an assignment
        for e in self.iter_idle_elevators():
            self.assignTask(e)
        self.status

