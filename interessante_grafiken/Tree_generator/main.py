import random
import sys
import pygame
import math


pygame.init()
screen = pygame.display.set_mode((1920, 1080))
background = (220, 180, 180)  # TODO: einen Farbverlauf ermöglichen
background = (100, 70, 70)

baum = [[90, 1, -1], ['l', 0]]
astfarbe = (200, 200, 200)
renderbaum = []  # fürs rendern optimierter Baum

'''
Baum wird aus mehreren Ästen gebildet (baum = [...])
1 Ast -> [Richtung (0 bis 180°, gegen den Uhrzeigersinn, 0 ist rechts Mitte), Energielevel (wie viel Energie in diesen Ast noch kommt), Befestigung (Ast an dem er Befestigt ist)]
[Richtung, Energie, Befestigung]

(der erste Ast hat als Befestigung einen Zufälligen Punkt auf dem Boden, wird in der List durch -1 dargestellt, dieser ist immer am Anfang von der List)
am Ende der list gibt es eine list, mit allen Ästen, die ohne Verbindung einfach enden: (für wachsen von dem Baum hilfreich)
['l', index_ast0, index_ast1, index_ast2, ..., index_ast]

außerdem gibt es Möglichkeit diese list (äste) zu komprimieren
1 Ast -> [Beginn, Ende, Energielevel]
Vorteil -> muss nicht jedes Mal komplett neu berechnet werden -> ist hoffentlich deutlich schneller zu rendern
'''


# Beginn Hilfsfunktionen------------------------------------------------------------------------------------------------
# gibt den Sinus von dem Winkel X zurück
def sin(x):
    return math.sin(math.radians(x))


# gibt den Cosinus von dem Winkel X zurück
def cos(x):
    return math.cos(math.radians(x))


# nimmt die die gegebenen Maße von einem Ast -> gibt die Koordinaten von dem Endpunkt
def get_pos(begin, winkel, length):
    winkel = (winkel+180) % 360
    x = length * cos(winkel)
    y = length * sin(winkel)
    return [x + begin[0], y + begin[1]]


# nimmt einen Baum in der komplizierten Form -> konvertiert ihn zu der einfacheren renderbaren Form
def convert(tree):
    convertiert = []
    size = 2
    for ast in tree:
        length = ast[1] * size
        if ast[0] != 'l':
            if ast[2] == -1:
                begin = [1000, 980]
                convertiert.append([begin, get_pos(begin, ast[0], length), ast[1]])
            else:
                convertiert.append([convertiert[ast[2]][1], get_pos(convertiert[ast[2]][1], ast[0], length), ast[1]])
    return convertiert


def wurzel(x):
    return math.sqrt(abs(x))
# Ende Hilfsfunktionen--------------------------------------------------------------------------------------------------


# Beginn Wachstumsfunktionen--------------------------------------------------------------------------------------------
# nimmt den gesamten Baum, und setzt nach der gewollten Regel an jedes Ende Zweige an (Regel wird als Funktion übergeben
def add_zweige(regel):
    buffer_baum = baum

    for i in buffer_baum[-1]:
        if i != 'l':
            buffer_baum = regel(i, buffer_baum)
    return buffer_baum


# nimmt den Index von einem Ast an dem Baum -> setzt zwei y mäßig angeordnete Zweige an
def y_zweige(ast, tree):
    # die Werte von dem vorherigen Ast
    richtung_0 = tree[ast][0]
    energie_0 = tree[ast][1]

    zweig_1 = [richtung_0 + random.randrange(5, 40), energie_0 / 1.5, ast]
    zweig_2 = [richtung_0 - random.randrange(5, 40), energie_0 / 1.5, ast]

    lose_enden = tree[-1].copy()
    tree.remove(lose_enden)
    lose_enden.remove(ast)

    tree.append(zweig_1)
    tree.append(zweig_2)

    lose_enden.append(tree.index(zweig_1))
    lose_enden.append(tree.index(zweig_2))
    tree.append(lose_enden)

    return tree
# Ende Wachstumsfunktionen----------------------------------------------------------------------------------------------


# Beginn Renderfunktionen-----------------------------------------------------------------------------------------------
def render():
    screen.fill(background)
    pygame.draw.rect(screen, (0, 0, 0), (0, 980, 1920, 100))  # irgendein Boden TODO: Boden fancier machen

    for ast in renderbaum:
        pygame.draw.line(screen, astfarbe, (ast[0][0], ast[0][1]), (ast[1][0], ast[1][1]), 5)
    pygame.display.update()
# Ende Renderfunktionen-------------------------------------------------------------------------------------------------


# Beginn Naturfunktionen------------------------------------------------------------------------------------------------
def wiggle(tree):
    for ast in tree:
        if ast[0] != 'l':
            ast[0] += (1 * (random.randrange(0, 11) - 5)) / tree[ast][1]
    return tree
# Ende Naturfunktionen--------------------------------------------------------------------------------------------------


counter = 0
changes = False
renderbaum = convert(baum)
while True:
    if counter % 10 == 0 and counter != 0:
        if len(baum) < 2000:
            baum = add_zweige(y_zweige)
            changes = True
        if baum[0][1] < 30 and counter % 30 == 0 and counter != 0:
            for i in range(len(baum)):
                if baum[i][0] != 'l':
                    baum[i][1] += wurzel(baum[i][1])
                    changes = True

        #baum = wiggle(baum)

    if changes:
        renderbaum = convert(baum)
        changes = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    render()
    counter += 1
