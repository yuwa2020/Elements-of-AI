#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: vvaradh-yuhirata-singarju
#
# Based on skeleton code for CSCI-B551 
#


# !/usr/bin/env python3

import sys
import math
from heapq import heappop, heappush

def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c



def parse_city_data(path):
    cities = {}
    with open(path,'r') as data:
        for line in data:
            parts = line.split()
            city_name = parts[0]
            latitude = float(parts[1])
            longitude = float(parts[2])
            cities[city_name] = {'lat': latitude, 'lon': longitude}
    return cities

def max_segment_and_speed(road_data):
    max_speed_limit = -1.0
    max_segment_length = -1.0
    for i, j, distance, speed_limit, k in road_data:
        if(max_speed_limit < int(speed_limit)):
            max_speed_limit = int(speed_limit)
        if(max_segment_length < int(distance)):
            max_segment_length = int(distance)
    
    return max_speed_limit, max_segment_length


def parse_road_data(path):
    roads = []
    with open(path,'r') as data:
        for line in data:
            parts = line.split()
            city1 = parts[0]
            city2 = parts[1]
            distance = int(parts[2])
            speed_limit = int(parts[3])
            highway = parts[4]
            roads.append((city1, city2, distance, speed_limit, highway))
    return roads

def heuristic(lat1, lon1, lat2, lon2, cost, max_speed_limit, max_segment_length):
    """
    Calculate the heuristic value between two cities.
    
    cost = 'distance' : haversine distance between two cities
    cost = 'time' : haversine distance between two cities / (max_speed_limit + 5)
    cost = 'segments' : haversine distance between two cities / max_segment_length
    cost = 'delivery' : haversine distance between two cities * max_speed_limit * 0.000001
    """
    if(cost == 'distance'):
        return haversine(lat1, lon1, lat2, lon2) 
    elif(cost == 'time'):
        return haversine(lat1, lon1, lat2, lon2) / (max_speed_limit+5)
    elif(cost == 'segments'):
        return (haversine(lat1, lon1, lat2, lon2) / max_segment_length)
    elif(cost == 'delivery'):
        return haversine(lat1, lon1, lat2, lon2) * max_speed_limit * 0.000001
    # elif(cost == 'statetour'):
    #     return haversine(lat1, lon1, lat2, lon2)
    else:
        return 0



def find_lat_lon(input_city, cities):
    """
    Find the latitude and longitude of a city.
    """
    if input_city in cities:
        return cities[input_city]['lat'], cities[input_city]['lon']
    else:
        return None, None
    
def find_neighbours(input_city, roads):
    """
    Args:
    input_city: str
    roads: list of tuples

    Returns:
    list of tuples:
    (neighbour_city, miles, max_speed_limit, road_name)
    """
    neighbours = []
    for road_info in roads:
        if road_info[0] == input_city:
            neighbours.append((road_info[1], int(road_info[2]), int(road_info[3]), road_info[4]))
        elif road_info[1] == input_city:
            neighbours.append((road_info[0], int(road_info[2]), int(road_info[3]), road_info[4]))
    return neighbours

def find_specific_road(start_city, end_city, roads):
    """
    Find the road between two cities.
    
    Args:
    start_city: str
    end_city: str
    road_data: list

    Returns:
    tuple
    """
    for road_info in roads:
        if road_info[0] == start_city and road_info[1] == end_city:
            return road_info[2], road_info[3], road_info[4]
        elif road_info[0] == end_city and road_info[1] == start_city:
            return road_info[2], road_info[3], road_info[4]

def if_city_exist(input_city,cities):
    """
    Check if a city is in the city data.
    
    Args:
    input_city: str
    cities: dict

    Returns:
    bool
    """
    if input_city in cities:
        return True
    

