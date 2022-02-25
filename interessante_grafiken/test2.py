old = [[i + j for i in range(3)] for j in range(3)]

for i in old:
    print(i)
print('---------')

old.insert(0, old[0].copy())

new = old.copy()
new[0].insert(0, 'X')


for i in new:
    print(i)

