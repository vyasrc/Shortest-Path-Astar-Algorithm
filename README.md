# Shortest-Path-Astar-Algorithm

Finding the shortest path in a maze using A* search algorithm , both array and GUI implementations. 

Algorithm :- 

* OPEN // the set of nodes to be evaluated.                                                                                              
* ClOSED // the set of nodes already evaluated.                                                                                          
* add the start node to OPEN                                                                                                              
* loop                                                                                                                         
  * current = node in OPEN with the lowest f_cost
  * remove current from OPEN
  * add current to CLOSED
  * if current is the target node // path has been found
    * return
  * for each neighbor of the current node
    * if neighbor is not traversable or neighbor is in CLOSED
      * skip to the next neighbor
    * if new_path to neighbor is shorter OR neighbor is in OPEN
      * set f_cost of neighbor 
      * set parent of neighbor to current 
      * if neighbor is not in OPEN 
        * add neighbor to OPEN

Array Implementation :-
* Python Library used :- Numpy 

GUI Implementation :-
* Python Libraries used :- Tkinter, Random, Time, Threading

![final ouput](https://github.com/vyasrc/Shortest-Path-Astar-Algorithm/blob/master/Capture.PNG)
