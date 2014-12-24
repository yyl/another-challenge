#!/usr/bin/python

'''
Main program
'''

from controller import Task, Controller

def main():
    c = Controller(2, 8)
    print c
    c.status
    c.receiveTask(Task(1,3))
    c.receiveTask(Task(5,3))
    c.tick()
    c.receiveTask(Task(1,0))
    c.receiveTask(Task(0,4))
    c.tick()
    c.tick()
    c.tick()
    c.tick()
    c.tick()
    c.tick()
    c.tick()
    c.tick()
    c.tick()
    c.tick()
    c.tick()
    c.tick()
    c.tick()

if __name__ == '__main__':
    main()
