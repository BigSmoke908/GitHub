import random
import sys
import time
import datetime
import pygame
import math

pygame.init()

FK = (3840, 2160)
FHD = (1920, 1080)
UHD = (2560, 1440)
HD = (1080, 720)

res = FK
# momentan ausgewählte Auflösung

screen = pygame.display.set_mode(res)


# Farben
#Punktcol = (120, 150, 200)
Punktcol = (0, 0, 0)
#Punktfcol = (200, 80, 120)
Punktfcol = (255, 255, 255)
Stickcol = (180, 180, 180)
Hintergrundcol = (50, 100, 170)
RED = (255, 70, 70)
GREEN = (70, 180, 70)

selected = -1
# bekommt die Zahl von einem Punkt der angeklickt wurde, ist -1 wenn keiner angeKlickt wurde

font = pygame.font.SysFont(None, 40)
Zeit = 0

# pygame.draw.circle(screen, Punktcol, (2560, 1440), 20)
# zeigt einen Punkt an

Mode = False  # wird auf True gesetzt wenn die Physik aktiv sein soll
x, y = 0, 0
# Mouseposition initialisiert

# speichert alle Punkte mit X und Y Koordinaten
# der dritte Wert ist 0 bie normalen Punkten und 1 wenn der Punkt gefixt ist
points = [[i, j, random.randrange(0, 2)] for i in range(res[0]) for j in range(res[1])]
# speichert alle Sticks, mit den beiden Punkten mit denen sie verbunden sind
sticks = []

# speichert die Geschwindigkeit von den einzelnen Punkten mit Betrag und Richtung
speed = [[0, 0] for i in range(len(points))]
# speichert für jeden Stick die Länge wenn er erstellt wird
Stick_Länge = []

print('The pain has begun')

def show_alles():
    print('--------------------------------------')
    print(speed)
    print('--------------------------------------')


# rendert den gesamten Screen, hat nichts mit der Physik zu tun
def render(modus, fps):
    screen.fill(Hintergrundcol)

    for i in range(len(sticks)):  # jeder Stick soll gerendert werden
        try:
            # zeichnet eine Linie zwischen den Punkten die verbunden sind
            pygame.draw.line(screen, Stickcol, (points[sticks[i][0]][0], points[sticks[i][0]][1]), (points[sticks[i][1]][0], points[sticks[i][1]][1]), 4)
        except:
            pass

    for i in range(len(points)):  # rendert die Punkte über den Sticks
        a, b = points[i][0], points[i][1]
        if points[i][2] == 0:  # normalen Punkt anzeigen
            pygame.draw.circle(screen, Punktcol, (a, b), 1)
        elif points[i][2] == 1:  # gefixten Punkt anzeigen
            pygame.draw.circle(screen, Punktfcol, (a, b), 1)

        # den Namen links oberhalb von dem Punkt anzeigen
        #img = font.render(str(i), True, RED)

        #screen.blit(img, (a - 10, b - 40))

    if modus:
        pygame.draw.circle(screen, GREEN, (22, 20), 20)
    else:
        pygame.draw.circle(screen, RED, (20, 20), 20)

    # fps rendern
    img = font.render('FPS: ' + str(fps), True, RED)
    screen.blit(img, (0, 50))

    pygame.display.update()


# löscht alles an Punkten/Verbindungen was bis jetzt vorhanden ist
def wipe():
    global points, sticks, speed
    points, sticks, speed = [], [], []


# bildet den tan hoch -1 von einem x und gibt diesen als float zurück
def intan(x):
    return math.atan(math.radians(x))


# bildet den cos hoch -1 von x und gibt dieses als float zurück, wenn man mehr als 180 Grad erwartet, wird das ergebnis %180 zurückgegeben
def incos(x):  # wurde getestet
    if x > 1:  # manchmal entstehen durch das runden falsche Werte
        x = 1
    elif x < -1:
        x = -1
    return math.degrees(math.acos(x))


