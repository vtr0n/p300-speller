import random

grid = [[0 for _ in range(6)] for _ in range(6)]

row = [0 for _ in range(6)]
col = [0 for _ in range(6)]

target = (0, 0)

for _ in range(10):
    for i in range(6):
        if i == target[0]:
            row[i] += 1 if random.randint(1, 4) <= 3 else -1
        else:
            row[i] += 1 if random.randint(1, 4) == 3 else -1

print(row)
