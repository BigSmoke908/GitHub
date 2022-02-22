import random
from PIL import Image, ImageFilter

LayerBereich = [4, 13]  # gibt den Bereich an, in dem sich der Faktor von den Layern während dem erstellen befindet, ist minimal 1 und maximal die 2er Potenz, mit der man auf die Größe der Map kommt (je größer, desto glatteres Terrain)
mapSize = 4096  # Größe der Map in Höhe mal Breite (muss eine 2er Potenz sein)
Map = []  # soll als List (alle Zeilen einfach hintereinander die Karte sein


# generiert eine Hightmap, indem verschiedene Layer übereinander gelegt werden, min/max sind mindest/maximal Höhe
def generate_heightmap(layerbereich, size):
    height_map = [[0 for i in range(size)] for j in range(size)]
    layermaps = {}  # speichert die Karte von jedem einzelnen

    # es sollen nacheinander verschiedene Bereiche erstelle werden, welche dann eine Höhe erhalten, welche dann alle
    # zusammen diesen Layer bilden sollen
    h = layerbereich[0]
    while h <= layerbereich[1]:
        bereiche = []  # immer die Begrenzungen von einem Bereich

        #  die Maße von den momentanen Bereichen

        length = size
        for i in range(h):
            length /= 2

        # generiert für jedes einzelne Layer die Bereiche, diese erhalten noch keine Höhe (wird erst bei dem nächsten Schritt festgelegt
        for i in range(1, size + 1):  # Loop für alle Werte (da immer ein Quadrat entsteht, reicht eine Seitenkante
            if i % length == 0 and i not in bereiche:
                bereiche.append(i)

        layermaps.update({h: []})
        layermaps[h] = bereiche     # enthält dann von allen Layern den Bereich (wo die Höhe jeweils wirkt) und
                                    # den Betrag (von der jeweiligen Höhe)
        h += 1

    print('Einzelne Schichten wurden erstellt. Die Schichten werden jetzt zusammengefügt')

    for i in layermaps:  # alle einzelnen Karten durchgehen (i enstpricht h von vorher)
        tile_y = 0  # Y Platz (in der List) von dem Tile, welches gerade genutzt wird
        tile_x = 0  # X Platz (in der List) von dem Tile, welches gerade genutzt wird
        y = 0  # Y Koordinate auf der heightmap
        x = 0  # X Koordinate auf der heightmap

        momentane_karte = layermaps[i]  # (ist dann einfacher bei jedes Mal aufrufen)

        momentane_höhen = [[random.randrange(0, 255) for j in range(len(momentane_karte))] for k in range(len(momentane_karte))]
        # eine Karte in der die Höhen der einzelnen Tiles drinstehen

        while True:  # fügt alle einzelnen Karten zusammen
            if y == len(height_map):  # am Boden angekommen?
                break
            elif x == len(height_map):  # an der rechten Wand angekommen
                x = 0
                tile_x = 0
                y += 1
            elif y == momentane_karte[tile_y]:  # muss das Tile geändert werden?
                tile_y += 1
            elif x == momentane_karte[tile_x]:  # muss das Tile geändert werden?
                tile_x += 1
            else:  # die Höhe kann bei dem jeweiligen eingetragen werden
                height_map[y][x] += (momentane_höhen[tile_y][tile_x] * (1))
                x += 1

    print('Die Schichten wurden zusammengefügt. Jetzt werden die Daten "bereinigt"')

    # TODO: Datenpunkte so erhöhen/erniedrigen, dass hohe dicht bei anderen hohen liegen

    # jetzt müssen die Datenpunkte noch so erhöht/erniedrigt werden, dass sie zwischen 0 und 255 liegen
    buffer = 0
    for i in range(len(height_map)):
        for j in range(len(height_map)):
            if height_map[i][j] > buffer:
                buffer = height_map[i][j]

    scale = 255 / buffer
    for i in range(len(height_map)):
        for j in range(len(height_map)):
            height_map[i][j] *= scale
            height_map[i][j] = int(height_map[i][j])

    print('Die Heightmap wurde fertig erstellt, jetzt wird sie in eine Bilddatei umgewandelt')
    return height_map


def make_png(map, file, size):
    img = Image.new('RGB', (size, size))
    img.putdata(map)
    img.save(file)

    img = Image.open(file)
    img = img.filter(ImageFilter.BLUR)
    img.save(file)

    print('alles ist abgeschlossen')


Map = generate_heightmap(LayerBereich, mapSize)

Fertig = []

for i in range(len(Map)):
    for j in range(len(Map)):
        Fertig.append((Map[i][j], Map[i][j], Map[i][j]))

make_png(Fertig, 'img.png', mapSize)
