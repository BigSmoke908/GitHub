import time
import sys
import os
import datetime

no_time = True
while no_time:
    try:
        dauer = float(input('Nach wie vielen Minuten soll der PC ausgehen?\n'))
        no_time = False
    except:
        print('Das ist keine richtige Zeit. Versuche es erneut!'
              '(Kommas sind Punkte, nur die Zahl ohne Einheit eingeben)')

begin = time.time()
while True:
    if begin + (dauer * 60) < time.time():
        f = open('log.txt', 'a')
        f.write('PC wurde abgeschaltet, Zeit: ' + str(datetime.datetime.now()) + '\n')
        print('PC wurde abgeschaltet.')
        time.sleep(0.1)
        os.system('shutdown /s /t 1')
        sys.exit()
