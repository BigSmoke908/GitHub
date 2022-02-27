def wert_nach_wurf(punkte,wurf):
    try:
        wurf = int(wurf)  # wurde der wurf mit ring geworfen?
    except:
        if 'd' in wurf:
            wurf = wurf.replace('d', '')
            wurf = 2 * int(wurf)
        elif 't' in wurf:
            wurf = wurf.replace('t', '')
            wurf = 3 * int(wurf)

    if punkte - wurf > -1:
        return punkte - wurf
    else:
        return punkte


def vorschlag(punkte):
    guteIdeen = []
    for i in range(1, 21):
        for j in range(3):
            if j == 0:
                m = ''
            elif j == 1:
                m = 'd'
            else:
                m = 't'
            if wert_nach_wurf(punkte, m + str(i)) != punkte:
                if len(guteIdeen) != 0:
                    if wert_nach_wurf(punkte, m + str(i)) < wert_nach_wurf(punkte, guteIdeen[len(guteIdeen) - 1]):
                        guteIdeen.append(m + str(i))
                else:
                    guteIdeen.append(m + str(i))
    if len(guteIdeen) != 0:
        return guteIdeen[len(guteIdeen) - 1]
    else:
        return ''


while True:
    print('bitte gib an mit wie vielen Punkten du beginnst')
    Punkte = int(input())

    while Punkte != 0:
        print('Vorschlag für den nächsten Wurf:')
        print(vorschlag(Punkte), '\n')
        print('bitte gib deinen Wurf an')
        Wurf = input()
        Punkte = wert_nach_wurf(Punkte, Wurf)
        print('momentane Punkte: ' + str(Punkte))

    print('du hast gewonnen!!', '\n')