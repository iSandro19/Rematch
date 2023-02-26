import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


SCREEN_WIDTH = 700
SCREEN_HEIGHT = 400

HALF_WIDTH = int(SCREEN_WIDTH / 2)
HALF_HEIGHT = int(SCREEN_HEIGHT / 2)


def main():
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    pygame.display.set_caption("RPG")
    global cameraX, cameraY



    pygame.init()

    #player = pygame.image.load("Textures(Final)\Whoo_For_Testing.bmp").convert()
    player = pygame.Surface((40,40))
    player.fill((255,0,0))

    playerrect = player.get_rect()
    player.set_colorkey(WHITE)


    #grasstile = pygame.image.load("Textures(Final)\Grass_Tile.bmp").convert()
    #watertile = pygame.image.load("Textures(Final)\Water_Tile.bmp").convert()
    #waterbeach = pygame.image.load("Textures(Final)\Water_Beach.bmp").convert()
    grasstile = pygame.Surface((40,40))
    watertile = pygame.Surface((40,40))
    waterbeach = pygame.Surface((40,40))
    grasstile.fill((0,200,0))
    watertile.fill((0,0,200))
    waterbeach.fill((200,200,250))

    grassrect = grasstile.get_rect()
    waterrect = watertile.get_rect()
    waterb = waterbeach.get_rect()

    TILE_WIDTH = 32
    TILE_HEIGHT = 32

    tilemap = [
                [grasstile, grasstile, grasstile, grasstile, waterbeach, watertile, watertile, watertile, watertile],
                [grasstile, grasstile, grasstile, grasstile, waterbeach, watertile, watertile, watertile, watertile],
                [grasstile, grasstile, grasstile, grasstile, waterbeach, watertile, watertile, watertile, watertile],
                [grasstile, grasstile, grasstile, grasstile, waterbeach, watertile, watertile, watertile, watertile],
                [grasstile, grasstile, grasstile, grasstile, waterbeach, watertile, watertile, watertile, watertile],
                [grasstile, grasstile, grasstile, grasstile, waterbeach, watertile, watertile, watertile, watertile],
                [grasstile, grasstile, grasstile, grasstile, waterbeach, watertile, watertile, watertile, watertile],
                [grasstile, grasstile, grasstile, grasstile, waterbeach, watertile, watertile, watertile, watertile],
                [grasstile, grasstile, grasstile, grasstile, waterbeach, watertile, watertile, watertile, watertile],
                [grasstile, grasstile, grasstile, grasstile, waterbeach, watertile, watertile, watertile, watertile],
                [grasstile, grasstile, grasstile, grasstile, waterbeach, watertile, watertile, watertile, watertile],
                [grasstile, grasstile, grasstile, grasstile, waterbeach, watertile, watertile, watertile, watertile],
                [grasstile, grasstile, grasstile, grasstile, waterbeach, watertile, watertile, watertile, watertile]
            ]

    total_level_width = len(tilemap[0]) * 32
    total_level_height = len(tilemap)*32

    camera = Camera(simple_camera ,total_level_width, total_level_height)


    map_surface = pygame.Surface(( len(tilemap[0])*TILE_WIDTH, len(tilemap)*TILE_HEIGHT))

    for y,row in enumerate(tilemap):
        for x,tile_surface in enumerate(row):
            map_surface.blit(tile_surface,(x*TILE_WIDTH,y*TILE_HEIGHT))

    map_surface = pygame.transform.scale(map_surface, (1200, 800))
    player = pygame.transform.scale(player, (50, 100))


    done = False

    clock = pygame.time.Clock()

    move_speed = 5
    x, y = 100, 100

    entities = pygame.sprite.Group()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            y -= move_speed
        elif keys[pygame.K_DOWN]:
            y += move_speed
        elif keys[pygame.K_LEFT]:
            x -= move_speed
        elif keys[pygame.K_RIGHT]:
            x += move_speed

        screen.fill(BLACK)

        screen.blit(map_surface, camera.apply(grassrect))
        screen.blit(player, camera.apply(pygame.Rect(x,y,50,100)))

        camera.update(player.get_rect().move((x,y)))

        clock.tick(20)

        pygame.display.flip()

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, rect):
        return rect.move(self.state.topleft)

    def update(self, target_rect):
        self.state = self.camera_func(self.state, target_rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera

    return pygame.Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-SCREEN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-SCREEN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return pygame.Rect(l, t, w, h)

if __name__ == "__main__":
    main()



pygame.quit()