from builtins import set
import os
import sys
from enum import Enum
import random
import time


class SortCriteria(Enum):
    EARLY_START = 0
    DISTANCE = 1

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
        self.start_region = get_9region(startX, startY, grid_rows, grid_cols)
        self.end_region = get_9region(endX, endY, grid_rows, grid_cols)

    def __str__(self):
        return (f"Ride(start={self.start}, end={self.end}, "
                f"earliest={self.early_start}, latest={self.latest_finish}),"
                f"distance={self.distance}, start_region={self.start_region}, end_region={self.end_region}")

class Route:
    def __init__(self):
        self.rides = []
        self.distance = 0

    def __str__(self):
        return " -> ".join([f"{ride.original_index}" for ride in self.rides])

class Simulation:
    def __init__(self, R, C, F, N, B, T, rides):
        self.rows = R
        self.cols = C
        self.vehicles = F
        self.num_rides = N
        self.rides = rides
        self.bonus = B
        self.steps = T

    # def sort(self, criteria: sortCriteria)

    def __str__(self):
        output = []
        output.append(f"Simulation:")
        output.append(f"  Grid: {self.rows} rows x {self.cols} cols")
        output.append(f"  Vehicles: {self.vehicles}")
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
    # Initialize a list of empty Route objects, one for each vehicle
    routes = [Route() for _ in range(len(sim.vehicles))]
    for ride in sorted_rides:
        route_index = random.randrange(len(routes))
        routes[route_index].rides.append(ride)
        routes[route_index].distance += ride.distance
    return routes

def assignmentByLabels(sorted_rides, gridX, gridY):

    # create a list of empty Route objects, one for each vehicle
    routes = [Route() for _ in range(sim.vehicles)]

    # Initialize routes with the first N rides assigned to each vehicle and compute their distances
    ride_assigned_index = 0
    for route in routes:
        assigned_ride = sorted_rides[ride_assigned_index]
        route.rides.append(assigned_ride)
        route.distance = assigned_ride.distance + assigned_ride.startX + assigned_ride.startY   
        ride_assigned_index += 1
    
    not_assigned_rides = []

    # assign the rest of the rides to the routes
    for k, ride in enumerate(sorted_rides[ride_assigned_index:]):
        # For each remaining ride (after the first N rides assigned to vehicles):
        changed = False
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
                    changed = True
        # if a souitable route is found
        if(changed):
            # Assign the ride to the best route found
            routes[best_route_index].rides.append(ride)
            # Update the total distance for the route
            routes[best_route_index].distance = min_distance
        else:
            not_assigned_rides.append(ride)
            # If no suitable route is found, add the ride to not_assigned_rides for
        
    for ride in not_assigned_rides:
        print(f"Ride not assigned: {ride}")

    while len(not_assigned_rides) > 0:

        # Find the route with the minimum total distance among all routes
        min_route = min(routes, key=lambda r: r.distance)
        # Get the last ride in that route
        last_ride = min_route.rides[-1]

        min_distance = float('inf')
        best_route = None
        # Find the ride from not_assigned_rides that, when added to min_route, results in the smallest increase in distance
        for ride in not_assigned_rides:
            new_distance = compute_distance(last_ride.endX, last_ride.endY, ride.startX, ride.startY) + ride.distance
            if new_distance < min_distance:
                min_distance = new_distance
                best_route = ride
        # Add the best ride to the min_route
        min_route.rides.append(best_route)
        # Update the distance of min_route
        min_route.distance += min_distance
        # Remove the assigned ride from not_assigned_rides
        not_assigned_rides.remove(best_route)


    return routes
    



if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) < 2:
        print("Usage: python app.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    sim = parser(input_file)
    print(sim)

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

