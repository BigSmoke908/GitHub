# TODO: später nicht in 4k sondern 24k oder irgendwie sowas absurd hohem rendern -> Screenshot danach runterskalieren
# (sollte weichere Kanten erzeugen)
import random
import sys
import time
import pygame

# kann erhöht werden, für das skalieren (siehe TO DO oben)
scale = 1

pygame.init()

screen = pygame.display.set_mode((2560, 1440))
font = pygame.font.SysFont(None, 20 * scale)

# kann zu einer Person später vielleicht auch noch ein Bild enthalten
Personen = [['Cooper'], ['Coopers Tochter'], ['Coopers Sohn'], ['Coopers Vater']]
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

    pygame.draw.line(screen, tuple(farbe1), anfang, mitte, 5 * scale)
    pygame.draw.line(screen, tuple(farbe2), ende, mitte, 5 * scale)
    pygame.draw.circle(screen, farbe, mitte, 7 * scale)


def render_personen():
    for person in range(len(Personen)):
        pygame.draw.circle(screen, (200, 200, 125), tuple(Positionen[person]), 10 * scale)
    for person in range(len(Personen)):
        name = font.render(Personen[person][0], True, (200, 200, 125))
        size = list(name.get_rect())
        pygame.draw.rect(screen, (0, 0, 0), (Positionen[person][0], Positionen[person][1], size[2], size[3]))
        screen.blit(name, Positionen[person])


def make_screenshot(file):
    pygame.image.save(screen, file)
    print(file + ' saved')


while True:
    render_all()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            make_screenshot('test.png')
