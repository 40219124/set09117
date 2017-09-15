previous = 0
current = 1
combo = 1
addEvens = 0
while True:
    combo = current + previous
    if combo >= 4000000:
        break
    previous = current
    current = combo
    if combo%2 == 0:
        addEvens += combo
print (addEvens)
input("Enter to close.")
