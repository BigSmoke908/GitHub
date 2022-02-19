import random


# erstellt Daten in bestimmter Anzahl mit einem bestimmten Label
# die ersten 3 Parameter sind lists
# label -> welches Label für die jeweiligen Daten verwendet werden soll
# Anzahl -> wie viele Datenpunkte von dem jeweiligen Label existieren sollen
# bereich -> der Bereich in dem sich die jeweiligen Datenpunkte bei der gegebenen Anzahl an Dimensionen befinden soll
# (jedes Label erhält eigene List, in der jeweils eine List für jede Dimension mit dem Bereich drin ist)
# die nächsten beiden Parameter sind keine Listen
# datei (string) -> gibt an in welche Datei die Datenpunkte geschrieben werden sollen
# Anzahl Dimensionen (integer) -> gibt an in wie vielen Dimensionen die Datenpunkte sich befinden sollen
# (muss mit der Länge von einem Element in der List "Bereich" übereinstimmen)
# wenn in der Datei bereits Datenpunkte vorhanden sind, werden diese Einfach ignoriert
# ersten werden mit jeweils einem Leerzeichen dazwischen alle Werte + das Label in die Datei geschrieben
# nach jedem Datenpunkt wird ein " || " eingefügt
# Funktionsaufruf Beispiel:
# create_data([0], [10], [[[10, 20], [30, 40]]], 'bekannt.txt')
# erstellt 10 Datenpunkte, mit dem Label 0, in 2 Dimensionen (erste in Bereich 10-20, die zweite mit Bereich 30-40)
# die Datenpunkte werden danach alle in bekannt.txt geschrieben
def create_data(label, anzahl, bereich, datei):
    f = open(datei, 'a')

    f.write('\n')

    for i in range(len(label)):  # Counter für die einzelnen Label
        for j in range(anzahl[i]):  # Counter für die einzelnen Punkte
            punkt = [(str(random.randrange(bereich[i][k][0], bereich[i][k][1])) + ' ') for k in range(len(bereich[i]))]
            punkt.append(str(label[i]) + ' ')
            punkt.append('|| ')

            punkt_neu = ''  # in einen String konvertieren, der dann in die Datei geschrieben werden kann
            for k in range(len(punkt)):
                punkt_neu += punkt[k]

            f.write(punkt_neu + '\n')

    f.close()
