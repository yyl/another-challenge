another-challenge
=================

### TODO:
- let elevator take multiple tasks
- find a metric to reflect the efficiency of the elevator
- run simulations to test efficiency
- try different distributions of task arrival
- let each task expire after certain time (people get impatient and decide to walk)


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

For controller, I setup multiple priority queues for storing and ordering tasks. Priority queue is built for scheduling problems as it could order stored objects in desired manner. I keep them grouped in each floor so that it is easy to find elevator that is closest to them. Within each floor, I keep tasks based on the distance from current floor to their destinations. 

In time-stepping simulation (`tick()`), the controller does two things:

First, it makes all elevators who are running a task move one step, either up or down, given its current destination. For each elevator, after making the step, if it reaches the destination, the controller marks it as idle. Note for each task, it has the floor the person is at, and the destination he/she wants to go. Therefore, for current implementation, the elevator essentially has two destinations to go to deliver one person.

Second, the controller finds all idle elevators, sort them based on their current floor, from lowest to highest. Then, for each elevator, the controller assigns the task that is closest to it. To find the proper task, the controller first check downwards from current floor, find the first floor whose task queue is not empty; then it just assigns the first task in that queue. If no task below, it does the same thing but check upwards until the max floor.

Pro:
First, it is easy to implement: no complex algorithm or data structures. Second, it minimizes the _global_ cost of electricity to reach each task by always looking for the closest elevator for each task. As it sorts all elevators by floor first, the sum of steps all elevators to take to reach tasks should be the minimum.

Con:
It is not real. Elevators should be able to take multiple persons along the way. It is also not optimized for efficiency as we did not take into account of destinations of every task when we assign tasks.