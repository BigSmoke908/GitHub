import pygame
pygame.init()
pygame.font.init()

playerCoords = [960, 540]
cities = {
    0:[0,0],
    1:[10,10]
}
# erste Zahl muss der Reihenfolge folgen, die Zahlen danach sind die Index der Städte die verbunden werden
routes = {}
routesCoords = {}
Font = pygame.font.SysFont('impact', 32)
numCities = 0
Citycounter = Font.render('Anzahl der Städe: ' + str(numCities), True, (100, 100, 100))
running = True

screen = pygame.display.set_mode((1920,1080))

city = pygame.image.load('City.png').convert_alpha()
salesman = pygame.image.load('Salesman.png').convert_alpha()
Pixel = pygame.image.load('Pixel.png').convert_alpha()


def get_route():
    #TODO: optimale Route muss berechnet werden
    return


def conv_coords(coordinate):
    if coordinate < 540:
        return 540 + (540 - coordinate)
    if coordinate > 540:
        return 540- (540 + coordinate)
    return 540


def render_weg(a, b):
    #TODO: Funktion muss gefixt werden
    start, end, = a, b
    if a[0] > b[0]:
        end, start = a, b

    m = int((end[0]-start[0]) / (end[1]+start[1]))
    n = int(start[1] - (m*start[0]))
    for x in range(start[0], end[0]):
        screen.blit(Pixel, (x, m*x+n))


def render_all():
    screen.fill((47, 45, 45))
    screen.blit(Citycounter,(1600, 20))

    for i in range(len(cities)):
        screen.blit(city,(cities[i][0], cities[i][1]))
    screen.blit(salesman,(playerCoords[0], playerCoords[1]))

    for i in range(len(routes)):
        start = cities[routes[i][0]]
        end = cities[routes[i][1]]
        render_weg(start, end)
    pygame.display.update()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                get_route()
            if event.key == pygame.K_r:
                cities = {}
                numCities = 0
                routes = {}
            if event.key == pygame.K_x:
                routes = {0: [0, 1], 1:[0,2]}
                Citycounter = Font.render('Anzahl der Städe: ' + str(numCities), True, (100, 100, 100))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                cities.update({len(cities):[x, y]})
                numCities += 1
                Citycounter = Font.render('Anzahl der Städe: ' + str(numCities), True, (100, 100, 100))
            elif event.button == 3:
                playerCoords[0], playerCoords[1] = pygame.mouse.get_pos()

    render_all()