#!/usr/bin/python

'''
Main program
'''

from controller import Task, Controller

def main():
    c = Controller(1, 8)
    print c
    c.status
    c.receiveTask(Task(0,2))
    c.tick()
    c.receiveTask(Task(2,1))
    c.receiveTask(Task(2,0))
    c.receiveTask(Task(2,3))
    c.receiveTask(Task(2,4))
    c.receiveTask(Task(2,5))
    c.tick()
    c.tick()
    c.tick()
    c.tick()
    c.tick()

if __name__ == '__main__':
    main()
