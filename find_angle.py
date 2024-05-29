import numpy as np

def find_angle(coord_1: tuple[int,int], coord_2: tuple[int,int]):
    slope = (coord_1[1] - coord_2[1]) / (coord_1[0] - coord_2[0])
    angle_rad = np.arctan(slope)
    angle = np.rad2deg(angle_rad)

    if angle < 0:
        return 360 + angle
    else:
        return angle

def main():
    coord_1 = input("Enter first two coordinates:\n").split(" ")
    coord_2 = input("Enter next two coordinates:\n").split(" ")
    
    coord_1 = [int(x) for x in coord_1]
    coord_2 = [int(x) for x in coord_2]

    print(f"{find_angle(coord_1, coord_2)}")


if __name__ == "__main__":
    main()

