import math


def feld_zeichnen(feld):
    for i in feld:
        buffer = '|'
        for j in range(len(feld[i])):
            if len(str(feld[i][j])) == 1:
                buffer += ' ' + str(feld[i][j]) + '|'
            else:
                buffer += str(feld[i][j]) + '|'
        print(buffer)


#  den Punkt raussuchen wo die Spirale anfängt
def finde_mitte(feld):
    x = len(feld)/2
    if type(x) != int:
        x = (x//2) + 1
    y = len(feld[0])/2
    if type(x) != int:
        y = (y//2) + 1
    return y, x


def erzeuge_spirale(maximum, y, x, spirale):
    spirale[y][x] = 1
    x += 1
    spirale[y][x] = 2
    for i in range(3, maximum + 1):
        if spirale[y][x - 1] != 0 and spirale[y - 1][x] == 0:  # es wird nach oben gegangen
            spirale[y - 1][x] = i
            y -= 1
        elif spirale[y + 1][x] != 0 and spirale[y][x - 1] == 0:  # es wird nach links gegangen
            spirale[y][x - 1] = i
            x -= 1
        elif spirale[y][x + 1] != 0 and spirale[y + 1][x] == 0:  # es wird nach unten gegangen
            spirale[y + 1][x] = i
            y += 1
        elif spirale[y - 1][x] != 0 and spirale[y][x + 1] == 0:  # es wird nach rechts gegangen
            spirale[y][x + 1] = i
            x += 1
        else:
            print('ein seltsamer Fehler ist aufgetreten')
    return spirale
            

spirale = {}


print('gib die Seitenlänge der Spirale ein')
maximum = input()


try:
    maximum = int(maximum)
except:
    print('Die Eingabe "' + str(maximum) + '" ist falsch')

maximum = maximum ** 2

for i in range(maximum):
    spirale[i] = []

for i in range(len(spirale)):
    for j in range(maximum):
        spirale[i].append(0)


x, y = finde_mitte(spirale)
spirale = erzeuge_spirale(maximum, int(y), int(x), spirale)

# alle überflüssigen Nullen rausstreichen
for i in range(len(spirale)):
    for j in range(len(spirale[i])):
        try:
            spirale[i].remove(0)
        except:
            pass
    if len(spirale[i]) == 0:
        spirale.pop(i)

feld_zeichnen(spirale)