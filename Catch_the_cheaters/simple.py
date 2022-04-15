import sys
import pyautogui
from pyautogui import *
from pyautogui import locateCenterOnScreen as search
import time
import keyboard
import random
import win32api, win32con
from main import get_wahrscheinlichkeit_fair as fair
from main import get_wahrscheinlichkeit_cheater as cheater


def click(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


# Klickt bei den jeweiligen Coins, auf das entsprechende Feld
def strat(coins):
    global schlafenszeit
    fair_gespielt = int(fair(coins) * 100)
    unfair = int(cheater(coins) * 100)

    if unfair < fair_gespielt:
        rating = search('fair.png')
        print('Fair gespielt')
        while rating is None:
            rating = search('fair.png')
        click(rating[0], rating[1])
    else:
        rating = search('cheater.png')
        print('GECHEATED!!!')
        while rating is None:
            rating = search('cheater.png')
        click(rating[0], rating[1])

    schlafenszeit = random.randrange(10, 21)/10
    time.sleep(schlafenszeit)


gewinne_durchschnitt = []  # enthält die Anzahl von allen Runden, je gespielt
gewinne = 0  # enthält die Anzahl von den Runden momentan
nicht_geflippt = True  # MUSS AM ANFANG UNBEDINGT TRUE SEIN!!!!
schlafenszeit = 0

time.sleep(2)
print('Looking for Cheaters now...')

while not keyboard.is_pressed('x'):
    time.sleep(4)
    submit = search('submit.png')  # gucken ob das Spiel zuende ist
    if submit is not None:
        click(submit[0], submit[1])

        time.sleep(random.randrange(1, 10)/10)
        reset = search('reset.png')
        while reset is None:
            reset = search('reset.png')
        click(reset[0], reset[1])

        time.sleep(1)

    # EIGENTLICHES SPIEL
    time.sleep(random.randrange(5, 20)/10)  # laden abwarten

    if nicht_geflippt or True:
        flip = search('flip5.png', confidence=0.8)
        if flip is not None:
            click(flip[0], flip[1])
            nicht_geflippt = False
    else:
        f = open('log.txt', 'a')
        f.write('\nFehler ist aufgetreten. Datum: ' + str(datetime.datetime.now()) + '||' + str(schlafenszeit))
        screenshot('error.png')
        sys.exit('Es konnte keine Zahl erkannt werden.\nSchlafzeit = ' + str(schlafenszeit))

    time.sleep((random.randrange(0, 10))//10)

    zwei = search('2.png', confidence=0.9)
    if zwei is None:
        zwei = search('22.png', confidence=0.9)
        if zwei is None:
            zwei = search('23.png', confidence=0.9)

    if zwei is not None:  # 2 und 3 sind auf dem Screen
        drei = search('3.png', confidence=0.9)
        if drei is None:
            drei = search('32.png', confidence=0.9)
            if drei is None:
                drei = search('33.png', confidence=0.9)

        if drei[1] < zwei[1]:  # Heads=2, Tails=3
            strat([3, 2])
        else:
            strat([2, 3])
        nicht_geflippt = True
    else:
        eins = search('1.png', confidence=0.9)
        if eins is not None:  # 1 und 4 sind auf dem Screen
            vier = search('4.png', confidence=0.9)
            if vier[1] < eins[1]:
                strat([4, 1])
            else:
                strat([1, 4])
            nicht_geflippt = True
        else:
            null = search('0.png', confidence=0.9)
            if null is not None:  # 0 und 5 sind auf dem Screen
                fuenf = search('5.png', confidence=0.9)
                if fuenf[1] < null[1]:
                    strat([5, 0])
                else:
                    strat([0, 5])
                nicht_geflippt = True

# spEeDrUnnEr