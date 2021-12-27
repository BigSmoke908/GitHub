alles = []
a = []
b = []
c = []
z = []

x = 0

with open('bekannt.txt') as f:
    alles = f.read()
    f.close()

    alles = alles.split()

for i in range(len(alles)):
    alles[i] = int(alles[i])

# jetzt sind alle Daten unsortiert in alles

for i in range(len(alles)):
    buffer = i % 4
    if buffer == 0:
        a.append(alles[i])
    elif buffer == 1:
        b.append(alles[i])
    elif buffer == 2:
        c.append(alles[i])
    else:
        z.append(alles[i])


while len(alles) != 0:
    alles.remove(alles[0])

# jetzt sind alle Daten in a, b, c, z aufgeteilt und damit verarbeitbar

if x != 0:
    x = x + ((x - 1) * 4)


#punkt = a[x], b[x], c[x], z[x]
#print(punkt)