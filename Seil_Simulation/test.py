import math

def incos(x):  # wurde getestet
    return math.degrees(math.acos(x))


def insinus(x):  # wurde getestet
    return math.degrees(math.asin(x))


def cos(x):
    return math.cos(math.radians(x))


def sin(x):
    return math.sin(math.radians(x))




# bildet das Kräfteparallelogramm von zwei Kräften und gibt Betrag und Richtung der resultierenden Kraft als List zurück
def get_force(force1, force2):  # Teststatus: Funktion wurde komplett getestet und funktioniert
    # Format der Kraft [Betrag, Richtung in Grad die die Kraft von g (senkrecht nach unten) abweicht -> ist gegen den Uhrzeigersinn]
    if force1[1] > force2[1]:  # damit v1 kleineren Winkel als v2 hat
        force_buffer = force1
        force1 = force2
        force2 = force_buffer

    if force1[0] == 0:
        return force2
    if force2[0] == 0:
        return force1

    v1 = force1[0]  # c
    v2 = force2[0]  # a
    alpha = force2[1] - force1[1]  # alpha ist jetzt der Winkel zwischen v1 und v2

    v = math.sqrt(v1 ** 2 + v2 ** 2 + (2 * v1 * v2 * cos(alpha)))  # b

    if alpha < 180:  # das Parallelogramm ist auf die normale Seite geklappt
        alpha = 180 - alpha  # alpha ist jetzt der andere Winkel im Kräfteparallelogramm -> wichtig für weitere Rechnungen
        alpha = insinus((v2/v) * sin(alpha))
    else:  # das Parallelogramm klappt sich auf die andere Seite
        alpha = incos((-(v2 ** 2) + v ** 2 + v1 ** 2) / (2 * v1 * v))

        alpha = 360 - alpha

    alpha += force1[1]
    alpha = alpha // 1
    alpha = alpha % 360
    return [v, alpha]


force1 = [41.843380337644476, 186.031922447347]
force2 = [9.81, 0]

forces = [force1, force2]

print(get_force(forces[0], forces[1]))
