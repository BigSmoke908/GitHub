"""
r = die daten aus der datei save_file.txt einlesen
s = die daten in die datei save_file.txt schreiben
linksklick auf eine person = diese person wird ausgewählt
rechtsklick danach = vorher ausgewählt person wird an diese position gesetzt

Kompletter Ablauf für das Erstellen einer Grafik
1. scale auf 1 setzen
2. die personen mit ihren beziehungen alle so anordnen, bis es einem gefällt
3. speichern
4. das programm schließen
5. scale auf 8 setzten
6. programm starten und einen screenshot erstellen
7. fertig

wichtig!!!
nach dem Erstellen von einem Bild, welches behalten werden soll, muss dieses sofort umbenannt/woanders gespeichert werden
(sonst wird es wohlmöglich gleich danach überschrieben)
"""
import random
import sys
import pygame

# muss erhöht werden, für das skalieren (siehe TO DO oben, maximum ist 8)
scale = 1

pygame.init()

screen = pygame.display.set_mode((1920 * scale, 1080 * scale))
font = pygame.font.SysFont(None, 20 * scale)

Personen = ['Cooper', 'Coopers Tochter', 'Coopers Sohn', 'Coopers Vater']
# Beziehungen können von -100 bis 100 gehen (höher = bessere Beziehung, 0 = neutral)
Beziehungen = [[0, i, random.randrange(-100, 101), random.randrange(-100, 101)] for i in range(1, 4)]
Positionen = [[random.randrange(0, 1920), random.randrange(0, 1080)] for i in range(len(Personen))]  # erstmal zufällig

Ausgewaehlte_Person = None


# Beginn von Rendern====================================================================================================
def get_farbe(beziehung):
    # gibt eine gut aussehende Farbe basierend auf der Beziehung zurück
    if beziehung == 'keine' or beziehung == 'k':
        return [100, 100, 100]
    beziehung += 100
    beziehung /= 2
    return [-2.55 * beziehung + 255, 2.55 * beziehung, 50]


def render_all(surface):
    for i in Beziehungen:
        render_strich(i, surface)
    render_personen(surface)
    pygame.display.update()


def render_strich(strich, surface):
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

    pygame.draw.line(surface, tuple(farbe1), anfang, mitte, 5 * scale)
    pygame.draw.line(surface, tuple(farbe2), ende, mitte, 5 * scale)
    pygame.draw.circle(surface, farbe, mitte, 7 * scale)


def render_personen(surface):
    for person in range(len(Personen)):
        position = (Positionen[person][0]*scale, Positionen[person][1]*scale)
        pygame.draw.circle(surface, (200, 200, 125), position, 10 * scale)
    for person in range(len(Personen)):
        name = font.render(Personen[person], True, (200, 200, 125))
        size = list(name.get_rect())
        pygame.draw.rect(surface, (0, 0, 0), (Positionen[person][0]*scale, Positionen[person][1]*scale, size[2], size[3]))
        surface.blit(name, (Positionen[person][0]*scale, Positionen[person][1]*scale))


# Beginn von Speicher/Lesen=============================================================================================
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
            if Beziehungen[i][j] != 'keine' and Beziehungen[i][j] != 'k':
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

    while len(Positionen) < len(Personen):
        Positionen.append([random.randrange(0, 1920), random.randrange(0, 1080)])
    screen.fill((0, 0, 0))
    pygame.display.update()


# Beginn von extras=====================================================================================================
def make_screenshot(file):
    global scale, font, screen
    scale = 8
    pygame.quit()
    pygame.init()
    screen = pygame.display.set_mode((1920*scale, 1080*scale))
    font = pygame.font.SysFont(None, 20 * scale)
    render_all(screen)
    pygame.image.save(screen, file)
    print(file + ' saved')
    pygame.quit()
    sys.exit()


# für Testzwecke, kann die RGB-Werte einer 2D List rendern
def render_liste(feld):
    for i in range(len(feld)):
        for j in range(len(feld[i])):
            pygame.draw.rect(screen, (feld[i][j]), (j, i, 1, 1))
    pygame.display.update()
    print("liste rendern fertig")


def get_person(pos):
    for i in Positionen:
        if i[0] - 15 < pos[0] < i[0] + 15 and i[1] - 15 < pos[1] < i[1] + 15:
            return Positionen.index(i)
    return None


# Beginn vom Mainloop===================================================================================================
read_file('save_file.txt')
while True:
    render_all(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_to_file('save_file.txt')
            elif event.key == pygame.K_r:
                read_file('save_file.txt')
            elif event.key == pygame.K_a:
                make_screenshot('test.png')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            pos = [x, y]
            state = pygame.mouse.get_pressed()

            if Ausgewaehlte_Person == None:
                Ausgewaehlte_Person = get_person(pos)
            elif Ausgewaehlte_Person != None:
                Positionen[Ausgewaehlte_Person] = pos
                Ausgewaehlte_Person = None
                screen.fill((0, 0, 0))
                pygame.display.update()
        elif event.type == pygame.MOUSEMOTION and Ausgewaehlte_Person is not None:
            Positionen[Ausgewaehlte_Person] = pygame.mouse.get_pos()
            screen.fill((0, 0, 0))


# TODO: eine Funktion, mit der man Personen/Beziehungen direkt über das Tool (ohne .txt Datei) hinzufügen kann
