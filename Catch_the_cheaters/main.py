import datetime
import functools
import math
import time
from multiprocessing import Pool
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


def draw_graph(verlauf1, verlauf2, verlauf3, verlauf4, player):
    plt.plot([i for i in range(len(verlauf1))], verlauf1, label='Fair')
    plt.plot([i for i in range(len(verlauf2))], verlauf2, label='Gecheated')
    plt.plot([i for i in range(len(verlauf3))], verlauf3, label='Heads')
    plt.plot([i for i in range(len(verlauf4))], verlauf4, label='Tails')

    plt.xlabel('Münzwürfe')
    plt.ylabel('Wahrscheinlichkeit')
    if player == 0:
        plt.title('Fair gespielt')
    elif player == 1:
        plt.title('Unfair gespielt')
    else:
        plt.title('Keine Angabe zur Spielweise')

    plt.show()


# berechnet eine Score, für wie stark die Gewinnwahrscheinlichkeit bei einer bestimmten Vermutung demnächst steigt
# (Score setzt sich aus dem möglichem Gewinn und der Wahrscheinlichkeit dafür zusammen)
def get_score(coins, vermutung):
    n = sum(coins)
    möglicher_gewinn = 15 + n
    möglicher_verlust = (30 + n) * -1
    if vermutung == 0:
        p = get_wahrscheinlichkeit_fair(coins)
    else:
        p = get_wahrscheinlichkeit_cheater(coins)
    return (p * möglicher_gewinn) + ((1 - p) * möglicher_verlust)


# beendet das Spiel nach x würfen, nutzt danach die Wahrscheinlichkeit, als Indicator für die Wahl von dem Ergebnis
def strat1(strat):
    wuerfe = 100
    coins = [0, 0]
    player = random.randrange(0, 2)
    jetzige_wuerfe = 0
    gewonnen = 0

    while wuerfe > 0:
        # neuer Wurf
        if player == 0:
            coins = fair(coins)
        else:
            coins = cheater(coins)

        jetzige_wuerfe += 1
        wuerfe -= 1

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
            player = random.randrange(0, 2)
            coins = [0, 0]
    return gewonnen


# spielt solange, bis der Wahrscheinliche Profit zu stark sinkt (strat == maximale Sinkrate zum vorherigen Score
# (max_depth == maximale Anzahl an Versuchen pro Blob gegenüber))
def strat2(strat, max_depth):
    wuerfe = 100
    coins = [0, 0]
    player = random.randrange(0, 2)
    gewonnen = 0
    momentane_versuche = 0
    durchschnittliche_versuche = []

    while wuerfe > 0:
        vscore_fair = get_score(coins, 0)
        vscore_cheat = get_score(coins, 1)

        pfair = get_wahrscheinlichkeit_fair(coins)
        pcheat = get_wahrscheinlichkeit_cheater(coins)

        if pfair > pcheat:  # wenn cheaten wahrscheinlicher ist
            neu1 = [coins[0] + 1, coins[1]]
            neu2 = [coins[0], coins[1] + 1]
            if get_score(coins, 1) + strat > (get_score(neu1, 1) * 0.75) + (get_score(neu2, 1) * 0.25) or momentane_versuche == max_depth:  # wenn die chance als nächstes zu stark sinkt
                if player == 1:
                    gewonnen += 1
                    wuerfe += 15
                else:
                    wuerfe -= 30
                durchschnittliche_versuche.append(momentane_versuche)
                momentane_versuche = 0
                player = random.randrange(0, 2)

        else:  # wenn fair spielen wahrscheinlicher ist
            neu1 = [coins[0] + 1, coins[1]]
            neu2 = [coins[0], coins[1] + 1]
            if get_score(coins, 0) + strat > (get_score(neu1, 0) + get_score(neu2, 0)) * 0.5 or momentane_versuche == max_depth:  # wenn die chane als nächstes zu stark sinkt
                if player == 0:
                    gewonnen += 1
                    wuerfe += 15
                else:
                    wuerfe -= 30
                durchschnittliche_versuche.append(momentane_versuche)
                momentane_versuche = 0
                player = random.randrange(0, 2)

        # neuer Wurf
        if player == 0:
            coins = fair(coins)
        else:
            coins = cheater(coins)
        wuerfe -= 1
        momentane_versuche += 1


def beide(ereignis):
    print(get_wahrscheinlichkeit_fair(ereignis))
    print(get_wahrscheinlichkeit_cheater(ereignis))
    print(get_score(ereignis, 0))
    print(get_score(ereignis, 1))


def call_x_times(strat):
    begin = time.time()
    res = [strat1(strat) for spiele in range(100000)]
    return [durchschnitt(res), max(res), strat, time.time() - begin]


# analysiert, bei nach wie vielen x, man am besten aufhören kann (benutzt Multiprocessing)
def analyse():
    alle_Gewinne = []
    p = Pool()
    Input = [i for i in range(1, 16)]

    #func = functools.partial(call_x_times, maxdepth=4)
    ergebnis = p.map(func=call_x_times, iterable=[i for i in range(0, 200)])

    p.close()
    p.join()

    print('Mp wurde abgeschlossen.')

    neu = []
    timing = []
    while len(ergebnis) != len(neu):
        for i in ergebnis:
            if i[2] == len(neu):
                neu.append(i)
                timing.append(i[3])
    print('Zeichnen wurde begonnen->')
    print('Ein Prozess hat im Durchschnitt ' + str(durchschnitt(timing)) + 's gedauert.')
    draw_graph([neu[i][0] for i in range(len(neu))], [neu[i][1] for i in range(len(neu))], [], [], None)
    # [neu[i][0] for i in range(len(neu))]

    for i in neu:
        print(i)


'''
Test_Coins = [0, 0]
Coin_speicher = []
Faireplay = []
Cheaten = []
for Test in range(1, 100):
    Wurf = random.randrange(0, 4)
    if Wurf == 3:
        Test_Coins[1] += 1
    else:
        Test_Coins[0] += 1
    Faireplay.append(get_score(Test_Coins, 0, None))
    Cheaten.append(get_score(Test_Coins, 1, None))
    Coin_speicher.append(Test_Coins.copy())

Heads = [Coin_speicher[i][0] for i in range(len(Coin_speicher))]
Tails = [Coin_speicher[i][1] for i in range(len(Coin_speicher))]

draw_graph(Faireplay, Cheaten, Heads, Tails, None)
'''


if __name__ == '__main__':
    analyse()
