from itertools import permutations

a = list('ABCDEFGHIJKL')
p = permutations(a)

print(len(a))
print(len(list(p)))