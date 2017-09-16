valueLeft = 999
valueRight = 999
highest = 0
while True:
    value = valueLeft * valueRight
    if value > highest:
        if value == int(str(value)[::-1]):
            highest = value
            valueLeft -= 1
            valueRight = valueLeft
        else:
            valueRight -= 1
    else:
        if valueLeft == valueRight:
            break
        valueLeft -= 1
        valueRight = valueLeft
    if valueRight == 99:
        valueLeft -= 1
        valueRight = valueLeft
    if valueLeft == 100:
        break
print(highest)
input("Enter to close.")
