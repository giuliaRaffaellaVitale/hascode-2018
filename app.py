import os
import sys
from enum import Enum
import random


class SortCriteria(Enum):
    EARLY_START = 0
    DISTANCE = 1

class Vehicle:
    def __init__(self):
        pass

class Ride:
    def __init__(self, startX, starY, endX, endY, early_start, latest, original_index):
        self.start = (startX, starY)
        self.end = (endX, endY)
        self.early_start = early_start
        self.latest_finish = latest
        self.original_index = original_index
        self.distance = abs(startX - endX) + abs(starY - endY)

    def __str__(self):
        return (f"Ride(start={self.start}, end={self.end}, "
                f"earliest={self.early_start}, latest={self.latest_finish})")

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
            
        rows = informations[0]
        cols = informations[1]
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
            r = Ride(ride_info[0], ride_info[1], ride_info[2], ride_info[3], ride_info[4], ride_info[5], i)
            rides_obj.append(r)
            i += 1


    return Simulation(rows, cols, vehicles, rides, bonus, steps, rides_obj)

def sortRides(rides_list, sortCriteria):

    if sortCriteria == SortCriteria.EARLY_START:
        sorted_rides = sorted(rides_list, key=lambda r: r.early_start)

    if sortCriteria == SortCriteria.DISTANCE:
        pass
    
    return sorted_rides

def constructFunctionForJudge(routes):
    with open("result.txt", "w") as f:
        for i, route in enumerate(routes):
            rides = " ".join([f"{ride.original_index}" for ride in route])
            f.write(f"{len(route)} {rides}\n")

# algorithms

def randomAssignment(sorted_rides):
    for ride in sorted_rides:
        route_index = random.randrange(len(sim.vehicles)) 
        routes[route_index].append(ride)
    return routes


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    sim = parser(input_file)
    print(sim)

    # routes list to save the different routes
    routes = [[] for _ in range(len(sim.vehicles))]

    #for each sorted ride, assign it to a random route 

    # vehicle makes a route, like 1 -> 2 -> 3 where 1, 2, 3 are rides, 
    # the vehicle do the ride 1, then the ride 2, and than the ride 3, that's a route
    # vehicle 1: 3 -> 2 this is a route
    # vehicle 2: 1 this is also a route

    sorted_rides = sortRides(sim.rides, SortCriteria.EARLY_START)

    routes = randomAssignment(sorted_rides)

    constructFunctionForJudge(routes)


    print("-------------------")
    print("Routes details\n")

    for i, route in enumerate(routes):
        print(f"Route {i + 1}:")
        for ride in route:
            print(f"  {ride}")   # relies on Ride.__str__()
        print()

    print("-------------------")

