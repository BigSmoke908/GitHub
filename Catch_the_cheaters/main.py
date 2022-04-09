import math
import matplotlib.pyplot as plt
import random


# in der Variable coins, stehen erst heads (häufiger bei cheatern) dann die Tails (seltener bei cheatern)


# gibt die Wahrscheinlichkeit von dem Ereignis zurück
def get_wahrscheinlichkeit_fair(ereignis):
    n = ereignis[0] + ereignis[1]
    return (math.factorial(n)/(math.factorial(ereignis[0]) * math.factorial(ereignis[1]))) * (0.5**n)


def get_wahrscheinlichkeit_cheater(ereignis):
    n = ereignis[0] + ereignis[1]
    x = ereignis[0]
    y = ereignis[1]
    return (math.factorial(n)/(math.factorial(x) * math.factorial(y))) * (0.75**x) * (0.25**y)


def durchschnitt(elemente):
    summe = 0
    for zahl in elemente:
        summe += zahl
    return summe/len(elemente)


def cheater(coins):
    coin = random.randrange(1, 5)
    if coin == 4:
        coins[1] += 1
        return coins
    coins[0] += 1
    return coins


# spielt fair -> tut immer einfach immer bei einer zufälligen Münze mehr rein
def fair(coins):
    coins[random.randrange(0, 2)] += 1
    return coins


def simulate_game(wuerfe):
    richtige = 0

    for i in range(100):
        player = random.randrange(0, 2)
        trys_left = wuerfe
        coins = [0, 0]
        cheaten = []
        fairplay = []
        while trys_left > 0:
            # neuer Münzwurf
            if player == 0:
                coins = fair(coins)
            elif player == 1:
                coins = cheater(coins)
            trys_left -= 1

            cheaten.append(get_wahrscheinlichkeit_cheater(coins))
            fairplay.append(get_wahrscheinlichkeit_fair(coins))

        if get_wahrscheinlichkeit_fair(coins) < get_wahrscheinlichkeit_cheater(coins):
            vermutung = 1
        else:
            vermutung = 0

        if vermutung == player:
            richtige += 1
    return richtige


def draw_graph(verlauf1, verlauf2, player):
    plt.plot([i for i in range(len(verlauf1))], verlauf1, label='Fair')
    plt.plot([i for i in range(len(verlauf2))], verlauf2, label='Gecheated')

    plt.xlabel('Münzwürfe')
    plt.ylabel('Wahrscheinlichkeit')
    if player == 0:
        plt.title('Fair gespielt')
    else:
        plt.title('Unfair gespielt')

    plt.show()


def full_sim(strat):
    wuerfe = 100
    coins = [0, 0]
    player = random.randrange(0, 2)
    jetzige_wuerfe = 0
    gewonnen = 0
    counter = 0

    while wuerfe > 0:
        # neuer Wurf
        if player == 0:
            coins = fair(coins)
        else:
            coins = cheater(coins)

        jetzige_wuerfe += 1
        wuerfe -= 1
        counter += 1
        if jetzige_wuerfe == strat:
            faire = get_wahrscheinlichkeit_fair(coins)
            unfair = get_wahrscheinlichkeit_cheater(coins)
            if faire > unfair and player == 0:
                wuerfe += 15
                gewonnen += 1
            elif faire < unfair and player == 1:
                wuerfe += 15
                gewonnen += 1
            else:
                wuerfe -= 30
            jetzige_wuerfe = 0
            coins = [0, 0]

        if counter%1000 == 0:
            print(wuerfe)
    return gewonnen

"""
Ertrag = []
for Wuerf in range(1, 10):
    Richtigkeit = []
    Wuerfe = 4
    for alle in range(500):
        Richtigkeit.append(simulate_game(Wuerfe))

    quote = durchschnitt(Richtigkeit)
    gewinn = (quote * (15 - Wuerfe)) + ((100 - quote) * -(30 + Wuerfe))
    Ertrag.append([Wuerfe, gewinn])
    print(Wuerfe)
"""

Gewinne = []

for i in range(5000):
    Gewinne.append(full_sim(3))

print(max(Gewinne))
print(durchschnitt(Gewinne))
