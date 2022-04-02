# TODO: später nicht in 4k sondern 24k oder irgendwie sowas absurd hohem rendern -> Screenshot danach runterskalieren
# (sollte weichere Kanten erzeugen)
import random
import sys
import time
import pygame

# kann erhöht werden, für das skalieren (siehe TO DO oben, maximum ist 8)
scale = 8

pygame.init()

screen = pygame.display.set_mode((1920 * scale, 1080 * scale))
font = pygame.font.SysFont(None, 20 * scale)

Personen = ['Cooper', 'Coopers Tochter', 'Coopers Sohn', 'Coopers Vater']
Namen = []
# Beziehungen können von -255 bis 255 gehen (höher = bessere Beziehung, 0 = neutral)
Beziehungen = [[0, i, random.randrange(-100, 101), random.randrange(-100, 101)] for i in range(1, 4)]
Positionen = [[random.randrange(0, 1920), random.randrange(0, 1080)] for i in range(len(Personen))]  # erstmal zufällig
next_Positionen = Positionen.copy()


# gibt eine gut aussehende Farbe basierend auf der Beziehung zurück
def get_farbe(beziehung):
    beziehung += 100
    beziehung /= 2
    return [-2.55 * beziehung + 255, 2.55 * beziehung, 50]


def render_all():
    for i in Beziehungen:
        render_strich(i)
    render_personen()
    pygame.display.update()


def render_strich(strich):
    anfang = Positionen[strich[0]]
    ende = Positionen[strich[1]]

    mitte = [(anfang[0] + ende[0]) // 2, (anfang[1] + ende[1]) // 2]

    farbe1 = get_farbe(strich[2])
    farbe2 = get_farbe(strich[3])
    farbe = [0, 0, 0]
    for i in range(3):
        farbe[i] = (farbe1[i] + farbe2[i]) / 2

    anfang = [anfang[0]*scale, anfang[1]*scale]
    mitte = [mitte[0]*scale, mitte[1]*scale]
    ende = [ende[0]*scale, ende[1]*scale]

    pygame.draw.line(screen, tuple(farbe1), anfang, mitte, 5 * scale)
    pygame.draw.line(screen, tuple(farbe2), ende, mitte, 5 * scale)
    pygame.draw.circle(screen, farbe, mitte, 7 * scale)


def render_personen():
    for person in range(len(Personen)):
        position = (Positionen[person][0]*scale, Positionen[person][1]*scale)
        pygame.draw.circle(screen, (200, 200, 125), position, 10 * scale)
    for person in range(len(Personen)):
        name = font.render(Personen[person], True, (200, 200, 125))
        size = list(name.get_rect())
        pygame.draw.rect(screen, (0, 0, 0), (Positionen[person][0]*scale, Positionen[person][1]*scale, size[2], size[3]))
        screen.blit(name, (Positionen[person][0]*scale, Positionen[person][1]*scale))


def save_to_file(file):
    print('Daten wurden in ' + file + ' gespeichert.')
    f = open(file, 'w')
    f.write('Personenbeginn\n')
    for i in Personen:
        out = ''
        for j in i:
            out += str(j)
        f.write(out + ' ||\n')
    f.write('Personenende\n\nBeziehungenbeginn\n')
    for i in Beziehungen:
        out = ''
        for j in i:
            out += str(j)
            out += '|'
        out += '| '
        f.write(out + '\n')
    f.write('Beziehungenende\n\nPositionenbeginn\n')
    for i in Positionen:
        out = ''
        for j in i:
            out += str(j) + '|'
        f.write(out + '|\n')
    f.write('Positionenende\n\n')
    f.close()


def read_file(file):
    global Personen, Beziehungen, Positionen
    f = open(file, 'r')
    gespeichert = f.read()
    f.close()

    # alles zurücksetzen
    Personen = []
    Beziehungen = []
    Positionen = []

    gespeichert = gespeichert.split()

    # Personen auslesen--------------------------
    while gespeichert[0] != 'Personenbeginn':  # Header Personen suchen
        gespeichert.remove(gespeichert[0])
    gespeichert.remove('Personenbeginn')
    while gespeichert[0] != 'Personenende':
        name = ''
        while gespeichert[0] != '||':
            name += gespeichert[0]
            if gespeichert[1] != '||':
                name += ' '
            gespeichert.remove(gespeichert[0])
        Personen.append(name)
        gespeichert.remove(gespeichert[0])
    gespeichert.remove(gespeichert[0])

    # Beziehungen auslesen----------------------
    while gespeichert[0] != 'Beziehungenbeginn':  # Header Beziehungen
        gespeichert.remove(gespeichert[0])
    gespeichert.remove(gespeichert[0])
    while gespeichert[0] != 'Beziehungenende':
        Beziehungen.append(gespeichert[0])
        gespeichert.remove(gespeichert[0])
    gespeichert.remove(gespeichert[0])

    for i in range(len(Beziehungen)):
        Beziehungen[i] = Beziehungen[i].split('|')
        while '' in Beziehungen[i]:
            Beziehungen[i].remove('')
        for j in range(len(Beziehungen[i])):
            Beziehungen[i][j] = int(Beziehungen[i][j])

    # Positionen auslesen------------------------
    while gespeichert[0] != 'Positionenbeginn':  # Header finden
        gespeichert.remove(gespeichert[0])
    gespeichert.remove(gespeichert[0])
    while gespeichert[0] != 'Positionenende':
        Positionen.append(gespeichert[0])
        gespeichert.remove(gespeichert[0])
    gespeichert.remove(gespeichert[0])
    for i in range(len(Positionen)):
        Positionen[i] = Positionen[i].split('|')
        while '' in Positionen[i]:
            Positionen[i].remove('')
        for j in range(len(Positionen[i])):
            Positionen[i][j] = int(Positionen[i][j])

    screen.fill((0, 0, 0))
    pygame.display.update()


def make_screenshot(file):
    pygame.image.save(screen, file)
    print(file + ' saved')


# für Testzwecke, kann die RGB-Werte einer 2D List rendern
def render_liste(feld):
    for i in range(len(feld)):
        for j in range(len(feld[i])):
            pygame.draw.rect(screen, (feld[i][j]), (j, i, 1, 1))
    pygame.display.update()
    print("liste rendern fertig")


while True:
    render_all()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_to_file('save_file.txt')
            elif event.key == pygame.K_r:
                read_file('save_file.txt')
            else:
                make_screenshot('test.png')

save_to_file()
read_file('save_file.txt')

# Feld = [[get_farbe((i / 19.2)) for i in range(1920)] for j in range(1440)]
# render_liste(Feld)
