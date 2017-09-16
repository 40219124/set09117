valueLeft = 999
valueRight = 999
value = 0
notDone = True
while notDone:
    value = valueLeft * valueRight
    if value == int(str(value)[::-1]):
        notDone = False
    else:
        if valueLeft == valueRight:
            valueRight -= 1
        else:
            valueLeft -= 1
outLeft = 0
outRight = 0
while True:
    if valueRight == 999:
        valueLeft += 1
        valueRight = valueLeft
    else:
        valueRight += 1
    if valueLeft == 999 and valueRight == 999:
        break
    tempValue = valueLeft * valueRight
    if tempValue == int(str(tempValue)[::-1]):
        if tempValue > value:
            value = tempValue
            outLeft = valueLeft
            outRight = valueRight

print(outLeft, value, outRight)
input("Enter to close.")