def check_start_end_city(start, end, cost, max_speed_limit, max_segment_length, city_data, road_data, original_start, original_end):
    """
    Check if the start and end cities are in the city data.
    If not, find the nearest city in the city data.

    Args:
    start: str
    end: str
    cost: str
    max_speed_limit: float
    max_segment_length: float
    city_data: dict
    road_data: list
    original_start: str
    original_end: str

    Returns:
    list, set
    """

    lat1, lon1 = find_lat_lon(start, city_data)
    lat2, lon2 = find_lat_lon(end, city_data)


    if if_city_exist(start, city_data) == True:
        # both start and end cities are in the city data
        if if_city_exist(end, city_data) == True:
            heuristics_function_value, total_miles, total_hours, total_expected_accidents, route_taken, node = 0, 0, 0, 0, [start], start
        # only end city is not in the city data
        elif if_city_exist(end, city_data) != True:
            original_end = end
            min_heuristic = 100000
            for nearby_end_city, miles, speed_limit, road_name in find_neighbours( end, road_data ):
                if if_city_exist(nearby_end_city, city_data) == True:
                    nearby_end_lat, nearby_end_lan = find_lat_lon(nearby_end_city, city_data)
                    if heuristic(lat1, lon1, nearby_end_lat, nearby_end_lan, cost, max_speed_limit, max_segment_length) < min_heuristic:
                        end = nearby_end_city
                        min_heuristic = heuristic(lat1, lon1, nearby_end_lat, nearby_end_lan, cost, max_speed_limit, max_segment_length)
            heuristics_function_value, total_miles, total_hours, total_expected_accidents, route_taken, node = 0, 0, 0, 0, [start], start

        
    
    # only start city is not in the city data
    # find the start city's nearest city in the city data
    elif if_city_exist(start, city_data) != True:
        if if_city_exist(end, city_data) == True:
            # keep the original start city in the original_start
            original_start = start
            min_heuristic = 100000
            for nearby_start_city, miles, speed_limit, road_name in find_neighbours( start, road_data ):
                if if_city_exist(nearby_start_city, city_data) == True:
                    nearby_start_lat, nearby_start_lan = find_lat_lon(nearby_start_city, city_data)
                    if heuristic(nearby_start_lat, nearby_start_lan, lat2, lon2, cost, max_speed_limit, max_segment_length) < min_heuristic:
                        # replace the start city with the nearest city in the city data
                        start = nearby_start_city
                        road_name_keep = road_name
                        mile_keep = miles
                        speed_limit_keep = speed_limit
                        min_heuristic = heuristic(nearby_start_lat, nearby_start_lan, lat2, lon2, cost, max_speed_limit, max_segment_length)
            

            # add information of the road between the original start city to alternative start city
            heuristics_function_value = 0
            total_miles = mile_keep
            total_hours = mile_keep / (speed_limit_keep + 5)
            total_expected_accidents = mile_keep * speed_limit_keep * 0.000001
            road_info = f"{road_name_keep} for {int(mile_keep)} miles"
            route_taken=  [(start, road_info)]
            node = start
        
        # both start and end cities are not in the city data
        elif if_city_exist(end_city, city_data) != True:
            # keep the original start city in the original_start
            original_start = start
            original_end = end
            nearby_start_cities = []
            nearby_dest_cities = []
            for nearby_start_city, miles, speed_limit, road_name in find_neighbours( start, road_data ):
                if if_city_exist(nearby_start_city, city_data) == True:
                    nearby_start_cities.append(nearby_start_city)
            for nearby_end_city, miles, speed_limit, road_name in find_neighbours( end, road_data ):
                if if_city_exist(nearby_end_city, city_data) == True:
                    nearby_dest_cities.append(nearby_end_city)
            
            min_heuristic = 1000000000
            for nearby_start_city in nearby_start_cities:
                for nearby_end_city in nearby_dest_cities:
                    nearby_start_lat, nearby_start_lon = find_lat_lon(nearby_start_city, city_data)
                    nearby_end_lat, nearby_end_lon = find_lat_lon(nearby_end_city, city_data)
                    if heuristic(nearby_start_lat, nearby_start_lon, nearby_end_lat, nearby_end_lon, cost, max_speed_limit, max_segment_length) < min_heuristic:
                        start = nearby_start_city
                        end = nearby_end_city
                        road_name_keep = road_name
                        mile_keep = miles
                        speed_limit_keep = speed_limit
                        min_heuristic = heuristic(nearby_start_lat, nearby_start_lon, nearby_end_lat, nearby_end_lon, cost, max_speed_limit, max_segment_length)
            # add information of the road between the original start city to alternative start city
            heuristics_function_value = 0
            total_miles = mile_keep
            total_hours = mile_keep / (speed_limit_keep + 5)
            total_expected_accidents = mile_keep * speed_limit_keep * 0.000001
            road_info = f"{road_name_keep} for {int(mile_keep)} miles"
            route_taken=  [(start, road_info)]
            node = start
    
    # calculate the latitude and longitude of the start and end cities after the adjustment
    lat1, lon1 = find_lat_lon(start, city_data)
    lat2, lon2 = find_lat_lon(end, city_data)

    # the open list is a list of nodes that can reachs
    # the closed list is a set of nodes that have already been explored.
    open_list, closed_list = [(heuristics_function_value, total_miles, total_hours, total_expected_accidents, route_taken, node)], set()
        
    return open_list, closed_list, lat1, lon1, lat2, lon2, start, end, original_start, original_end

