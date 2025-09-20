from builtins import set
import os
import sys
from enum import Enum
import random
import time


class SortCriteria(Enum):
    EARLY_START = 0
    DISTANCE = 1

class Vehicle:
    def __init__(self):
        pass

class Ride:
    def __init__(self, startX, startY, endX, endY, early_start, latest, original_index, grid_rows, grid_cols):
        self.start = (startX, startY)
        self.startX = startX
        self.startY = startY
        self.end = (endX, endY)
        self.endX = endX
        self.endY = endY
        self.early_start = early_start
        self.latest_finish = latest
        self.original_index = original_index
        self.distance = abs(startX - endX) + abs(startY - endY)
        self.start_region = get_16region(startX, startY, grid_rows, grid_cols)
        self.end_region = get_16region(endX, endY, grid_rows, grid_cols)

    def __str__(self):
        return (f"Ride(start={self.start}, end={self.end}, "
                f"earliest={self.early_start}, latest={self.latest_finish}),"
                f"distance={self.distance}, start_region={self.start_region}, end_region={self.end_region}")

class Route:
    def __init__(self, ride):
        self.rides = [ride]
        self.distance = 0

    def __str__(self):
        return " -> ".join([f"{ride.original_index}" for ride in self.rides])

class Simulation:
    def __init__(self, R, C, F, N, B, T, rides):
        self.rows = R
        self.cols = C
        self.vehicles = [Vehicle for i in range(F)]
        self.num_rides = N
        self.rides = rides
        self.bonus = B
        self.steps = T

    # def sort(self, criteria: sortCriteria)

    def __str__(self):
        output = []
        output.append(f"Simulation:")
        output.append(f"  Grid: {self.rows} rows x {self.cols} cols")
        output.append(f"  Vehicles: {len(self.vehicles)}")
        output.append(f"  Rides: {len(self.rides)}")
        output.append(f"  Bonus: {self.bonus}")
        output.append(f"  Steps: {self.steps}")
        output.append("")
        output.append("Rides:")
        for ride in self.rides:
            output.append("  " + str(ride))   # use Ride.__str__()
        return "\n".join(output)
        

def parser(input_file: str) -> Simulation:
    # read the file header row which contains R, C, F, N, B, T
    rows = 0
    cols = 0
    vehicles = 0
    rides = 0
    bonus = 0
    steps = 0
    informations = []
    
    with open(input_file, "r") as f:
        # parse the first line
        for line in f:
            informations = list(map(int, line.split()))
            break
            
        grid_rows = informations[0]
        grid_cols = informations[1]
        vehicles = informations[2]
        rides = informations[3]
        bonus = informations[4]
        steps = informations[5]

        # parse the rest

    rides_obj = []
    with open(input_file, "r") as f:
        next(f)
        i = 0
        for line in f:
            ride_info = list(map(int, line.split()))
            r = Ride(ride_info[0], ride_info[1], ride_info[2], ride_info[3], ride_info[4], ride_info[5], i, grid_rows, grid_cols)
            rides_obj.append(r)
            i += 1


    return Simulation(grid_rows, grid_cols, vehicles, rides, bonus, steps, rides_obj)

def sortRides(rides_list, sortCriteria):

    if sortCriteria == SortCriteria.EARLY_START:
        sorted_rides = sorted(rides_list, key=lambda r: r.early_start)

    if sortCriteria == SortCriteria.DISTANCE:
        sorted_rides = sorted(rides_list, key=lambda r: r.distance)
    
    return sorted_rides

def get_1region(row, col, num_rows, num_cols):
    return 0

def get_4region(row, col, num_rows, num_cols):
    # Divide rows and columns in half
    row_region = 0 if row < num_rows // 2 else 1
    col_region = 0 if col < num_cols // 2 else 1
    # Region index: 0 (top-left), 1 (top-right), 2 (bottom-left), 3 (bottom-right)
    return row_region * 2 + col_region

def get_9region(row, col, num_rows, num_cols):
    # Divides rows and columns in 3 parts
    row_region = row * 3 // num_rows
    col_region = col * 3 // num_cols
    # Region index: from 0 to 8
    return row_region * 3 + col_region

def get_16region(row, col, num_rows, num_cols):
    # Devides rows and columns in 4 parts
    row_region = row * 4 // num_rows
    col_region = col * 4 // num_cols
    # Region index: from 0 to 15
    return row_region * 4 + col_region

def compute_distance(startX, startY, endX, endY):
    computed_distance = abs(startX - endX) + abs(startY - endY)
    return computed_distance

def constructFunctionForJudge(routes):
    with open("result.txt", "w") as f:
        for i, route in enumerate(routes):
            rides = " ".join([f"{ride.original_index}" for ride in route.rides])
            f.write(f"{len(route.rides)} {rides}\n")



# algorithms

