from pynput.keyboard import Key, Controller
from selenium import webdriver as driver
from selenium.webdriver.common.keys import Keys
from time import sleep
import sys
from selenium.webdriver.common.by import By

keyboard = Controller()


Tasks = open('files/tasks.txt')
Tasks = Tasks.read()
Tasks = Tasks.split()

Links = open('files/links.txt')
Links = Links.read()
Links = Links.split()

# bereits abgschlossene Aufgaben, wird wenn alles abgeschlossen ist automatisch zurückgesetzt
Fertig = open('files/fertig.txt')
Fertig = Fertig.read()
Fertig = Fertig.split()

# fehlgeschlagene nicht beendete Aufgaben (wird ausgebenen und auch zurückgesetzt)
Failed = open('files/Failed.txt')
Failed = Failed.read()
Failed = Failed.split()


# Daten werden eingelesen und geprüft (auf gleiche Länge und ob die Aufgaben nur Zahlen sind)
for i in range(len(Tasks)):
    buffer = Tasks[i]
    Tasks[i] = buffer.split('_')
    for j in range(len(Tasks[i])):
        try:
            buffer = int(Tasks[i][j])
        except:
            print('Error: Die Taskeingabe ist fehlerhaft. Der Fehler ist bei: ' + buffer)
            sys.exit()

if len(Tasks) < len(Links):
    print('Error: Die Anzahl der gegebenen Aufgaben ist geringer als die Anzahl der gegebenen Links')
    sys.exit()
elif len(Tasks) > len(Links):
    print('Error: Die Anzahl der gegebenen Aufgaben ist höher als die Anzahl der gegebenen Links')
    sys.exit()
# alle Eingaben sind überprüft -> das Browserfenster wird geöffnet

fenster = driver.Firefox()
fenster.get('https://gheed.com')
print('bitte logge dich ein, drücke danach ENTER in der Konsole')
input()


for i in range(len(Tasks)):
    fenster.get('https://gheed.com/giveaways/g-' + Links[i])

    sleep(2)
    button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[1]/div/div[6]/div/div/button[2]/span[1]')
    button.click()
    # zu Aufgaben wechseln

    for j in range(len(Tasks[i])):
        finished = False  # ob die jeweilige Aufgabe bereits geöffnet wurde
        while not finished:
            try:
                xpath = '/html/body/div[1]/div/div[2]/div/div[1]/div/div[7]/div[2]/div[' + Tasks[i][j] + ']/div[1]/div/div/div[3]'
                button = driver.find_element_by_xpath(xpath)
                button.click()
            except:
                pass
                # TODO: runterscrollen (nur ein bisschen)

        xpath = '/html/body/div[1]/div/div[2]/div/div[1]/div/div[7]/div[2]/div[4]/div[2]/div/div/div/div/div/div[2]/button[3]'

    # TODO: erfolgreiche/gefailte Giveaways eintragen
