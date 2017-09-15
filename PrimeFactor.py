value = 600851475143
keepGoing = True
while keepGoing:
    for x in range(2, value):
        if x >= value // 2:
            keepGoing = False
            break
        if value % x == 0:
            value = value//x
            break
print(value)
input("Enter to finish.")
