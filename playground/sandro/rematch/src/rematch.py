import sys, os, pygame
from pygame import *

sys.path.append("src/levels")
import jardin, sala, biblioteca, torre, catacumbas, pasillo1, pasillo2

LEVEL_NAMES = ["jardin", "sala", "biblioteca", "torre", "catacumbas", "pasillo1", "pasillo2"]
PLAYER_TILE = [[6, 6], [4, 18], [4, 20], [18, 42], [8, 4], [2, 6], [2, 6]]
SCREEN_SIZE = pygame.Rect((0, 0, 1280, 720))
GRAVITY = pygame.Vector2((0, 0.5))
TILE_SIZE = 64

bishop_image = pygame.image.load("assets/sprites/bishop.png")
background_image = pygame.image.load("assets/sprites/background.png")
board_image = pygame.image.load("assets/sprites/board.png")
button_door_image = pygame.image.load("assets/sprites/button_door.png")
button_image = pygame.image.load("assets/sprites/button.png")
knight_image = pygame.image.load("assets/sprites/knight.png")
destroy_image = pygame.image.load("assets/sprites/destroy.png")
door_image = pygame.image.load("assets/sprites/door.png")
easter_image = pygame.image.load("assets/sprites/easter.png")
enemy_image = pygame.image.load("assets/sprites/enemy.png")
floor_image = pygame.image.load("assets/sprites/floor.png")
pawn_image = pygame.image.load("assets/sprites/pawn.png")
player_image = pygame.image.load("assets/sprites/player.png")
shelving_image = pygame.image.load("assets/sprites/shelving.png")
table_image = pygame.image.load("assets/sprites/table.png")
rook_image = pygame.image.load("assets/sprites/rook.png")
wall_image = pygame.image.load("assets/sprites/wall.png")
oneway_door_image = pygame.image.load("assets/sprites/oneway_door.png")

###############################################################################

# Main ########################################################################
def main(lvl):
    screen = pygame.display.set_mode(SCREEN_SIZE.size)
    timer = pygame.time.Clock()
    
    platforms = pygame.sprite.Group()
    x, y = player_pos(lvl)
    player = Player(platforms, (x*TILE_SIZE, y*TILE_SIZE))

    entities = update_level(LEVEL_NAMES[lvl], player, platforms)
    
    while True:
        for e in pygame.event.get():
            if e.type == QUIT: 
                return
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                return

        entities.update()

        screen.fill((0, 0, 0))
        entities.draw(screen)
        pygame.display.update()
        timer.tick(60)

###############################################################################

# Functions ###################################################################
def levels(name):
    if name == "jardin":
        return jardin.world_data
    elif name == "sala":
        return sala.world_data
    elif name == "biblioteca":
        return biblioteca.world_data
    elif name == "torre":
        return torre.world_data
    elif name == "catacumbas":
        return catacumbas.world_data
    elif name == "pasillo1":
        return pasillo1.world_data
    elif name == "pasillo2":
        return pasillo2.world_data
    else:
        print("Error: Level not found") 
        exit(0)

