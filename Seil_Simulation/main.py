import sys
import pygame
import math

pygame.init()

FK = (3840, 2160)
FHD = (1920, 1080)
UHD = (2560, 1440)
HD = (1080, 729)

screen = pygame.display.set_mode(UHD)

# bildet den tan hoch -1 von einem x und gibt diesen als float zurück
def intan(x):
    return math.degrees(math.atan(x))


# Farben
Punktcol = (120, 150, 200)
Punktfcol = (200, 80, 120)
Stickcol = (140, 180, 200)
Hintergrundcol = (50, 100, 170)

# pygame.draw.circle(screen, Punktcol, (2560, 1440), 20)
# zeigt einen Punkt an
Stick = pygame.image.load('stick.png')
#Stick = pygame.transform.scale(Stick, (4, 1000))
#Stick = pygame.transform.rotate(Stick, 90)
# verzerrt den Stick in jede gewünschte Form

x, y = 0, 0
# Mouseposition initialisiert

# speichert alle Punkte mit X und Y Koordinaten
# der dritte Wert ist 0 bie normalen Punkten und 1 wenn der Punkt gefixt ist
points = [[500, 500, 0], [700, 700, 0], [100, 600, 1]]
# speichert alle Sticks, mit den beiden Punkten mit denen sie verbunden sind
sticks = [[0, 1], [0, 2]]


def render():
    global Stick
    screen.fill(Hintergrundcol)

    for i in range(len(sticks)):  # jeder Stick soll gerendert werden
        try:
            a = points[sticks[i][0]][0] - points[sticks[i][1]][0]  # Abstand auf der X Koordinate
            b = points[sticks[i][0]][1] - points[sticks[i][1]][1]  # Abstand auf der Y Koordinate
            alpha = int(intan(a / b))
            c = abs(int(math.sqrt(a ** 2 + b ** 2)))  # Länge der Hypotenuse
            StickIMG = pygame.transform.scale(Stick, (4, c))  # zieht den Stick auf die richtige Länge
            StickIMG = pygame.transform.rotate(StickIMG, alpha)  # rotiert den Stick richtig hin

            screen.blit(StickIMG, (points[sticks[i][0]][0], points[sticks[i][0]][1]))
            #if points[sticks[i][0]][0] < points[sticks[i][2]][0]:

            del StickIMG
        except:
            pass

    for i in range(len(points)):  # rendert die Punkte
        a, b = points[i][0], points[i][1]
        if points[i][2] == 0:  # normalen Punkt anzeigen
            pygame.draw.circle(screen, Punktcol, (a, b), 10)
        elif points[i][2] == 1:  # gefixten Punkt anzeigen
            pygame.draw.circle(screen, Punktfcol, (a, b), 10)

    pygame.display.update()


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

    screen.blit(Stick, (500, 500))

    render()
