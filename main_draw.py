from collections import Counter
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

with open("output.txt", "w") as out_file:
    print(f"Storing {len(result_groups)} groups into {out_file.name}")
    for result in result_groups:
        print(result, file=out_file)

with open("raw_groups.txt", "w") as group_file:
    print(f"Storing {len(result_groups)} groups into {group_file.name}")
    for result in result_groups:
        print(result.groups, file=group_file)

# Sort the groups so that order will not matter, reducing hash values
for result in result_groups:
    result.sort_groups()

with open("totals.txt", "w") as totals_file:
    totals = Counter()
    for result in result_groups:
        totals[str(result.groups)] += 1
    print(f"Storing {len(totals)} hashes into {totals_file.name}")
    for key in totals:
        print(f"{key} - {totals[key]}", file=totals_file)
