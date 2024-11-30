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

# right_angle()
# left_angle(8)
# down_right()
straight_down()