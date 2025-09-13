import os
import sys

class Vehicle:
    def __init__(self):
        pass

class Ride:
    def __init__(self, startX, starY, endX, endY, early_start, latest):
        self.start = (startX, starY)
        self.end = (endX, endY)
        self.early_start = early_start
        self.latest_finish = latest

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
        for line in f:
            ride_info = list(map(int, line.split()))
            r = Ride(ride_info[0], ride_info[1], ride_info[2], ride_info[3], ride_info[4], ride_info[5])
            rides_obj.append(r)


    return Simulation(rows, cols, vehicles, rides, bonus, steps, rides_obj)


if __name__ == "__main__":
    
    sim = parser("./input/a.txt")
    
    print(sim)