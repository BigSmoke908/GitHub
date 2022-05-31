import urllib.request
import urllib.error
import urllib.parse


# soll hinterher die Preis-Historien für ein beliebiges Produkt von PC-Partpicker zurückgegeben
# (Datenstruktur steht noch nicht fest)
# Funktion kann bis jetzt:
# die Daten von einem Produkt in eine gewünschte (auch noch unexistente) Datei schreiben
# die einzelnen Händler werden durch '||' voneinander getrennt, innerhalb von den Händlern wird die Struktur nicht verändert
# (diese soll dann später in einem anderen Script interpretiert werden
def get_chart_data(product_url, file):
    response = urllib.request.urlopen(product_url)
    webcontent = response.read().decode('UTF-8')

    gefiltert = ''

    for i in range(webcontent.index('chart_data'), webcontent.index('init_price_history_chart')):
        gefiltert += webcontent[i]

    gefiltert = gefiltert.replace('chart_data = ', '')
    gefiltert = gefiltert.replace('"', '')
    gefiltert = gefiltert.split('{')
    gefiltert.remove(gefiltert[0])

    for i in range(len(gefiltert)):
        gefiltert[i] = gefiltert[i].split(':')

    for shop in gefiltert:
        shop.remove(shop[0])
        shop[0] = shop[0].replace(',data', '')

    for shop in gefiltert:
        print(shop)

    f = open(file, 'w')
    for shop in gefiltert:
        buffer = ''
        for a in shop:
            while '\n' in a:
                a = a.replace('\n', '')
            while ' ' in a:
                a = a.replace(' ', '')
            buffer += a
        f.write(buffer + '||\n')
    f.close()


get_chart_data('https://de.pcpartpicker.com/product/FNprxr/gskill-aegis-16gb-2-x-8gb-ddr4-3000-memory-f43000c16d16gisb', 'test.txt')


# TODO: irgendwie intelligent die verschiedenen Typen von GPU (wie man die Links zum Suchen von denen erstellt) durch ein Skript machen
# TODO: eine Funktion um nacheinander die Links von den GPUs in Dateien zu laden erstellen
