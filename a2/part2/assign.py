#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: vvaradh-yuhirata-singarju
#
# Based on skeleton code for CSCI-B551
#

import sys
import time

def parse_input(input_file):
    students = {}
    with open(input_file, 'r') as f:
        for line in f:
            parts = line.strip().split(' ', 2)
            username = parts[0]
            teammate_part = parts[1] if len(parts) > 1 else ''
            dislikes_part = parts[2] if len(parts) > 2 else '_'

            # Process teammates and determine request_size
            requested_size = teammate_part.count('-') + 1
            # Strip spaces and filter out empty or 'zzz' entries
            teammates = [t.strip() for t in teammate_part.split('-') if t.strip() and t != 'zzz']

            # Process dislikes
            if dislikes_part.strip() == '_':
                dislikes = []
            else:
                dislikes = [d.strip() for d in dislikes_part.split(',') if d.strip()]

            students[username] = {
                'teammates': teammates,
                'dislikes': dislikes,
                'request_size': requested_size
            }



    return students

def calculate_cost(groups, students, k, n, m):
    total_cost = k * len(groups)
    complaints = 0
    
    # Loop through each student and calculate their specific complaints
    for username, prefs in students.items():
        assigned_group = next((group for group in groups if username in group), None)
        if not assigned_group:
            continue

        requested_size = prefs['request_size']
        actual_size = len(assigned_group)

        # Penalty for size mismatch
        if actual_size != requested_size:
            complaints += 1

        # Penalty for missing requested teammates
        for teammate in prefs['teammates']:
            if teammate != username and teammate not in assigned_group:
                complaints += n

        # Penalty for disliked teammates in the same group
        for dislike in prefs['dislikes']:
            if dislike in assigned_group:
                complaints += m

    total_cost += complaints
    return total_cost


def create_initial_groups(students):
    all_students = sorted(students.keys())
    groups = []
    for i in range(0, len(all_students), 3):
        group = all_students[i:i+3]
        groups.append(group)
    return groups


def improve_groups(groups, students, k, n, m):
    max_no_improvement = 50  # Maximum iterations without improvement
    no_improvement_count = 0  # Counter to track unsuccessful iterations
    best_groups = groups
    best_cost = calculate_cost(groups, students, k, n, m)
    all_results = [(best_groups, best_cost)]  # Store all results for tracking

    while no_improvement_count < max_no_improvement:
        improved = False
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                # Try to swap student from group i with student from group j
                for student_i in groups[i]:
                    for student_j in groups[j]:
                        # Perform swap
                        new_groups = [group.copy() for group in groups]
                        new_groups[i].remove(student_i)
                        new_groups[j].remove(student_j)
                        new_groups[i].append(student_j)
                        new_groups[j].append(student_i)

                        # Calculate cost of the new grouping
                        new_cost = calculate_cost(new_groups, students, k, n, m)
                        
                        # If we find a better solution, store it
                        if new_cost < best_cost:
                            best_cost = new_cost
                            best_groups = new_groups
                            all_results.append((best_groups, best_cost))
                            improved = True
                            no_improvement_count = 0  # Reset the counter as we found improvement
                            break

                    if improved:
                        break
                if improved:
                    break
            if improved:
                break
        
        if not improved:  # If no improvement found in this entire iteration
            no_improvement_count += 1  # Increment the counter of failed attempts

    # Return only the best result with the lowest cost
    return best_groups, best_cost




def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
    - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
    - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    students = parse_input(input_file)
    k, n, m = 30, 10, 20

    # Create initial groups and find the first solution
    initial_groups = create_initial_groups(students)
    first_cost = calculate_cost(initial_groups, students, k, n, m)

    # Yield the first solution
    yield {
        "assigned-groups": ["-".join(group) for group in initial_groups],
        "total-cost": first_cost
    }


    time.sleep(10)
    best_groups, best_cost = improve_groups(initial_groups, students, k, n, m)

    # Yield the best solution after improvement
    yield {
        "assigned-groups": ["-".join(group) for group in best_groups],
        "total-cost": best_cost
    }




if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Error: expected an input filename")

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