def randomAssignment(sorted_rides):
    # Inizializza una lista di oggetti Route vuoti, uno per ogni veicolo
    routes = [Route(None) for _ in range(len(sim.vehicles))]
    for ride in sorted_rides:
        route_index = random.randrange(len(routes))
        if routes[route_index].rides[0] is None:
            routes[route_index].rides[0] = ride
        else:
            routes[route_index].rides.append(ride)
    return routes

def assignmentByLabels(sorted_rides, gridX, gridY):
    """
    Assigns rides to vehicles based on their start and end regions to minimize route distances.

    Parameters:
        sorted_rides (list): List of Ride objects, sorted by a given criteria.
        gridX (int): Number of rows in the grid.
        gridY (int): Number of columns in the grid.

    Returns:
        list: A list of Route objects, each representing the sequence of rides assigned to a vehicle.
    """
    # assign the first n rides (n = number of vehicles) to the n vehicles
    # ride_assigned_index = 0
    #for route in routes:
     #   route = Route(sorted_rides[ride_assigned_index])
      #  route.distance = sorted_rides[ride_assigned_index].distance + sorted_rides[ride_assigned_index].startX + sorted_rides[ride_assigned_index].startY   
       # ride_assigned_index += 1
    
    # Initialize routes with the first N rides assigned to each vehicle
    routes = [Route(sorted_rides[i]) for i in range(len(sim.vehicles))]

    # assign the rest of the rides to the routes
    for k, ride in enumerate(sorted_rides[len(sim.vehicles):]):
        # For each remaining ride (after the first N rides assigned to vehicles):
        best_route_index = 0
        min_distance = gridX * gridY  # Initialize with a large value (max possible grid distance)
        for i, route in enumerate(routes):
            last_ride = route.rides[-1]  # Get the last ride assigned to this route
            # Check if the end region of the last ride matches the start region of the current ride
            if last_ride.end_region == ride.start_region:
                # Calculate the total distance if this ride is added to this route
                new_distance = route.distance + compute_distance(last_ride.endX, last_ride.endY, ride.startX, ride.startY) + ride.distance
                # If this route gives a smaller total distance, update the best route
                if new_distance <= sim.steps and new_distance <= ride.latest_finish and new_distance < min_distance:
                    min_distance = new_distance
                    best_route_index = i
        # Assign the ride to the best route found
        routes[best_route_index].rides.append(ride)
        # Update the total distance for the route
        routes[best_route_index].distance = min_distance
    
    # Assign any rides that were not added to any route
    # Instead, ensure all rides are assigned by iterating through unassigned rides.
    # Step 1: Collect all assigned ride indices
    assigned_indices = set()
    for route in routes:
        for ride in route.rides:
            if ride is not None:
                assigned_indices.add(ride.original_index)

    # Step 2: Find all unassigned ride indices
    all_indices = set(range(len(sorted_rides)))
    unassigned_indices = all_indices - assigned_indices
    for idx in unassigned_indices:
        # Assign each unassigned ride to the route with the least total distance
        ride = sorted_rides[idx]

        # Find the route with the minimum total distance among all routes
        min_route = min(routes, key=lambda r: r.distance)

        # Add the current ride to the route with minimum distance
        min_route.rides.append(ride)

        # Get the second-to-last ride (the previous ride before the one just added)
        # If there's only one ride in the route now, last_ride will be None
        last_ride = min_route.rides[-2] if len(min_route.rides) > 1 else None

        # Update the total distance of the route
        if last_ride:
            # If there was a previous ride, add:
            # 1. Travel distance from end of previous ride to start of current ride
            # 2. Distance of the current ride itself
            min_route.distance += compute_distance(last_ride.endX, last_ride.endY, ride.startX, ride.startY) + ride.distance
        else:
            # If this is the first ride in the route, just add the ride's distance
            # (assuming vehicle starts at origin or previous distance calculation already accounts for initial position)
            min_route.distance += ride.distance

    return routes



if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) < 2:
        print("Usage: python app.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    sim = parser(input_file)
    print(sim)

    # routes list to save the different routes
    # routes = [[] for _ in range(len(sim.vehicles))]

    #for each sorted ride, assign it to a random route 

    # vehicle makes a route, like 1 -> 2 -> 3 where 1, 2, 3 are rides, 
    # the vehicle do the ride 1, then the ride 2, and than the ride 3, that's a route
    # vehicle 1: 3 -> 2 this is a route
    # vehicle 2: 1 this is also a route

    sorted_rides = sortRides(sim.rides, SortCriteria.EARLY_START)

    # routes = randomAssignment(sorted_rides)
    routes = assignmentByLabels(sorted_rides, sim.rows, sim.cols)

    constructFunctionForJudge(routes)


    print("-------------------")
    print("Routes details\n")

    for i, route in enumerate(routes):
        print(f"Route {i + 1}:")
        for ride in route.rides:
            print(f"  {ride}")
        print()

    print("-------------------")


    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")

