import random
import sys
import time

import pygame
import math

pygame.init()

FK = (3840, 2160)
FHD = (1920, 1080)
UHD = (2560, 1440)
HD = (1080, 720)

screen = pygame.display.set_mode(UHD)


# Farben
Punktcol = (120, 150, 200)
Punktfcol = (200, 80, 120)
Stickcol = (180, 180, 180)
Hintergrundcol = (50, 100, 170)
RED = (180, 70, 70)
GREEN = (70, 180, 70)

selected = -1
# bekommt die Zahl von einem Punkt der angeklickt wurde, ist -1 wenn keiner angeKlickt wurde

# pygame.draw.circle(screen, Punktcol, (2560, 1440), 20)
# zeigt einen Punkt an

Mode = False  # wird auf True gesetzt wenn die Physik aktiv sein soll
x, y = 0, 0
# Mouseposition initialisiert

# speichert alle Punkte mit X und Y Koordinaten
# der dritte Wert ist 0 bie normalen Punkten und 1 wenn der Punkt gefixt ist
points = []
# speichert alle Sticks, mit den beiden Punkten mit denen sie verbunden sind
sticks = []

# speichert die Geschwindigkeit von den einzelnen Punkten mit Betrag und Richtung
speed = [[0, 0] for i in range(len(points))]
# speichert für jeden Stick die Länge wenn er erstellt wird
Stick_Länge = []



# rendert den gesamten Screen, hat nichts mit der Physik zu tun
def render(modus):
    screen.fill(Hintergrundcol)

    for i in range(len(sticks)):  # jeder Stick soll gerendert werden
        try:
            # zeichnet eine Linie zwischen den Punkten die verbunden sind
            pygame.draw.line(screen, Stickcol, (points[sticks[i][0]][0], points[sticks[i][0]][1]), (points[sticks[i][1]][0], points[sticks[i][1]][1]), 4)
        except:
            pass

    for i in range(len(points)):  # rendert die Punkte
        a, b = points[i][0], points[i][1]
        if points[i][2] == 0:  # normalen Punkt anzeigen
            pygame.draw.circle(screen, Punktcol, (a, b), 10)
        elif points[i][2] == 1:  # gefixten Punkt anzeigen
            pygame.draw.circle(screen, Punktfcol, (a, b), 10)

    if modus:
        pygame.draw.circle(screen, GREEN, (15, 15), 20)
    else:
        pygame.draw.circle(screen, RED, (15, 15), 20)

    pygame.display.update()


def wipe():
    global points, sticks, speed

    points, sticks, speed = [], [], []



# bildet den tan hoch -1 von einem x und gibt diesen als float zurück
def intan(x):
    return math.degrees(math.atan(x))


# bildet den cos hoch -1 von x und gibt dieses als float zurück, wenn man mehr als 180 Grad erwartet, wird das ergebnis %180 zurcükgegeben
def incos(x):
    return math.acos(x) * 180/math.pi


# gibt die Nummer von einem Punkt wenn dieser angeklickt wurde, gibt True wenn einer angeklickt wurde
def detect_point(a, b):
    bereich = 20  # wie groß die "Hitbox" von einem Punkt ist, etwa 20 ist ganz okay
    for i in range(a - bereich, a + bereich):
        for j in range(b - bereich, b + bereich):
            if [i, j, 0] in points or [i, j, 1] in points:
                try:
                    return points.index([i, j, 0]), True
                except:
                    return points.index([i, j, 1]), True
    return -1, False


# ist um die Standardlänge von einem neuen Stick zu ermitteln
def get_sticklänge(stick):
    A = [points[sticks[stick][0]][0], points[sticks[stick][0]][1]]  # Koordinaten von Punkt 1
    B = [points[sticks[stick][1]][0], points[sticks[stick][1]][1]]  # Koordinaten von Punkt 2

    a = abs(A[0] - B[0])  # Abstand auf der X-Achse
    b = abs(A[1] - B[1])  # Abstand auf der Y-Achses

    return math.sqrt(a**2 + b**2)


