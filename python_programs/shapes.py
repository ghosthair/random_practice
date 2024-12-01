import sys

def right_angle(x=5):
    rows = x
    for j in range(1, rows+1):
        print('* ' * j)

def left_angle(x=5):
    rows=x
    for i in range(0, rows):
        for j in range(0, i + 1):
            print("*", end=' ')
        print("\r")

def down_right(x=5):
    rows = x
    for i in range(rows + 1, 0, -1):
        for j in range(0, i -1):
            print("*", end=' ')
        print(" ")

def straight_down(x=5):
    rows = x
    k =2 * rows -2
    for i in range(rows, -1, -1):
        for j in range(k, 0, -1):
            print(end=" ")
        k = k + 1
        for j in range(0, i + 1):
            print("*", end=' ')
        print("")

#Testing the functions 
# right_angle()
# left_angle(8)
# down_right()
# straight_down()

if __name__ == "__main__":
    while True:
        print("Which would you like to run?\n1.) Upside down\n2.) Right Angle\n3.) Left Angle\n4.) Down right")
        x = int(input())
        print("How many lines would you like for the picture? (5-25)")
        y = int(input())
        if y > 25:
            y = 25
            print("Max size is 25")
        elif y < 5:
            y =5
            print("Minimum size is 5")
        print()

        if x == 1:
            straight_down(y)
            break
        elif x == 2:
            right_angle(y)
            break
        elif x == 3:
            left_angle(y)
            break
        elif x == 4:
            down_right(y)
            break
        else:
            print("Invalid choice, please try again.")

