"""
r = die daten aus der datei save_file.txt einlesen
s = die daten in die datei save_file.txt schreiben
e + Maus auf Person richten = diese Person mit allen bestehenden Beziehungen entfernen
linksklick auf eine person = diese person wird ausgewählt
rechtsklick danach = vorher ausgewählt person wird an diese position gesetzt

Kompletter Ablauf für das Erstellen einer Grafik
1. scale auf 1 setzen
2. die personen mit ihren beziehungen alle so anordnen, bis es einem gefällt
2. die Personen so erstellen wie man will (Mausrad reindrücken)
2. die Beziehungen so einstellen wie man will (Rechtsklick auf beide Personen)
3. speichern
4. Screenshot machen (a drücken)
5. für mögliche Änderungen das Programm neustarten

wichtig!!!
nach dem Erstellen von einem Bild, welches behalten werden soll, muss dieses sofort umbenannt/woanders gespeichert werden
(sonst wird es wohlmöglich gleich danach überschrieben)
"""
import random
import sys
import time
import pygame

# muss erhöht werden, für das skalieren (siehe TO DO oben, maximum ist 8)
scale = 1

pygame.init()

screen = pygame.display.set_mode((1920 * scale, 1080 * scale))
font = pygame.font.SysFont(None, 20 * scale)

Personen = ['Cooper', 'Coopers Tochter', 'Coopers Sohn', 'Coopers Vater']
# Beziehungen können von -100 bis 100 gehen (höher = bessere Beziehung, 0 = neutral)
Beziehungen = [[0, i, random.randrange(-100, 101), random.randrange(-100, 101)] for i in range(1, 4)]
Positionen = [[random.randrange(0, 1920), random.randrange(0, 1080)] for i in range(len(Personen))]
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
    render_legende()
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


def render_legende():
    # pygame.draw.rect(screen, (50, 50, 50), (0, (1080 - 100) * scale, 300 * scale, 100 * scale))

    # print_only_text('Legende', [120 * scale, (1080 - 95) * scale])

    # TODO: die Legende vervollständigen!

    pass


# Beginn von Speicher/Lesen=============================================================================================
def save_to_file(file):
    print('Änderungen wurden in ' + file + ' gespeichert.')
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


# Beginn von Person/Beziehung hinzufügen/entfernen======================================================================
def add_person(x, y):
    global Personen, Positionen
    print_text('Bitte gib den Namen der Person ein', (x, y))
    status = True
    name = ''

    while status:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                state = pygame.mouse.get_pressed()
                if state[0]:
                    status = False
            elif event.type == pygame.KEYDOWN:
                name += event.unicode
    screen.fill((0, 0, 0))
    pygame.display.update()
    render_all(screen)
    if name not in Personen and name != '':
        Personen.append(name)
        Positionen.append([x, y])
    else:
        print_text('Bei diesem Name ist ein Fehler aufgetreten', (x, y))
        time.sleep(3)
    screen.fill((0, 0, 0))
    pygame.display.update()
    return


def remove_person(person):
    global Personen, Beziehungen, Positionen
    Positionen.pop(person)

    beziehungen_neu = []
    for i in range(len(Beziehungen)):  # Beziehungen entfernen
        if i in range(len(Beziehungen)):
            if person != Beziehungen[i][0] and person != Beziehungen[i][1]:
                if Beziehungen[i][0] > person:
                    Beziehungen[i][0] -= 1
                if Beziehungen[i][1] > person:
                    Beziehungen[i][1] -= 1
                beziehungen_neu.append(Beziehungen[i])
    Beziehungen = beziehungen_neu.copy()

    screen.fill((0, 0, 0))
    Personen.remove(Personen[person])


def add_beziehung(pers1, pers2, position):
    neu = [pers1, pers2, '', '']

    print_text('Gib die Beziehung von ' + Personen[pers1] + ' zu ' + Personen[pers2] + ' ein.', position)
    status = True
    while status:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    if neu[2] != 'keine' and neu[2] != 'k':
                        neu[2] = int(neu[2])
                    status = False
                except:
                    neu[2] = ''
                    print_text('Fehler bei der Eingabe, versuche es erneut.', position)
                    time.sleep(2)
            elif event.type == pygame.KEYDOWN:
                neu[2] += event.unicode

    print_text('Gib die Beziehung von ' + Personen[pers2] + ' zu ' + Personen[pers1] + ' ein.', position)
    status = True
    while status:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    if neu[3] != 'keine' and neu[3] != 'k':
                        neu[3] = int(neu[3])
                    status = False
                except:
                    neu[3] = ''
                    print_text('Fehler bei der Eingabe, versuche es erneut.', position)
                    time.sleep(2)
            elif event.type == pygame.KEYDOWN:
                neu[3] += event.unicode
    if type(neu[2]) is int:
        if neu[2] > 100:
            neu[2] = 100
        elif neu[2] < -100:
            neu[2] = -100

    if type(neu[3]) is int:
        if neu[3] > 100:
            neu[3] = 100
        elif neu[3] < -100:
            neu[3] = -100
    Beziehungen.append(neu)
    return


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


def print_text(text, pos):
    text = font.render(text, True, (100, 100, 100))
    screen.fill((0, 0, 0))
    render_all(screen)
    screen.blit(text, pos)
    pygame.display.update()


def print_only_text(text, pos):
    text = font.render(text, True, (100, 100, 100))
    screen.blit(text, pos)


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
PersonenFuerBeziehung = []
while True:
    render_all(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            x, y = pygame.mouse.get_pos()  # falls eine Person entfernt werden soll
            pos = [x, y]

            if event.key == pygame.K_s:
                save_to_file('save_file.txt')
            elif event.key == pygame.K_r:
                read_file('save_file.txt')
            elif event.key == pygame.K_a:
                make_screenshot('test.png')
            elif event.key == pygame.K_e and get_person(pos) is not None:
                print('Person ' + Personen[get_person(pos)] + ' wird entfernt!')
                remove_person(get_person(pos))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            pos = [x, y]
            state = pygame.mouse.get_pressed()

            if state[1]:
                add_person(pos[0], pos[1])
            elif state[2] and get_person(pos) is not None:
                if len(PersonenFuerBeziehung) != 2:
                    PersonenFuerBeziehung.append(get_person(pos))
                if len(PersonenFuerBeziehung) == 2:
                    add_beziehung(PersonenFuerBeziehung[0], PersonenFuerBeziehung[1], pos)
                    PersonenFuerBeziehung = []
            else:
                if Ausgewaehlte_Person is None:
                    Ausgewaehlte_Person = get_person(pos)
                else:
                    Positionen[Ausgewaehlte_Person] = pos
                    Ausgewaehlte_Person = None
                    screen.fill((0, 0, 0))
                    pygame.display.update()
        elif event.type == pygame.MOUSEMOTION and Ausgewaehlte_Person is not None:
            Positionen[Ausgewaehlte_Person] = pygame.mouse.get_pos()
            screen.fill((0, 0, 0))


# TODO: die Farbe von der Beziehung ändert sich, wie man den Abstand hinzieht -> mann kann auch den Mittelpunkt verschieben und soe die Farben einzeln direkt steuern