def get_force(force1, force2):
    # Format der Kraft [Betrag, Richtung in Grad die die Kraft von g (senkrecht nach unten) abweicht -> ist gegen den Uhrzeigersinn]

    if force1[1] > force2[1]:  # damit v1 kleineren Winkel als v2 hat
        force_buffer = force1
        force1 = force2
        force2 = force_buffer

    v1 = force1[0]  # c
    v2 = force2[0]  # a
    alpha = force2[1] - force1[1]

    v = math.sqrt(v1 ** 2 + v2 ** 2 + (2* v1 * v2 * math.cos(alpha)))  # b

    try:
        alpha = incos((-(v1 ** 2) + v ** 2 + v2 ** 2) * (2 * v * v1))  # es müssen wieder wie in Stickforce die Fälle betrachtet werden, wenn v/v1 0 ist/wenn incos() wegen Spiegelungen rumbuggt

        alpha += v1[1]  # das Offset vom Anfang muss addiert werden (ist momentan nur der Winkel relativ zu v1

    except:  # ein Fehler tritt bei dem oberen dann auf, wenn b oder c Null ist ->
        if v == 0:
            alpha = 0
        elif v1 == 0:
            alpha = v2

        # TODO: weitere Sonderfälle?

    return [v, alpha]


#  berechnet Kraft von einem Stick der gestreckt/zusammengedrückt wird
#  es muss der Stick angegeben werden auf den die Kraft wirkt
def get_stickforce(stick, D, point_of_attack):  # kann erstmal eingebaut werden, müsste soweit auch funktionieren
    F = abs(get_sticklänge(stick) - Stick_Länge[stick]) * D  # berechnet den Betrag der Kraft

    A = [points[sticks[stick][0]][0], points[sticks[stick][0]][1]]  # Koordinaten von Punkt 1
    B = [points[sticks[stick][1]][0], points[sticks[stick][1]][1]]  # Koordinaten von Punkt 2

    if A[0] != points[point_of_attack][0] and A[1] != points[point_of_attack][1]:
        B = A
        A = points[point_of_attack]

    # Seiten in einem Dreieck
    a = A[0] - B[0]
    b = A[1] - B[1]
    c = math.sqrt(a ** 2 + b ** 2)

    try:
        alpha = incos((-(a ** 2) + b ** 2 + c ** 2) / (2 * b * c))
        if A[0] > B[
            0]:  # zweiter Punkt ist im 2. oder 3. Quadranten relativ zum 1. Punkt -> ist nicht richtig berechnet
            alpha = 180 + alpha

    except:  # ein Fehler tritt bei dem oberen dann auf, wenn b oder c Null ist -> 180° oder 0°
        if A[0] < B[0]:
            alpha = 0
        else:
            alpha = 180

    return [F, alpha]