def draw_level(level, platforms, entities):
    x = y = 0
    """
    ESTRUCTURAS
        W - pared
        F - suelo
        T - mesa
        S - estantería

    PUERTAS
        DS - puerta (ir a sala)
        DJ - puerta (ir a jardín)
        DP1 - puerta (ir a pasillo1)
        DP2 - puerta (ir a pasillo2)
        DB - puerta (ir a biblioteca)
        DT - puerta (ir a torre)
        DC - puerta (ir a catacumbas)
    
    Q - puerta botón
    U - puerta unidireccional

    ENTITIES
        E - enemigo
        P - jugador
        X - destructible
        A - Easter Egg

    BOTONES
        B - boton

    ITEMS
        0 - tablero
        1 - peón
        2 - alfil
        3 - torre
        4 - caballo
    """
    for row in level:
        for col in row:
            if "W" in col:
                Wall((x, y), platforms, entities)
            if "F" in col:
                Floor((x, y), platforms, entities)
            if "T" in col:
                Table((x, y), platforms, entities)
            if "S" in col:
                Shelving((x, y), platforms, entities)
            if "D" in col:
                if "DJ" in col:
                    DoorGarden((x, y), platforms, entities)
                if "DS" in col:
                    DoorHall((x, y), platforms, entities)
                if "DP1" in col:
                    DoorCorridor1((x, y), platforms, entities)
                if "DP2" in col:
                    DoorCorridor2((x, y), platforms, entities)
                if "DB" in col:
                    DoorLibrary((x, y), platforms, entities)
                if "DT" in col:
                    DoorTower((x, y), platforms, entities)
                if "DC" in col:
                    DoorCatacombs((x, y), platforms, entities)
            if "Q" in col:
                ButtonDoor((x, y), platforms, entities)
            if "U" in col:
                OneWayDoor((x, y), platforms, entities)
            if "E" in col:
                Enemy((x, y), platforms, entities)
            if "X" in col:
                Destroy((x, y), platforms, entities)
            if "A" in col:
                Easter((x, y), platforms, entities)
            if "B" in col:
                Button((x, y), platforms, entities)
            if "0" in col:
                Board((x, y), platforms, entities)
            if "1" in col:
                Pawn((x, y), platforms, entities)
            if "2" in col:
                Bishop((x, y), platforms, entities)
            if "3" in col:
                Rook((x, y), platforms, entities)
            if "4" in col:
                Knight((x, y), platforms, entities)
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0

def update_level(name, player, platforms):
    level = levels(name)
    level_width  = len(level[0])*TILE_SIZE
    level_height = len(level)*TILE_SIZE

    entities = CameraAwareLayeredUpdates(player, pygame.Rect(0, 0, level_width, level_height))

    draw_level(level, platforms, entities)

    return entities

def player_pos(lvl):
    x = PLAYER_TILE[lvl][0]
    y = PLAYER_TILE[lvl][1]

    return x, y

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

###############################################################################

# Main classes ################################################################
class CameraAwareLayeredUpdates(pygame.sprite.LayeredUpdates):
    def __init__(self, target, world_size):
        super().__init__()
        self.target = target
        self.cam = pygame.Vector2(0, 0)
        self.world_size = world_size
        if self.target:
            self.add(target)

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + SCREEN_SIZE.width/2
            y = -self.target.rect.center[1] + SCREEN_SIZE.height/2
            self.cam += (pygame.Vector2((x, y)) - self.cam) * 0.05
            self.cam.x = max(-(self.world_size.width-SCREEN_SIZE.width), min(0, self.cam.x))
            self.cam.y = max(-(self.world_size.height-SCREEN_SIZE.height), min(0, self.cam.y))

    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect
        for spr in self.sprites():
            rec = spritedict[spr]
            newrect = surface_blit(spr.image, spr.rect.move(self.cam))
            if rec is init_rect:
                dirty_append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty_append(newrect.union(rec))
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[spr] = newrect
        return dirty
        
