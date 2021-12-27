from pynput.keyboard import Key, Controller
import time

keyboard = Controller()
Link = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley'
time.sleep(2)

def typIn(text):
    for char in text:
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(0.02)

def pressOnce(letter):
    keyboard.press(letter)
    keyboard.release(letter)

def Rickroll():
    keyboard.press(Key.cmd)
    keyboard.release(Key.cmd)
    time.sleep(0.1)
    typIn('firefox')

    time.sleep(0.5)

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    time.sleep(1)

    keyboard.press(Key.ctrl)
    pressOnce('t')
    pressOnce('1')
    pressOnce('w')
    keyboard.release(Key.ctrl)

    typIn(Link)

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(1)
    keyboard.press(Key.space)
    keyboard.release(Key.space)



Rickroll()