arr = []  # [] for i in range(10)]
for i in range(10):
    arr.append([])
    for j in range(5):
        arr[i].append(i*j)
        print(i, i*j)

print(arr[1][3])
print(arr)