def move_points():
    global speed, points
    D = [1, 0]  # Stärke der Federn der Sticks, die Null muss für die Richtung jedes Sticks angepasst werden
    g = [9.81, 180]

    try:
        for i in range(len(points)):
            if points[i][2] == 0:  # wenn der Punkt nicht gelockt ist
                beteiligte_sticks = []  # speichert alle Sticks an denen der Punkt irgendwie befestigt ist
                for j in range(len(sticks)):
                    if points[i] in sticks[j]:
                        beteiligte_sticks.append(j)

                force = [0, 0]
                for j in range(len(beteiligte_sticks)):  # berechnet die Kraft von momentaner Kraft und jedem Stick
                    force = get_force(force, get_stickforce(beteiligte_sticks[j], 1, i))

                force = get_force(force, g)  # berechnet Kraft mit der Gravitation
                print('---')
                print(i, len(speed), speed)
                force = get_force(force, speed[i])  # berechnet Kraft mit letzter Geschwindigkeit

                speed[i] = force  # Geschwindigkeit wird so hingesetzt
    except:
        pass


    # Daten bereinigen -> falls Kräfte eine Richtung von Beispielsweise 420° haben -> 60°
    '''for i in range(len(speed)):
        speed[i][1] = speed[i][1] % 360'''  # TODO: die Datenbereinigung ist irgendwie kinda dump und muss gefixt werden

    # TODO: nachdem jeder Stick eine Geschwindigkeit bekommen hat muss jeder auch noch bewegt werden
    # als erstes muss herausgefunden werden in welchem Quadrant relativ zur jetztigen Position sich die neue Position befindet
    '''
    Quadraten:
    32
    41
    (alter Punkt ist in der Mitte)
    '''
    for i in range(len(speed)):
        speed[i][0] /= 10


    for i in range(len(speed)):  # Loop für alle Punkte mit ihren Geschwindigkeiten
        print('####')
        print(len(points), len(speed))
        if speed[i][1] == 0:  # Sonderfall senkrecht nach unten
            points[i][0] += speed[i][0]
        elif (speed[i][1] - 90) == 0:  # Sonderfall waagerecht nach rechts
            points[i][1] += speed[i][0]
        elif (speed[i][1] - 180) == 0:  # Sonderfall senkrecht nach oben
            points[i][0] -= speed[i][0]
        elif (speed[i][1] - 270) == 0:  # Sonderfall waagerecht nach links
            points[i][1] -= speed[i][0]
        else:  # die generellen Fälle (treten eigentlich immer auf)
            if (speed[i][1] - 90) < 0:  # erster Quadrant
                points[i][0] += speed[i][0] / math.sin(90 - speed[i][1])  # X Koordinate
                points[i][1] += speed[i][0] / math.sin(speed[i][1])       # Y Koordinate
            elif (speed[i][1] - 180) < 0:  # zweiter Quadrant
                speed[i][0] = speed[i][1] - 90  # den Winkel an den Quadranten anpassen

                points[i][0] += speed[i][0] / math.sin(90 - speed[i][1])  # X Koordinate
                points[i][1] -= speed[i][0] / math.sin(speed[i][1])       # Y Koordinate
            elif (speed[i][1] - 270) < 0:  # dritter Quadrant
                speed[i][0] = speed[i][1] - 180  # den Winkel an den Quadranten anpassen

                points[i][0] -= speed[i][0] / math.sin(90 - speed[i][1])  # X Koordinate
                points[i][1] -= speed[i][0] / math.sin(speed[i][1])       # Y Koordinate
            else:  # vierter Quadrant
                speed[i][0] = speed[i][1] - 270  # den Winkel an den Quadranten anpassen

                points[i][0] -= speed[i][0] / math.sin(90 - speed[i][1])  # X Koordinate
                points[i][1] += speed[i][0] / math.sin(speed[i][1])  # Y Koordinate

    return



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos  # gibt die Position der Maus mit Oben Links als (0|0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            state = pygame.mouse.get_pressed()
            if state[0]:  # linker Mousebutton -> loser Punkt soll hinzugefügt werden
                points.append([x, y, 0])
            elif state[2]:  # rechter Mousebutton -> gefixter Punkt soll hinzugefügt werden
                points.append([x, y, 1])
            elif state[1]:  # mittlerer Mousebutton wurde gedrückt, soll die Möglichkeit geben 2 Punkte mit einem Seil zu verbinden/trennen
                Punkt, test = detect_point(x, y)

                if test:
                    if selected == -1:
                        selected = Punkt
                    else:
                        if [selected, Punkt] in sticks or [Punkt, selected] in sticks:  # wenn an dieser Stelle eine Verbindung ist -> entferne diese
                            try:
                                i = sticks.index([selected, Punkt])

                                Stick_Länge.remove(Stick_Länge[i])
                                sticks.remove(sticks[i])
                                speed.remove(speed[i])
                            except:
                                i = sticks.index([Punkt, selected])

                                Stick_Länge.remove(Stick_Länge[i])
                                sticks.remove(sticks[i])
                                speed.remove(speed[i])
                        else:
                            sticks.append([selected, Punkt])
                            Stick_Länge.append(get_sticklänge(len(sticks) - 1))
                            speed.append([0, 0])

                        selected = -1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Mode = not Mode
            elif event.key == pygame.K_c:
                wipe()

    if Mode:
        move_points()
        #time.sleep(1)


    render(Mode)
