import random

a = 10, 15
# Bereich für Parameter a, in dem er richtig ist (beide Zahlen sind immer ausgeschlossen)
b = 7, 12
# Bereich für Parameter b
c = 9, 10
# Bereich für Parameter c
x = 10
# wie viele wahre Datenpunkte gegeben sein sollen
y = 0
# wie viele falsche Datenpunkte gegeben sein sollen

wahr = 1
falsch = 0
# wie die einzelnen Datenpunkte wenn sie wahr/falsch sein gelabelt werden sollen (wird halbiert, eine Hälfte größer, andere kleiner)
maxi = 60
# wie groß eine maximale Zahl sein kann, für einen Datenpunkt der nicht der Klasse angehört

with open('bekannt.txt', 'w') as f:
    for i in range(x):
        an = random.randrange(a[0] + 1, a[1] + 1, 1)
        bn = random.randrange(b[0] + 1, b[1] + 1, 1)
        cn = random.randrange(c[0] + 1, c[1] + 1, 1)
        buffer = str(an) +  " " + str(bn) + " " + str(cn) + " 1"
        f.write(buffer + '\n')

    not_Found = True

    for i in range(y):
        while not_Found:
            an = random.randrange(0,  maxi, 1)
            bn = random.randrange(0, maxi, 1)
            cn = random.randrange(0, maxi, 1)

            if an <= a[0] or an >= a[1] or bn <= b[0] or bn >= b[1] or cn <= c[0] or cn >= c[1]:
                not_Found = False
        buffer = str(an) + " " + str(bn) + " " + str(cn) + " 0"
        f.write(buffer + '\n')
        not_Found = True

    f.close()