def adjust_original_start_end_city(original_start, original_end, start, end, total_miles, total_hours, total_expected_accidents, route_taken, city_data, road_data):
    """
    Adjust the original start and end cities to the nearest cities in the city data.
    
    Args:
    original_start: str
    original_end: str
    start: str
    end: str
    total_miles: float
    total_hours: float
    total_expected_accidents: float
    route_taken: list
    city_data: dict
    road_data: list
    
    Returns:
    float, float, float, list
    """

    if original_start == None:
        # both start and end cities are in the city data
        if original_end == None:
            # start_city is not neeeded in the route_taken
            route_taken = route_taken[1:]
        
        elif original_end != None:
            route_taken = route_taken[1:]
            miles, speed_limit, road_name = find_specific_road(end, original_end, road_data)
            total_miles = float(total_miles + miles)
            total_hours = total_hours + miles / (speed_limit + 5)
            total_expected_accidents = total_expected_accidents + miles * speed_limit * 0.000001
            road_info = f"{road_name} for {int(miles)} miles"
            route_taken = route_taken + [(original_end, road_info)]

            

    elif original_start != None:
        # only start city is not in the city data
        if original_end == None:
            # nothing to do here
            a= 0
        elif original_end != None:
            miles, speed_limit, road_name = find_specific_road(end, original_end, road_data)
            total_miles = float(total_miles + miles)
            total_hours = total_hours + miles / (speed_limit + 5)
            total_expected_accidents = total_expected_accidents + miles * speed_limit * 0.000001
            road_info = f"{road_name} for {int(miles)} miles"
            route_taken = route_taken + [(original_end, road_info)]
    
    return total_miles, total_hours, total_expected_accidents, route_taken


        

def calculate_gx(total_miles, total_hours, total_expected_accidents, cost, miles, speed_limit, route_taken):
    """
    Calculate the cost of the path from the start node to the current node in the selected cost function.

    Args:
    total_miles: float
    total_hours: float
    total_expected_accidents: float
    cost: str
    miles: float
    speed_limit: float
    route_taken: list

    Returns:
    float

    """
    if cost == 'segments':
        return len(route_taken) 
    elif cost == 'distance':
        return total_miles + miles
    elif cost == 'time':
        return total_hours + miles / (speed_limit + 5)
    elif cost == 'delivery':
        return total_expected_accidents + miles * speed_limit * 0.000001
    
def calculate_total_cost(gx, heuristic_cost, total_miles, total_hours, total_expected_accidents, miles, speed_limit, road_name, route_taken, neighbor):
    """
    Calculate the total cost of the path from the start node to the neighbor node.

    Args:
    gx: float
    heuristic_cost: float
    total_miles: float
    total_hours: float
    total_expected_accidents: float
    miles: float
    speed_limit: float
    road_name: str
    route_taken: list
    neighbor: str

    Returns:
    float, float, float, float, str, list

    """
    to_neighbor_total_cost = gx + heuristic_cost
    to_neighbor_total_miles = float(total_miles + miles)
    to_neighbor_total_hours = total_hours + miles / (speed_limit + 5)
    to_neighbor_total_expected_accidents = total_expected_accidents + miles * speed_limit * 0.000001
    road_info = f"{road_name} for {int(miles)} miles"
    route = route_taken + [(neighbor, road_info)]

    return to_neighbor_total_cost, to_neighbor_total_miles, to_neighbor_total_hours, to_neighbor_total_expected_accidents, road_info, route




