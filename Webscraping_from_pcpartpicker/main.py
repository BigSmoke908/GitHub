import urllib.request
import urllib.error
import urllib.parse


# soll hinterher die Preis-Historien für ein beliebiges Produkt von PC-Partpicker zurückgegeben (Struktur steht noch nicht fest)
def get_chart_data(product_url):
    response = urllib.request.urlopen(product_url)
    webcontent = response.read().decode('UTF-8')

    gefiltert = ''

    for i in range(webcontent.index('chart_data'), webcontent.index('init_price_history_chart')):
        gefiltert += webcontent[i]

    # Label zeigt an, dass jeweils ein neuer Händler beginnt, das erste Element ist noch keine Händler sind andere Sachen von HTML
    gefiltert = gefiltert.split('label').pop(0)

    gefiltert

    print(len(gefiltert))

    for stuff in gefiltert:
        print(stuff)


get_chart_data('https://de.pcpartpicker.com/product/FNprxr/gskill-aegis-16gb-2-x-8gb-ddr4-3000-memory-f43000c16d16gisb')
