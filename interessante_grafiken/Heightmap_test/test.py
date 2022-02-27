# nimmt ein Heightmap und glättet sie etwas (Punkte die nebeneinander liegen, bekommen eine ähnliche Höhe)
# macht mitunter seltsame Dinge, könnte vielleicht noch verbessert werden (Durchschnitt von mehr als nur 9 Feldern bespielsweise)
def smooth_map(karte, h):

    # zusätzliche Seiten anhängen
    karte.insert(0, karte[0].copy())  # oben
    karte.append(karte[-1].copy())  # unten

    for c in range(len(karte)):
        karte[c].insert(0, 1)
        karte[c].append(1)

    buffer = karte.copy()

    for c in range(100//h):
        karte = buffer.copy()
        for a in range(1, len(buffer) - 1):
            for b in range(1, len(buffer) - 1):
                buffer[a][b] = (karte[a][b] + karte[a - 1][b] + karte[a - 1][b - 1] + karte[a][b - 1] + karte[a + 1][b - 1] + karte[a + 1][b] + karte[a + 1][b + 1] + karte[a][b + 1] + karte[a - 1][b + 1]) // 9

    buffer.remove(buffer[0])
    buffer = buffer[:-1]

    for c in range(len(buffer)):
        buffer[c].remove(buffer[c][0])
        buffer[c] = buffer[c][:-1]

    return buffer


seite = 4
karte = [[0 for i in range(seite)] for j in range(seite)]

smooth_map(karte, 100)
