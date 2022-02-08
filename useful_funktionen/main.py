# DIESE DATEI ENTHÄLT VERSCHIEDENE POTENTIELL NÜTZLICHE FUNKTIONEN


# FUNKTION 1
# diese Funktion kann der den Wert von Aktien von Yahoo Finance für einen beliebigen Zeitraum aus dem Netz ziehen
# als Eingabe wird das Kürzel der Aktie (stock), dann im datetime-Format der Beginn von dem Zeitraum (start) und in dem
# selben Format (end)
# wenn es nicht möglich war irgendwelche Daten aus dem Internet zu ziehen, dann gibt sie eine leere List zurück
# in der Datei F1.odt wird das auslesen der Der zurückgegebenen List noch genauer erklärt

# IMPORT ANFANG FÜR F1:
import datetime as dt
import pandas_datareader.data as pdr
# IMPORT ENDE FÜR F1:
# F1 ANFANG


def get_value(stock, start, end):
    try:
        df = pdr.get_data_yahoo(stock, start, end)

    except:
        print('es konnten keine Daten erhoben werden bei der Aktie mit dem Kürzel "' + stock + '"')
        return []

    return df.to_numpy()

# F1 ENDE
