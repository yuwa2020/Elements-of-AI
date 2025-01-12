# a2-release
# Part 1: 
## (1) a description of how you formulated the search problem, including precisely defining the state space, the successor function, the edge weights, the goal state, and (if applicable) the heuristic function(s) you designed, including an argument for why they are admissible;

### State Space
All possible cities in the city data and possible roads from the road data.

### Initial State
Start city. If the start city is not in the city data, find the nearest city in the city data which has a low heuristic value to the end city.

### Successor Function
Find the neighbors of the current city and get information about the road between the current city and the neighbor city (neighbor city, miles, speed limit, road name).

### Edge Weights
Implemented in the `calculate_gx` function:
- If cost = 'segments', the edge weight is the number of segments between the current city and the neighbor city.
- If cost = 'distance', the edge weight is the total miles between the current city and the neighbor city.
- If cost = 'time', the edge weight is the total hours between the current city and the neighbor city.
- If cost = 'delivery', the edge weight is the total expected accidents between the current city and the neighbor city.

### Goal State
End city. If the end city is not in the city data, find the nearest city in the city data which has a low heuristic value to the start city.

### Heuristic Function
Implemented in the `heuristic` function:
- If cost = 'distance', the heuristic value is the haversine distance between two cities.
- If cost = 'time', the heuristic value is the haversine distance between two cities divided by (max_speed_limit + 5).
- If cost = 'segments', the heuristic value is the haversine distance between two cities divided by max_segment_length.
- If cost = 'delivery', the heuristic value is the haversine distance between two cities multiplied by max_speed_limit * 0.000001.
- If the city being searched for is not in the city data, the heuristic value is 0 because the city is not in the city data.

### Admissible Heuristic Function
The heuristic function is admissible because instead of using Manhattan distance, we used haversine distance, which is more accurate because the Earth is a sphere and Manhattan distance is not accurate for this problem.

cost = 'distance'
Using harvestine distance is admissible because it is always less than the actual distance between two cities. This is also consistent heuristic.
cost = 'time'
Using harvestine distance divided by (max_speed_limit + 5) is admissible because max_speed_limit is always less than the actual speed limit. This is also consistent heuristic.
cost = 'segments'
Using harvestine distance divided by max_segment_length is admissible because max_segment_length is always less than the actual segment length. This is also consistent heuristic.
cost = 'delivery'
Using harvestine distance * max_speed_limit * 0.000001 is admissible because max_speed_limit  is always less than the actual speed limit. This is also consistent heuristic.



## (2) a brief description of how your search algorithm works;

The entire algorithm is implemented in the `a_star_search` function.

Start using `heapq` to implement the A* search algorithm.

The `check_start_end_city` function is used to adjust the original start and end cities to the nearest cities in the city data:
- When the start city is not in the city data, the function will find the nearest city in the city data which has a low heuristic value to the end city.
- When the end city is not in the city data, the function will find the nearest city in the city data which has a low heuristic value to the start city.
- When both start and end cities are not in the city data, the function will find the nearest city in the city data which has a low heuristic value to the start city and end city.

