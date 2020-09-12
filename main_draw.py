from teams import pool1, pool2, pool3, pool4
from result import Result
from itertools import permutations

teams = []
for i in range(4):
    teams.append(pool1[i])
for i in range(4):
    teams.append(pool2[i])
for i in range(4):
    teams.append(pool3[i])
for i in range(4):
    teams.append(pool4[i])

print(f'Simulating teams: {", ".join(map(str, teams))}')

# The group draw goes before Play-ins.  Pool 4 teams are drawn into groups after Play-ins ends.

# Create a list of all draw order permutations, ignoring team selection
permutations1 = list(permutations(pool1))
permutations2 = list(permutations(pool2))
permutations3 = list(permutations(pool3))
permutations4 = list(permutations(pool4))

result_groups = []
for p1 in permutations1:
    for p2 in permutations2:
        for p3 in permutations3:
            for p4 in permutations4:
                result_groups.append(Result(p1, p2, p3, p4))

for result in result_groups:
    print(result)
