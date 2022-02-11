import random
import sys
import pygame
import math

pygame.init()

FK = (3840, 2160)
FHD = (1920, 1080)
UHD = (2560, 1440)
HD = (1080, 720)

screen = pygame.display.set_mode(HD)


# Farben
Punktcol = (120, 150, 200)
Punktfcol = (200, 80, 120)
Stickcol = (180, 180, 180)
Hintergrundcol = (50, 100, 170)

selected = -1
# bekommt die Zahl von einem Punkt der angeklickt wurde, ist -1 wenn keiner angeKlickt wurde

# pygame.draw.circle(screen, Punktcol, (2560, 1440), 20)
# zeigt einen Punkt an


x, y = 0, 0
# Mouseposition initialisiert

# speichert alle Punkte mit X und Y Koordinaten
# der dritte Wert ist 0 bie normalen Punkten und 1 wenn der Punkt gefixt ist
points = []
# speichert alle Sticks, mit den beiden Punkten mit denen sie verbunden sind
sticks = []

# speichert die Geschwindigkeit von den einzelnen Punkten mit Betrag und Richtung
speed = []
# speichert für jeden Stick die Länge wenn er erstellt wird
Stick_Länge = []



# bildet den tan hoch -1 von einem x und gibt diesen als float zurück
def intan(x):
    return math.degrees(math.atan(x))


# bildet den cos hoch -1 von x und gibt dieses als float zurück
def incos(x):
    return math.acos(x) * 180/math.pi


def render():
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

    pygame.display.update()


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
    # TODO: soll aus 2 Kräften mit Richtung und Betrag die resultierende Kraft mit Richtung und Betrag berechnen
    # Format der Kraft [Betrag, Richtung in Grad die die Kraft von g (senkrecht nach unten) abweicht -> ist gegen den Uhrzeigersinn]

    if force1[0] == 0:
        return force2
    if force2[0] == 0:
        return force1

    # TODO: hier alle Fälle bearbeiten die nicht Sonderfälle sind


#  berechnet Kraft von einem Stick der gestreckt/zusammengedrückt wird
#  es muss der Stick angegeben werden auf den die Kraft wirkt
def get_stickforce(stick, D, point_of_attack):
    F = abs(get_sticklänge(stick) - Stick_Länge[stick]) * D  # berechnet den Betrag der Kraft

    A = [points[sticks[stick][0]][0], points[sticks[stick][0]][1]]  # Koordinaten von Punkt 1
    B = [points[sticks[stick][1]][0], points[sticks[stick][1]][1]]  # Koordinaten von Punkt 2

    if A != points[point_of_attack]:
        print(1)
        B = A
        A = points[point_of_attack]

        print(A, B)

    # Seiten in einem Dreieck
    a = A[0] - B[0]
    b = A[1] - B[1]
    c = math.sqrt(a**2 + b **2)

    alpha = incos((-(a**2) + b ** 2 + c ** 2) / (2 * b * c))

    return F, alpha


def move_points():
    global speed, points
    D = [1, 0]  # Stärke der Federn der Sticks, die Null muss für die Richtung jedes Sticks angepasst werden
    g = [9.81, 0]

    bereits_erledigt = []  # die Punkte die bereits neu berechnet wurden
    while len(bereits_erledigt) != len(points):  # um jeden Punkt in zufälliger Reihenfolge zu nehmen müssen die bereits erledigten gespeichert werden
        i = random.randrange(0, len(points))
        if i not in bereits_erledigt and sticks[i][2] != 1:  # wenn der Punkt noch nicht neu berechnet wird
            force = [0, 0]
            beteiligte_sticks = []  # speichert alle Sticks an denen der Punkt irgendwie befestigt ist
            for j in range(len(sticks)):
                if points[i] in sticks[j]:
                    beteiligte_sticks.append(j)

            for j in range(len(beteiligte_sticks)):  # berechnet die Kraft von momentaner Kraft und jedem Stick
                # TODO: die Kraft von der momentanen und einem Stick berechnen
                pass

            force = get_force(force, g)  # berechnet Kraft mit der Gravitation
            force = get_force(force, speed[i])  # berechnet Kraft mit letzter Geschwindigkeit

            speed[i] = force  # Geschwindigkeit wird so hingesetzt

            bereits_erledigt.append(i)  # der Punkt kann als fertig gespeichert werden

        elif sticks[i][2] == 1 and i not in bereits_erledigt:  # der Stick ist gelockt und kann mit als erledigt gemarkt werden
            bereits_erledigt.append(i)


    # TODO: nachdem jeder Stick eine Geschwindigkeit bekommen hat muss jeder auch noch bewegt werden

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
                                Stick_Länge.remove(Stick_Länge[sticks.index([selected, Punkt])])
                                sticks.remove([selected, Punkt])
                            except:
                                Stick_Länge.remove(Stick_Länge[sticks.index([Punkt, selected])])
                                sticks.remove([Punkt, selected])
                        else:
                            sticks.append([selected, Punkt])
                            Stick_Länge.append(get_sticklänge(len(sticks) - 1))

                        selected = -1

    try:
        print(get_stickforce(0, 1, 0))

    except:
        pass

    render()
