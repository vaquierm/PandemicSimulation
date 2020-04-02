from random import random

count = 0
N = 10000000
for i in range(N):
    if random() < 0.2:
        count += 1
    if random() < 0.1:
        count += 1
    if random() < 0.3:
        count += 1
    if random() < 0.4:
        count += 1

print(count/N)