class Entity(pygame.sprite.Sprite):
    def __init__(self, image, pos, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

# Estructures  ################################################################
class Wall(Entity):
    def __init__(self, pos, *groups):
        super().__init__(wall_image, pos, *groups)

class Floor(Entity):
    def __init__(self, pos, *groups):
        super().__init__(floor_image, pos, *groups)

class Table(Entity):
    def __init__(self, pos, *groups):
        super().__init__(table_image, pos, *groups)

class Shelving(Entity):
    def __init__(self, pos, *groups):
        super().__init__(shelving_image, pos, *groups)

# Doors #######################################################################
class DoorGarden(Entity):
    def __init__(self, pos, *groups):
        super().__init__(door_image, pos, *groups)

class DoorHall(Entity):
    def __init__(self, pos, *groups):
        super().__init__(door_image, pos, *groups)

class DoorLibrary(Entity):
    def __init__(self, pos, *groups):
        super().__init__(door_image, pos, *groups)

class DoorTower(Entity):
    def __init__(self, pos, *groups):
        super().__init__(door_image, pos, *groups)

class DoorCatacombs(Entity):
    def __init__(self, pos, *groups):
        super().__init__(door_image, pos, *groups)

class DoorCorridor1(Entity):
    def __init__(self, pos, *groups):
        super().__init__(door_image, pos, *groups)

class DoorCorridor2(Entity):
    def __init__(self, pos, *groups):
        super().__init__(door_image, pos, *groups)

class ButtonDoor(Entity):
    def __init__(self, pos, *groups):
        super().__init__(button_door_image, pos, *groups)

class OneWayDoor(Entity):
    def __init__(self, pos, *groups):
        super().__init__(oneway_door_image, pos, *groups)

# Entities ####################################################################
class Enemy(Entity):
    def __init__(self, pos, *groups):
        super().__init__(enemy_image, pos, *groups)

class Player(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(player_image, pos)
        self.vel = pygame.Vector2((0, 0))
        self.onGround = False
        self.platforms = platforms
        self.speed = 8
        self.jump_strength = 14
        
    def update(self):
        pressed = pygame.key.get_pressed()
        up = pressed[K_UP]
        left = pressed[K_LEFT]
        right = pressed[K_RIGHT]
        running = pressed[K_SPACE]
        
        if up:
            if self.onGround: self.vel.y = -self.jump_strength
        if left:
            self.vel.x = -self.speed
        if right:
            self.vel.x = self.speed
        if running:
            self.vel.x *= 1.5
        if not self.onGround:
            self.vel += GRAVITY
            if self.vel.y > 100: self.vel.y = 100
        if not(left or right):
            self.vel.x = 0
        
        self.rect.left += self.vel.x
        self.collide(self.vel.x, 0, self.platforms)
        self.rect.top += self.vel.y
        self.onGround = False;
        self.collide(0, self.vel.y, self.platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                # Doors
                if isinstance(p, DoorGarden):
                    print("Go to garden")
                    main(0)
                if isinstance(p, DoorHall):
                    print("Go to hall")
                    main(1)
                if isinstance(p, DoorLibrary):
                    print("Go to library")
                    main(2)
                if isinstance(p, DoorTower):
                    print("Go to tower")
                    main(3)
                if isinstance(p, DoorCatacombs):
                    print("Go to catacombs")
                    main(4)
                if isinstance(p, DoorCorridor1):
                    print("Go to corridor1")
                    main(5)
                if isinstance(p, DoorCorridor2):
                    print("Go to corridor2")
                    main(6)             
                
                # Physics
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.vel.y = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom

class Destroy(Entity):
    def __init__(self, pos, *groups):
        super().__init__(destroy_image, pos, *groups)

class Easter(Entity):
    def __init__(self, pos, *groups):
        super().__init__(easter_image, pos, *groups)

class Button(Entity):
    def __init__(self, pos, *groups):
        super().__init__(button_image, pos, *groups)

# Items
class Board(Entity):
    def __init__(self, pos, *groups):
        super().__init__(board_image, pos, *groups)

class Pawn(Entity):
    def __init__(self, pos, *groups):
        super().__init__(pawn_image, pos, *groups)

class Bishop(Entity):
    def __init__(self, pos, *groups):
        super().__init__(bishop_image, pos, *groups)

class Rook(Entity):
    def __init__(self, pos, *groups):
        super().__init__(rook_image, pos, *groups)

class Knight(Entity):
    def __init__(self, pos, *groups):
        super().__init__(knight_image, pos, *groups)

###############################################################################

# Start #######################################################################
if __name__ == "__main__":
    pygame.init()
    main(0)