import math
import random


def incos(x):
    return math.acos(math.radians(x))


def insinus(x):
    return math.degrees(math.asin(x))


def cos(x):
    return math.cos(math.radians(x))


def sin(x):
    return math.sin(math.radians(x))



def get_force(force1, force2):  # TODO: Funktion testen/debuggen
    # Format der Kraft [Betrag, Richtung in Grad die die Kraft von g (senkrecht nach unten) abweicht -> ist gegen den Uhrzeigersinn]
    if force1[1] > force2[1]:  # damit v1 kleineren Winkel als v2 hat
        force_buffer = force1
        force1 = force2
        force2 = force_buffer

    if force1[0] == 0:
        return force2
    if force2[0] == 0:
        return force1

    print(force1, force2)
    print('--')
    v1 = force1[0]  # c
    v2 = force2[0]  # a
    alpha = force2[1] - force1[1]  # alpha ist jetzt der Winkel zwischen v1 und v2
    print(alpha)

    v = math.sqrt(v1 ** 2 + v2 ** 2 + (2 * v1 * v2 * cos(alpha)))  # b

    alpha = 180 - alpha  # alpha ist jetzt der andere Winkel im Kräfteparallelogramm -> wichtig für weitere Rechnungen

    print()
    alpha = insinus((v2/v) * sin(alpha))

    print(alpha)
    alpha += force1[1]
    res = [v, alpha]
    print(res)
    return res


forces = [[1, 135], [8, 137]]

print(forces)

forceges = [0, 0]
for i in range(len(forces)):
    forceges = get_force(forceges, forces[i])
    print('------')
    print(forceges)
