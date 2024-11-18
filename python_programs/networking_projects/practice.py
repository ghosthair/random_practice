print("Would you like to message a user or person?")
x = input()
if x == "user":
    y = input("User: ")
    y = "@" + y
elif x == "room":
    y = input("Room: ")
    y = "#" + y

print(y)