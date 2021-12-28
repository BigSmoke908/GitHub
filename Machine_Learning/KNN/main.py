from math import sqrt as wurzel


def knn_gewichtet(x):
    global a, b, c, z, ta, tb, tc, tz, result, in_Daten
    a = []
    b = []
    c = []
    z = []
    ta = []
    tb = []
    tc = []
    tz = []
    in_Daten = False
    result = 0

    # alle Daten werden sortiert
    with open('bekannt.txt') as f:
        alles = f.read()
        f.close()
        alles = alles.split()
    for i in range(len(alles)):
        alles[i] = int(alles[i])

    # jetzt sind alle Daten unsortiert in alles
    for i in range(len(alles)):
        buffer = i % 4
        if buffer == 0:
            a.append(alles[i])
        elif buffer == 1:
            b.append(alles[i])
        elif buffer == 2:
            c.append(alles[i])
        else:
            z.append(alles[i])
    while len(alles) != 0:
        alles.remove(alles[0])
    # jetzt sind alle Daten in a, b, c, z aufgeteilt und damit verarbeitbar

    # die Testdaten werden sortiert
    with open('unbekannt.txt') as f:
        alles = f.read()
        f.close()
        alles = alles.split()
    for i in range(len(alles)):
        alles[i] = int(alles[i])
    # jetzt sind alle Daten unsortiert in alles
    for i in range(len(alles)):
        buffer = i % 4
        if buffer == 0:
            ta.append(alles[i])
        elif buffer == 1:
            tb.append(alles[i])
        elif buffer == 2:
            tc.append(alles[i])
        else:
            tz.append(alles[i])
    while len(alles) != 0:
        alles.remove(alles[0])
    # jetzt sind die Punkte die geprüft werden sollen fertig sortiert in ta, tb, tc, tz

    distanz = {}
    # speichert den Abstand zwischen einem gegebenen Punkt (der der geprüft)
    # und allen Punkten aus den Trainingsdaten (Postion = Nummer von Punkt)
    # die Keys werden nach den Nummern der Punkte in den Trainingsdaten einfach durchnummeriert
    # (erst steht der Abstand, dann ob Teil der Kategorie oder nicht

    for i in range(len(a)):
        buffer = ((a[i] - ta[x]) ** 2) + ((b[i] - tb[x]) ** 2) + ((c[i] - tc[x]) ** 2)
        if buffer != 0:
            buffer = wurzel(buffer)
        distanz[i] = [buffer, z[i]]

    for i in range(len(distanz)):
        if distanz[i][1] == 0 and distanz[i][0] != 0:
            result -= 1/distanz[i][0]
        elif distanz[i][0] != 0:
            result += 1/distanz[i][0]
        else:
            if distanz[i][1] == 0:
                result = -1
            else:
                result = 1
            in_Daten = True
            break


for i in range(7):
    knn_gewichtet(i)
    print('Punkt Nummer: ' + str(i))
    print('Eigenschaften:', ta[i], tb[i], tc[i])

    if not in_Daten:
        if result == 0:
            print('Kein Eindeutiges Ergebnis konnte ermittelt werden')
        elif result > 0:
            print('Der Gegebene Punkt ist Teil der Klasse. Berechneter Wert:')
            print(result)
        else:
            print('Der gegebene Punkt ist nicht Teil der Klasse. Berechneter Wert:')
            print(abs(result))
    else:
        print('Der Punkt ist so in den Trainingsdaten vorhanden.')
        if result < 0:
            print('In den Daten ist dieser Punkt nicht Teil der Klasse')
        else:
            print('In den Daten ist dieser Punkt Teil der Klasse')
    print()