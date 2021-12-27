# A
'''Messungen = []
tiefer = 0
vorheriges = -2

with open('Messungen.txt') as f:
    zeug = f.read()

    Messungen = zeug.split()

for i in range(len(Messungen)):
    if int(Messungen[i]) > int(vorheriges):
        tiefer += 1
    vorheriges = Messungen[i]

if Messungen[20000]

print(tiefer)'''


# B

Messungen = []
tiefer = 0
vorheriges = -4

with open('Messungen.txt') as f:
    zeug = f.read()

    Messungen = zeug.split()

for i in range(len(Messungen)):
    Messungen[i] = int(Messungen[i])

i = 0
while i + 2 < len(Messungen):
    summe = Messungen[i] + Messungen[i+1] + Messungen[i+2]
    if summe >= vorheriges:
        tiefer += 1
    #print(summe)
    vorheriges = summe
    i += 1

print(tiefer)