def insinus(x):  # wurde getestet
    if x > 1:  # manchmal entstehen durch das runden falsche Werte
        x = 1
    elif x < -1:
        x = -1
    return math.degrees(math.asin(x))


def cos(x):
    return math.cos(math.radians(x))


def sin(x):
    return math.sin(math.radians(x))


# zeigt oben Links die FPS mit denen die Simulation momentan gerendert wird
def calc_FPS(last_time):
    Time = time.time()

    differenz = Time - last_time

    if differenz != 0:
        fps = 1 / differenz
        fps = (fps // 10) * 10
    else:
        fps = 'alle'

    return Time, fps


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


# entfernt einen beliebigen Punkt aus dem System
def delete_point(Punkt):
    print('Punkt 0 wird gelöscht ')
    for j in range(len(sticks)):
        i = 0
        while i < len(sticks):  # alle Sticks an denen der Punkt beteiligt ist entfernen
            if Punkt in sticks[i]:
                sticks.remove(sticks[i])

            i += 1

    for i in range(len(sticks)):  # alle Nachfolgenden Punkte haben ihren Namen geändert -> müssen in Sticks auch geändert werden
        if sticks[i][0] > Punkt:
            sticks[i][0] -= 1
        if sticks[i][1] > Punkt:
            sticks[i][1] -= 1

    speed.remove(speed[Punkt])  # die Geschwindigkeit von dem Punkt entfernen

    points.remove(points[Punkt])


# ist um die Standardlänge von einem neuen Stick zu ermitteln
def get_sticklänge(stick):  # Teststatus: Funktion wurde komplett getestet und funktioniert
    A = [points[sticks[stick][0]][0], points[sticks[stick][0]][1]]  # Koordinaten von Punkt 1
    B = [points[sticks[stick][1]][0], points[sticks[stick][1]][1]]  # Koordinaten von Punkt 2

    a = abs(A[0] - B[0])  # Abstand auf der X-Achse
    b = abs(A[1] - B[1])  # Abstand auf der Y-Achses

    return math.sqrt(a**2 + b**2)


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


#  berechnet Kraft von einem Stick der gestreckt/zusammengedrückt wird
#  es muss der Stick angegeben werden auf den die Kraft wirkt
def get_stickforce(stick, D, point_of_attack):  # Teststatus: Funkion wurde komplett getestet und funktioniert  TODO: beim zusammendrücken testen
    F = abs(get_sticklänge(stick) - Stick_Länge[stick]) * D   # berechnet den Betrag der Kraft

    A = [points[sticks[stick][0]][0], points[sticks[stick][0]][1]]  # Koordinaten von Punkt 1
    B = [points[sticks[stick][1]][0], points[sticks[stick][1]][1]]  # Koordinaten von Punkt 2

    if A[0] != points[point_of_attack][0] and A[1] != points[point_of_attack][1]:  # damit mit A immer als der Punkt ausgehende Punkt gerechnet werden kann
        B = A
        A = points[point_of_attack]

    # Seiten in einem Dreieck
    a = abs(A[0] - B[0])
    b = abs(A[1] - B[1])
    c = math.sqrt(a ** 2 + b ** 2)

    alpha = insinus(a / c)
    if A[0] > B[0]:  # zweiter Punkt ist im 2. oder 3. Quadranten relativ zum 1. Punkt -> ist nicht richtig berechnet
        alpha = 180 + abs(alpha)

    return [F, alpha]


def move_points():  # TODO: Funktion testen/debuggen
    global speed, points
    time.sleep(0.001)
    D = 1  # Stärke der Federn der Sticks
    g = [9.81, 0]

    for i in range(len(points)):
        if points[i][2] == 0:  # wenn der Punkt nicht gelockt ist
            beteiligte_sticks = []  # speichert alle Sticks an denen der Punkt irgendwie befestigt ist
            for j in range(len(sticks)):
                if i in sticks[j]:
                    beteiligte_sticks.append(j)

            force = [0, 0]
            for j in range(len(beteiligte_sticks)):  # berechnet die Kraft von momentaner Kraft und jedem Stick
                force = get_force(force, get_stickforce(beteiligte_sticks[j], D, i))
                force[1] = force[1] % 360
                force[1] = force[1] // 1

            force = get_force(force, g)  # berechnet Kraft mit der Gravitation
            force[1] = force[1] % 360
            force = get_force(force, speed[i])  # berechnet Kraft mit letzter Geschwindigkeit

            force[1] = force[1] % 360
            speed[i] = force  # Geschwindigkeit wird so hingesetzt



    # TODO: nachdem jeder Stick eine Geschwindigkeit bekommen hat muss jeder auch noch bewegt werden
    # als erstes muss herausgefunden werden in welchem Quadrant relativ zur jetztigen Position sich die neue Position befindet
    '''
    Quadraten:
    32
    41
    (alter Punkt ist in der Mitte)
    '''

    for i in range(len(speed)):
        speed[i][0] /= 100
        speed[i][1] = speed[i][1] % 360

    # Loop für alle Punkte mit ihren Geschwindigkeiten
    for i in range(len(points)):  # Teststatus für den Loop: wurde soweit getestet und funktioniert
        if speed[i][1] == 0:  # Sonderfall senkrecht nach unten
            points[i][1] += speed[i][0]
        elif (speed[i][1] - 90) == 0:  # Sonderfall waagerecht nach rechts
            points[i][0] += speed[i][0]
        elif (speed[i][1] - 180) == 0:  # Sonderfall senkrecht nach oben
            points[i][1] -= speed[i][0]
        elif (speed[i][1] - 270) == 0:  # Sonderfall waagerecht nach links
            points[i][0] -= speed[i][0]
        else:  # die generellen Fälle (treten eigentlich immer auf)
            if (speed[i][1] - 90) < 0:  # erster Quadrant
                points[i][0] += speed[i][0] * sin(speed[i][1])       # X Koordinate
                points[i][1] += speed[i][0] * sin(90 - speed[i][1])  # Y Koordinate
            elif (speed[i][1] - 180) < 0:  # zweiter Quadrant
                points[i][0] += speed[i][0] * sin(180 - speed[i][1])  # X Koordinate
                points[i][1] -= speed[i][0] * sin(270 - speed[i][1])  # Y Koordinate
            elif (speed[i][1] - 270) < 0:  # dritter Quadrant
                points[i][0] -= speed[i][0] * sin(speed[i][1] - 180)         # X Koordinate
                points[i][1] -= speed[i][0] * sin(90 - (speed[i][1] - 180))  # Y Koordinate
            else:  # vierter Quadrant
                points[i][0] -= speed[i][0] * sin(speed[i][1] - 270)            # X Koordinate
                points[i][1] += speed[i][0] * sin(90 - (speed[i][1] - 270))     # Y Koordinate
    return


counter = 0
y = 0
z = 0
FPS = 1
# TODO: aus irgendeinem Grund können Punkte die bewegt wurde nicht mehr zu Sticks hinzugefügt werden
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
                speed.append([0, 0])
            elif state[2]:  # rechter Mousebutton -> gefixter Punkt soll hinzugefügt werden
                points.append([x, y, 1])
                speed.append([0, 0])
            elif state[1]:  # mittlerer Mousebutton wurde gedrückt, soll die Möglichkeit geben 2 Punkte mit einem Seil zu verbinden/trennen
                Punkt, test = detect_point(x, y)
                print(Punkt )

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

                        selected = -1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Mode = not Mode
            elif event.key == pygame.K_c:
                wipe()
            elif event.key == pygame.K_1:
                show_alles()

    if Mode:
        move_points()

    if FPS != 'alle' and FPS != 0:
        if counter % int(FPS) == 0:
            Zeit, FPS = calc_FPS(Zeit)
        else:
            Zeit, Trash = calc_FPS(Zeit)
    else:
        if counter % 1000 == 0:
            Zeit, FPS = calc_FPS(Zeit)
        else:
            Zeit, Trash = calc_FPS(Zeit)

    render(Mode, FPS)

    counter += 1