another-challenge
=================
### Intro

To execute the program, do `python main.py`. The latest version is in the root dir, and each folder named `iterationX` indicates older versions.

- `main.py`: the main program where it simulates the elevators and controller running
- `elevator.py`: elevator class to represent an elevator
- `controller.py`: controller class to represent the contoller who controls all elevators in the buidling
- `task.py`: represent a person wants to go from current floor to a certain floor in the building

### TODO:
- ~~let elevator take multiple tasks~~
- unify getter and setter
- multi-threaded scheduling?
- find a metric to reflect the efficiency of the elevator
- run simulations to test efficiency
- try different distributions of task arrival
- let each task expire after certain time (people get impatient and decide to walk)

### 2nd iteration
In 2nd, I am gonna make elevators take multiple tasks in each step. 

Assumptions:
- each elevator could take 10 tasks maximum
- initially, each elevator will only take one task
- each elevator will stop at any floor whose queue is not empty along the way, and take tasks in the same direction

Implementations:
- elevator
	- a queue to store tasks (FCFS)
	- a hash table to store piggy backed tasks it picks up along the way
- controller
	- hash table to store elevators `(id, elevator obj)`
	- hash table of `(floor, tasks queue)` to store tasks
	- priority queue to store tasks per floor

Essentially, 2nd version added the support of pigging back tasks along the way if they are a subset of the current task for each elevator. Here by subset I mean the destination of the task is no further than that of current task. 

To accommodate such change, in controller, for every working elevator it checks if theres any valid tasks for them to pick back on during each floor; if so, it adds such task to the elevator.

This is only a **semi**-complete multi-task program, as initially elevator still take into one task. But to complete the feature it is easy, we add a variable to keep track of the maximum distance of all stored tasks in elevator, and change the destination accordingly when takes in new tasks.

### 1st iteration
As mentioned in the challenge description, the key problem is the scheduling problem: to distribute tasks to available elevators. The 1st iteration of my program has two purposes: (1) a version that could work (2) a minimum framework could be extended further. Therefore, I do following assumptions and implementations.

Assumptions:
- each elevator could take one task at a time, and will not take any more task until it finishes the current one
- tasks are grouped by floors, and assigned to elevator that is closest to the floor

Implementations:
- elevator
	- a queue to store tasks (FCFS)
- controller
	- hash table to store elevators `(id, elevator obj)`
	- hash table of `(floor, tasks queue)` to store tasks
	- priority queue to store tasks per floor
	
A task here is defined by `(cur_floor, destination)` pair. Because each elevator could only take one task, we do not have to worry about store and order multiple tasks for each elevator. 

For controller, I setup multiple priority queues for storing and ordering tasks. One obvious choice to keep tasks ordered is queue, which is a FCFS structure. But here I try something different. Priority queue is built for scheduling problems as it could order stored objects in desired manner. I use a priority queue for tasks of each floor. I keep them grouped in each floor so that it is easy to find elevator that is closest to them. Within each floor, I keep tasks based on the distance from current floor to their destinations.

In time-stepping simulation (`tick()`), the controller does two things:

First, it makes all elevators who are running a task move one step, either up or down, given its current destination. For each elevator, after making the step, if it reaches the destination, the controller marks it as idle. Note for each task, it has the floor the person is at, and the destination he/she wants to go. Therefore, for current implementation, the elevator essentially has two destinations to go to deliver one person.

Second, the controller finds all idle elevators, sort them based on their current floor, from lowest to highest. Then, for each elevator, the controller assigns the task that is closest to it. To find the proper task, the controller first check downwards from current floor, find the first floor whose task queue is not empty; then it just assigns the first task in that queue. If no task below, it does the same thing but check upwards until the max floor.

Pro:
- easy to implement: no complex algorithm or data structures. 
- it minimizes the _global_ cost of electricity to reach each task by always looking for the closest elevator for each task. As it sorts all elevators by floor first, the sum of steps all elevators to take to reach tasks should be the minimum. 
- use priority queue instead of queue to store tasks, therefore, controller will deal with the most recent tasks with closest destination first.

Con:
- It is not real. Elevators should be able to take multiple persons along the way. 
- It is also not optimized for efficiency as we did not take into account of destinations of every task when we assign tasks. The worst case is, the priority queue of each floor is sorted based on the distance, therefore a person who wants to go really far might have to wait for a very long time as he/she is in the tail of the queue.