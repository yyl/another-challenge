#!/usr/bin/python

'''
Main program
'''

from controller import Task, Controller

def main():
    c = Controller(2, 8)
    print c
    c.status
    c.receiveTask(Task(0,2))
    c.receiveTask(Task(0,5))
    c.receiveTask(Task(4,5))
    c.tick()
    c.receiveTask(Task(1,2))
    c.tick()
    c.receiveTask(Task(5,1))
    c.tick()
    c.tick()
    c.tick()
    c.tick()

if __name__ == '__main__':
    main()
