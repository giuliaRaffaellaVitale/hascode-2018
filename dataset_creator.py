import random
import os
import sys


def generate_dataset(input_file):

    with open(input_file, "r") as f:
        first_line = f.readline()
        info = list(map(int, first_line.split()))
        X_axis_min, X_axis_max = 0, info[0]
        Y_axis_min, Y_axis_max = 0, info[1] 


    with open("VitaleGiuliaRaffaella_dataset.txt", "w") as f_out:
        f_out.write(first_line)
        for _ in range(info[3]):
            x_start = random.randint(X_axis_min, X_axis_max - 1)
            y_start = random.randint(Y_axis_min, Y_axis_max - 1)
            x_end = random.randint(X_axis_min, X_axis_max - 1)
            y_end = random.randint(Y_axis_min, Y_axis_max - 1)
            while x_start == x_end and y_start == y_end:
                x_end = random.randint(X_axis_min, X_axis_max - 1)
                y_end = random.randint(Y_axis_min, Y_axis_max - 1)
            f_out.write(f"{x_start} {y_start} {x_end} {y_end} 0 {info[5]} \n")

if __name__ == "__main__":

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        sys.exit(1)

    generate_dataset(input_file)

    