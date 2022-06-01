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
    # Website herunterladen
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

    f = open(file, 'w')
    for shop in gefiltert:
        buffer = ''
        for a in shop:
            while '\n' in a:
                a = a.replace('\n', '')
            while ' ' in a:
                a = a.replace(' ', '')
            while ';' in a:
                a = a.replace(';', '')
            while '}' in a:
                a = a.replace('}', '')
            buffer += a
        f.write(buffer + '||\n')
    f.close()


# nimmt die ID für den Filter von einem Produkt entgegen und ließt erstellt dann die einzelnen Dateien, in denen
def get_all_products(filter_id):
    url = 'https://de.pcpartpicker.com/products/video-card/#c=' + str(filter_id)
    response = urllib.request.urlopen(url)
    site = response.read().decode('UTF-8')

    print(site)


get_all_products(494)

# TODO: irgendwie intelligent die verschiedenen Typen von GPU (wie man die Links zum Suchen von denen erstellt) durch ein Skript machen
# TODO: eine Funktion um nacheinander die Links von den GPUs in Dateien zu laden erstellen
# (Hinweis dafür in notizen.txt)