def a_star_search(start, end, cost, max_speed_limit, max_segment_length, city_data, road_data):

    # heuristics_function_value
    # start = stat city
    # end = end city
    # cost = cost function

    original_start = None
    original_end = None

    # check if the start and end cities are in the city data
    open_list, closed_list, lat1, lon1, lat2, lon2, start, end, original_start, original_end= check_start_end_city(start, end, cost, max_speed_limit, max_segment_length, city_data, road_data, original_start, original_end)



    # Main A* search idea from:https://www.codecademy.com/resources/docs/ai/search-algorithms/a-star-search
    while open_list:
        # heuristics_function_value = f(x) = g(x) + h(x)
        # node is the current city
  
        heuristics_function_value, total_miles, total_hours, total_expected_accidents, route_taken, node = heappop(open_list)

        # The algorithm ends when the goal node has been explored, NOT when it is added to the open list.
        if node == end:
            total_miles, total_hours, total_expected_accidents, route_taken = adjust_original_start_end_city(original_start, original_end, start, end, total_miles, total_hours, total_expected_accidents, route_taken, city_data, road_data)
            return total_miles, total_hours, total_expected_accidents, route_taken

        if node in closed_list:
            continue


        closed_list.add(node)

        for neighbor, miles, speed_limit, road_name in find_neighbours(node, road_data):

            if neighbor in closed_list:
                continue
            
            # if the neighbor city is in the city data
            if if_city_exist(neighbor, city_data) == True:
                # f(x) = g(x) + h(x), where g(x) is the path cost and h(x) is the heuristic.
                lat1, lon1 = find_lat_lon(neighbor, city_data)
                heuristic_cost = heuristic(lat1, lon1, lat2, lon2, cost, max_speed_limit, max_segment_length)
            else:
                # if the neighbor city is not in the city data, heuristic_cost = 0
                heuristic_cost = 0

            # caluculate the cost of the path from the start node to the previous node and add the cost of the edge to the neighbor node.
            gx = calculate_gx(total_miles, total_hours, total_expected_accidents, cost, miles, speed_limit, route_taken)

            # Calcualte the total cost of the path from the start node to the neighbor node.
            # to_neighbor_total_cost = g(x) + h(x)
            to_neighbor_total_cost, to_neighbor_total_miles, to_neighbor_total_hours, to_neighbor_total_expected_accidents, road_info, route = calculate_total_cost(gx, heuristic_cost, total_miles, total_hours, total_expected_accidents, miles, speed_limit, road_name, route_taken, neighbor)

            # Note: headpush always return the lowest value
            heappush(open_list, (to_neighbor_total_cost, to_neighbor_total_miles, to_neighbor_total_hours, to_neighbor_total_expected_accidents, route, neighbor))

    return -1  # No path found

    # route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
    #                ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
    #                ("Indianapolis,_Indiana","IN_37 for 7 miles")]

    # total_miles = 51
    # total_hours = 1.07949
    # total_expected_accidents = 1.1364

    # return(route_taken,total_miles,total_hours,total_expected_accidents)


def a_star_statetour(start, end, cost, city_data, road_data):


    states = {}
    
    for city, data in city_data.items():
        state = city.split(',')[-1].strip()
        if state not in ['Alaska', 'Hawaii']: # Exclude Alaska and Hawaii
            states[city] = state

    max_speed_limit, max_segment_length = max_segment_and_speed(road_data)
    
    total_miles, total_hours, total_expected_accidents, route_taken = a_star_search_optional(start, end, cost, max_speed_limit, max_segment_length, city_data, road_data, states)
    print('total_miles', total_miles)
    return 0

