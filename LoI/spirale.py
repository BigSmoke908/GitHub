def erstelle_feld(b):
    result = []
    for i in range(b):
        row = []
        
        for j in range(b):
            row.append(0)
        result.append(row)
    return result


def finde_mitte(a):
    l = len(a)
    row = (l + 1) / 2
    if row % 1 != 0:
        row += 0.5

    column = (l + 1)/2
    if column % 1 != 0 :
        column -= 0.5

    return int(row - 1), int(column - 1)



def zeichne_feld(a):
    l = len(a) ** 2  + 1
    for i in a:
        print_string = ""
        for j in i:
            print_string += ((len(str(l)) + 1 - len(str(j))) * " ") + str(j)
        print(print_string)
    print("")
    return
    

def erzeuge_spirale(a:list):
    l = len(a)
    k = finde_mitte(a)  # koordinaten
    r = k[0]            # row               1
    c = k[1]            # column            0
    i = 1
    a[r][c] = i
    i += 1
    while(True):
        # nach rechts
        while (r,c) == k or a[r-1][c] > 0:
            c += 1
            a[r][c] = i
            i += 1
            if i == len(a) ** 2 + 1:
                return
        
        # nach oben
        while a[r][c-1] > 0:          
            r -= 1
            a[r][c] = i
            i += 1
            if i == len(a) ** 2 + 1:
                return
        
        # nach links
        while a[r+1][c] > 0:
            c -= 1
            a[r][c] = i
            i += 1
            if i == len(a) ** 2 + 1:
                return

        
        # nach unten
        while a[r][c+1] > 0:
            r += 1
            a[r][c] = i
            i += 1
            if i == len(a) ** 2 + 1:
                return



print('gib die Seitenlänge an: ')
x = input()
A = erstelle_feld(int(x)) # <- Größe des Quadrates als Parameter einfügen

zeichne_feld(A)

erzeuge_spirale(A)

zeichne_feld(A)
    