The main idea of A* search is used from the following link: (https://www.codecademy.com/resources/docs/ai/search-algorithms/a-star-search).

- The open list is a list of nodes that can be reached.
- The closed list is a set of nodes that have already been explored.
- The algorithm ends when the goal node has been explored
- Use the `find_neighbours` function to find the neighbors of the current city and get information about the road between the current city and the neighbor city (neighbor city, miles, speed limit, road name).
- If the neighbor city is in the city data, use the heuristic function to calculate the heuristic value between the current city and the neighbor city.
- If the neighbor city is not in the city data, the heuristic value is 0 because the city is not in the city data.
- Calculate `f(x) = g(x) + h(x)`, where `g(x)` is the path cost and `h(x)` is the heuristic.
- Push the total cost of the path from the start node to the neighbor node to the open list.

## (3) and discussion of any problems you faced, any assumptions, simplifications, and/or design decisions you made. These comments are especially important if your code does not work as well as you would like, since it is a chance to document the energy and thought you put into your solution. For example, if you tried several different heuristic functions before finding one that worked, feel free to describe this in the report so that we appreciate the work that you did.


For implementing heapq in Python, we referred to the tutorial at Codeacademy(https://www.codecademy.com/resources/docs/ai/search-algorithms/a-star-search ) to understand push and pop operations and applied heappush for A* algorithm implementation.

Distance Calculation

Initially, we considered using Manhattan distance to calculate the distance between cities. However, because city distances are not along a grid but on a spherical surface, we chose the Haversine formula to more accurately compute distances between two points on Earth.



Handling Missing Location Data

- Neighbor Cities: When neighboring cities lacked latitude and longitude data, we set heuristic_cost = 0 and found the nearest city with available data to substitute.
- Start and End Cities: Similarly, if the start or end cities were missing in the dataset, we substituted them with the nearest available cities.



We also Implemented the extra credit function 
The output looks something like this, but since the output formatting is different, the code we uploaded will not show this type of output :


```
singarju@silo:~/a2-release/part1$ python3 ./route.py Hawthorne,_Nevada London,_Kentucky segments
Start in Hawthorne,_Nevada
   Then go to Luning,_Nevada via US_95 for 24 miles
   Then go to Jct_US_95_&_NV_360,_Nevada via US_95 for 18 miles
   Then go to Coaldale,_Nevada via US_95 for 21 miles
   Then go to Tonopah,_Nevada via US_6/95 for 41 miles
   Then go to Beatty,_Nevada via US_95 for 93 miles
   Then go to Amargosa_Valley,_Nevada via US_95 for 29 miles
   Then go to Las_Vegas,_Nevada via US_95 for 87 miles
   Then go to St._George,_Utah via I-15 for 114 miles
   Then go to Fredonia,_Arizona via UT_9_&_UT_59/AZ_399 for 72 miles
   Then go to Jacob_Lake,_Arizona via Alt_US_89 for 32 miles
   Then go to Echo_Cliffs,_Arizona via Alt_US_89 for 55 miles
   Then go to Jct_US_89_&_US_160,_Arizona via US_89 for 42 miles
   Then go to Jeddito,_Arizona via AZ_264 for 103 miles
   Then go to Ganado,_Arizona via AZ_264 for 38 miles
   Then go to Gallup,_New_Mexico via AZ/NM_264 for 44 miles
   Then go to Albuquerque,_New_Mexico via I-40 for 138 miles
   Then go to Clines_Corners,_New_Mexico via I-40 for 59 miles
   Then go to Santa_Rosa,_New_Mexico via I-40 for 55 miles
   Then go to Tucumcari,_New_Mexico via I-40 for 59 miles
   Then go to Vega,_Texas via I-40 for 80 miles
   Then go to Amarillo,_Texas via I-40 for 35 miles
   Then go to Claude,_Texas via US_287 for 28 miles
   Then go to Clarendon,_Texas via US_287 for 30 miles
   Then go to Childress,_Texas via US_287 for 58 miles
   Then go to Vernon,_Texas via US_287 for 59 miles
   Then go to Wichita_Falls,_Texas via US_287 for 51 miles
   Then go to Waurika,_Oklahoma via OK/TX_79 for 37 miles
   Then go to Ardmore,_Oklahoma via US_70 for 50 miles
   Then go to Madill,_Oklahoma via US_70 for 25 miles
   Then go to Durant,_Oklahoma via US_70 for 26 miles
   Then go to Hugo,_Oklahoma via US_70 for 55 miles
   Then go to Idabel,_Oklahoma via US_70 for 44 miles
   Then go to Broken_Bow,_Oklahoma via US_70/259 for 13 miles
   Then go to DeQueen,_Arkansas via US_70 for 24 miles
   Then go to Jct_US_59/71_&_US_70_E,_Arkansas via US_59/70/71 for 8 miles
   Then go to Hot_Springs,_Arkansas via US_70 for 80 miles
   Then go to Ola,_Arkansas via AR_7 for 55 miles
   Then go to Perry,_Arkansas via AR_10 for 26 miles
   Then go to Morrilton,_Arkansas via AR_9 for 9 miles
   Then go to Conway,_Arkansas via I-40 for 20 miles
   Then go to Beebe,_Arkansas via US_64 for 30 miles
   Then go to Bald_Knob,_Arkansas via US_64/67/167 for 28 miles
   Then go to Newport,_Arkansas via US_67 for 30 miles
   Then go to Waldenburg,_Arkansas via AR_14 for 18 miles
   Then go to Jonesboro,_Arkansas via US_49 for 23 miles
   Then go to Paragould,_Arkansas via US_49 for 21 miles
   Then go to Kennett,_Missouri via US_412 for 32 miles
   Then go to Hayti,_Missouri via US_412 for 17 miles
   Then go to Dyersburg,_Tennessee via I-155 for 27 miles
   Then go to Union_City,_Tennessee via US_51 for 33 miles
   Then go to Fulton,_Kentucky via US_45W/51 for 12 miles
   Then go to Mayfield,_Kentucky via Purchase_Parkway for 23 miles
   Then go to Hardin,_Kentucky via KY_80 for 23 miles
   Then go to Aurora,_Kentucky via KY_80 for 9 miles
   Then go to Cadiz,_Kentucky via US_68 for 25 miles
   Then go to Hopkinsville,_Kentucky via US_68 for 16 miles
   Then go to Russellville,_Kentucky via US_68 for 35 miles
   Then go to Bowling_Green,_Kentucky via US_68 for 30 miles
   Then go to Hays,_Kentucky via I-65 for 24 miles
   Then go to Glasgow,_Kentucky via Cumberland_Pkwy for 12 miles
   Then go to Russell_Springs,_Kentucky via Cumberland_Pkwy for 53 miles
   Then go to Somerset,_Kentucky via Cumberland_Pkwy for 27 miles
   Then go to London,_Kentucky via KY_80 for 33 miles

          Total segments:   63
             Total miles: 2518.000
             Total hours:   44.669
Total expected accidents:    0.133
Number of states visited:   11
```


- start_city: The starting city.
    - end_city: The destination city.
    - cities: Dictionary mapping city names to (latitude, longitude).
    - distances: Dictionary of (city1, city2) -> distance values.
    - states: Dictionary mapping city names to state names.
The above were used to implement the statetour function using exploring neighbors and updating the h(x) and cost of g(x)
To be really honest, The cost function was not working really well, it was returning one extra city traveled which was not correct. Such as if we count in the above example, the city visited should return 10 but it is returning 11.
Also we made changes in the driver code, to have ststetour as the cost function.

We handled the case when we found “Jct” as the other cost functions. 

# PART 2:

This code uses the input file to parse and produce a list of groups of students for a group assignment and also the total time required (in minutes) by the course staff to assess the groups and their complaints. This code uses three main steps to calculate the groups and their assignment cost. 1. Parsing the total number of students and their requests, 2. Calculating cost and 3. Initializing and improving the assigned groups.

Search algorithm used: Greedy algorithm. If the next best value is identified, it replaces the current value with the new one.

state space: all possible student group formation in groups of 3

successor function: The next lowest value obtained from the ‘calculate_cost’ function. Detail information is written on 4.  Improving the initial set of groups using the ‘improve_groups’ function:

the edge weights,: The difference in cost between the current arrangement of group and the new arrangement of the groups.

the goal state: an optimal solution with the lowest assignment cost and its group.


heuristic function(s) : The cost function implemented in the ‘calculate_cost’ function is the heuristic function of this code. This function evaluates how ‘good’ or ‘bad’ the particular assignment of groups is.



The following are the steps taken in each functions involved in the code:

1: Parsing the Input using the 'parse_input' function:

- the input consists of strings with 3 spacings.
- the first string represents the name of the student who wants to form the team
- the second string represents the teammates the student wants in their team.
- if there are more than one teammate that the student requests, they are separated by ‘-’.
- if the student wants someone in their team but doesn’t have anyone in mind, they can use ‘zzz’ to represent each student they want in their team.
- the third string represents the name of the students they do not want in their team.
- if there are more than one student that they do not want in their team, the names of the students are separated by ‘,’.
-  if there are none, then it is represented by ‘_’
- based on this the ‘parse_input’ function the code splits the input into 3 different parts.
- for the teammates part, to analyze the total number of requested teammates by the student, it counts the total number of ‘-’ used. 
- for one ‘-’ the requested teammates are considered as 2.
- for two ‘-’ the requested teammates are considered as 3.
- if there are no ‘-’, then the requested teammates are considered as 1.

2. Calculating the cost for every group using ‘calculate_cost’ function:

- The cost is the time taken by the course staff to evaluate all the assignments.
- the cost is calculated by using three different variables: k,m,n
- time taken by the staff to grade each assignment is set to 30 minutes, which is defined by the variable k.
- for each disliked person that got assigned in the same group, raises a complaint to the staff, who then needs to read and respond to that complaint. The time taken is set as 20 minutes and is defined by the variable m.
- for each requested teammate, who did not get assigned to the same team, the student raises a complaint which takes up 10 minutes of the staff time. This is defined by the variable n.
- and also for each student who did not get assigned to the specific number of requested teammates, they require 1 minute each of staff time.
- for each case, a separate loop is used to calculate the total number of costs.
- the ‘calculate_cost’ function will be used for each and every set of groups and their results are added together at the end to provide the total assignment cost.
- the code runs more than one time, in order to find all the possible solutions, so this ‘calculate_cost’ function runs for every set of groups.

3. Creating an initial set of groups using the ‘create_initial_groups’ function:

- this function creates a set of initial groups which can be later improved to find the optimal solution.
- the group is created by sorting all the names in the input file by the ascending order.
- each group is made sure that there are only 3 members in each group.
- a list of groups, consisting of all the student’s names is returned.

4. Improving the initial set of groups using the ‘improve_groups’ function:

- this function swaps the places of all the students' names with other students and calculates the cost for each iteration.
- from the initial set of groups, each student will be swapped with some other student and then the new total cost will be calculated and stored in the variable ‘new_cost’
- if the ‘new_cost’ is lesser than the original cost (stored in variable ‘best_cost’), then the ‘best_cost’ will be replaced with the ‘new_cost’
- this loop continues until no new cost is found. But if we exit now, it may lead to wrong calculation of values.
- we may have found a new cost which is lower, but it may not be the optimal cost.
- to make sure we obtain the optimal value, we make this iteration continue for 50 times.
- we can also use higher values like 500 or even 1000, but then the time taken by the program increases thus increasing the time complexity of the code.
- to ensure an efficient calculation with lower time, we use 50 iterations. We can also find the optimal solution under these 50 iterations.
- we have tested it with various test cases and we have achieved our optimal solution under 50 iterations, so we are not going for anything higher to ensure efficiency of the code.
- after 50 iterations the values of the ‘best_cost’ variable and also their group is returned.

5. Using the ‘solver’ function display the optimal solution:

- the ‘solver’ function initializes values to the variables in the ‘calculate_cost’ cost function in order to calculate the assignment cost.
- also, it yields the initial groups as the first result. This is the quick solution that we obtain at the first loop of the code.
- after this is displayed there is a 10 second delay between the first solution and the optimal solution.
- if the data set is large, it may take longer than 10 seconds. During this 10 second sleep timer, the code runs multiple times in order to receive the optimal solution,
- once the optimal solution is received the code then displays it as the result. 

6. Main script execution:

- it expects the input file as the command-line argument.
- it invokes the solver function in order to produce the latest solution and its cost.




Problems faced during the execution of the code:

Problem 1:

- To initialize the requested number of teammates by each student, we first tried to make the code read the teammates requested by each student and calculate the length of the students.
- this did not work and led to problems where the calculation cost was wrongly calculated and produced an improper result.
- we then changed to calculate the count of ‘-’ in the string to determine the requested team members.

Problem 2:

- we first used a random function in a loop, to calculate all possible values and compared all the values to find the optimal solution.
- this didn't work well and produced a different output every time we ran the code.
- in order to get a consistent result we changed to a method which replaces every student with each other to produce the result. 
