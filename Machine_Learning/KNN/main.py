from math import sqrt as wurzel
from sortedcontainers import SortedDict

alles = []
a = []
b = []
c = []
z = []

ta = []
tb = []
tc = []
tz = []

x = 3 # welcher Punkt in den unbekannten Daten bestimmt werden soll


# alle Daten werden sortiert
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


# die Testteile werden sortiert
with open('unbekannt.txt') as f:
    alles = f.read()
    f.close()
    alles = alles.split()
for i in range(len(alles)):
    alles[i] = int(alles[i])

# jetzt sind alle Daten unsortiert in alles

for i in range(len(alles)):
    buffer = i % 4
    if buffer == 0:
        ta.append(alles[i])
    elif buffer == 1:
        tb.append(alles[i])
    elif buffer == 2:
        tc.append(alles[i])
    else:
        tz.append(alles[i])
while len(alles) != 0:
    alles.remove(alles[0])
# jetzt sind die Punkte die geprüft werden sollen fertig sortiert in ta, tb, tc, tz


distanz = {}
# speichert den Abstand zwischen einem gegebenen Punkt (der der geprüft)
# und allen Punkten aus den Trainingsdaten (Postion = Nummer von Punkt)
# der Key ist Abstand und der Wert ist der Wert von dem Punkt

for i in range(len(a)):
    buffer = wurzel(((a[i] - ta[x]) ** 2) + ((b[i] - tb[x]) ** 2) + ((c[i] - tc[x]) ** 2))
    print(buffer)
    distanz[buffer] = {z[i]}

distanz2 = SortedDict(distanz)

print(distanz)
print(distanz2)