def a_star_search_optional(start, end, cost, max_speed_limit, max_segment_length, city_data, road_data, states):
    def get_state(city):
        return states.get(city, "Unknown")

    def get_state(city):
        return states.get(city, "Unknown")
        
    def heuristic1(current_city, end_city, visited_states):
        lat1, lon1 = find_lat_lon(current_city, city_data)
        lat2, lon2 = find_lat_lon(end_city, city_data)
        h = heuristic(lat1, lon1, lat2, lon2, cost, max_speed_limit, max_segment_length)
        state_penalty = 48 - len(visited_states)
        return h + state_penalty * 100 # Adjust the penalty as needed
    
    def calculate_gx_optional(total_miles, total_hours, total_expected_accidents, cost, miles, speed_limit, route_taken,visited_states):

        if cost == 'segments':
            return len(route_taken)
        elif cost == 'distance':
            return total_miles + miles
        elif cost == 'time':
            return total_hours + miles / (speed_limit + 5)
        elif cost == 'delivery':
            return total_expected_accidents + miles * speed_limit * 0.000001
        elif cost == 'statetour':
            return (len(visited_states))




    original_start = start
    original_end = end
    start_state = (start, frozenset([get_state(start)]), 0, [start])
    open_list = [(heuristic1(start, end, start_state[1]), start_state)]
    closed_list = set()



    while open_list:

        _, (node, visited_states, g_cost, route_taken) = heappop(open_list)
        print('node', node)
        print('visited_states', visited_states)
        print('g_cost', g_cost)
        print('route_taken', route_taken)
        
        if node == end and len(visited_states) == 48:
            print('a')
            total_miles, total_hours, total_expected_accidents, final_route = adjust_original_start_end_city(original_start, original_end, start, end, g_cost, g_cost / max_speed_limit, g_cost * max_speed_limit * 0.000001, route_taken, city_data, road_data)
            print('total_miles', total_miles)
            return total_miles, total_hours, total_expected_accidents, final_route


        if (node, visited_states) in closed_list:
            continue


        closed_list.add((node, visited_states))



        for neighbor, miles, speed_limit, road_name in find_neighbours(node, road_data):
            print('neighbor', neighbor)
            print('miles', miles)
            print('speed_limit', speed_limit)
            print('road_name', road_name)

            new_state = states[neighbor]
            new_visited_states = visited_states | {new_state}
            print('new_visited_states', new_visited_states)
            new_g_cost = g_cost + calculate_gx_optional(g_cost, 0, 0, cost, miles, speed_limit, route_taken,visited_states)
            new_route = route_taken + [(neighbor, f"{road_name} for {int(miles)} miles")]



            if (neighbor, new_visited_states) not in closed_list:
                print('a')
                h_cost = heuristic1(neighbor, end, new_visited_states)
                f_cost = new_g_cost + h_cost
                heappush(open_list, (f_cost, (neighbor, new_visited_states, new_g_cost, new_route)))
                print('open_list', open_list)
                

        return -1 # No path found


def get_route(start, end, cost):
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-expected-accidents": a float indicating the expected (average) accidents
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    # Parse city and road data
    city_data = parse_city_data("./city-gps.txt")
    road_data = parse_road_data("./road-segments.txt")

    max_speed_limit, max_segment_length = max_segment_and_speed(road_data)

    if cost != 'statetour':

        total_miles,total_hours,total_expected_accidents, route_taken = a_star_search(start, end, cost, max_speed_limit, max_segment_length, city_data, road_data)
    else:
        total_miles,total_hours,total_expected_accidents, route_taken = a_star_statetour(start, end, cost, city_data, road_data)

    
    total_miles = float(total_miles)

    # route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
    #                ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
    #                ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    
    return {"total-segments" : len(route_taken), 
            "total-miles" : total_miles, 
            "total-hours" : total_hours, 
            "total-expected-accidents" : total_expected_accidents, 
            "route-taken" : route_taken}


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery","statetour"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total expected accidents: %8.3f" % result["total-expected-accidents"])


