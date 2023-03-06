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
    player = Player(screen, platforms, (x*TILE_SIZE, y*TILE_SIZE))

    entities = update_level(LEVEL_NAMES[lvl], player, platforms)
    
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                exit(0)
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                exit(0)

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
            if col.startswith("W"):
                Wall((x, y), platforms, entities)
            if col.startswith("F"):
                Floor((x, y), platforms, entities)
            if col.startswith("T"):
                Table((x, y), platforms, entities)
            if col.startswith("S"):
                Shelving((x, y), platforms, entities)
            if "D" in col:
                if col == "DJ":
                    DoorGarden((x, y), platforms, entities)
                if col == "DS":
                    DoorHall((x, y), platforms, entities)
                if col == "DP1":
                    DoorCorridor1((x, y), platforms, entities)
                if col == "DP2":
                    DoorCorridor2((x, y), platforms, entities)
                if col == "DB":
                    DoorLibrary((x, y), platforms, entities)
                if col == "DT":
                    DoorTower((x, y), platforms, entities)
                if col == "DC":
                    DoorCatacombs((x, y), platforms, entities)
            if col.startswith("Q"):
                ButtonDoor((x, y), platforms, entities)
            if col.startswith("U"):
                OneWayDoor((x, y), platforms, entities)
            if col.startswith("E"):
                Enemy((x, y), platforms, entities)
            if col.startswith("X"):
                Destroy((x, y), platforms, entities)
            if col.startswith("A"):
                Easter((x, y), platforms, entities)
            if col.startswith("B"):
                Button((x, y), platforms, entities)
            if col.startswith("0"):
                Board((x, y), platforms, entities)
            if col.startswith("1"):
                Pawn((x, y), platforms, entities)
            if col.startswith("2"):
                Bishop((x, y), platforms, entities)
            if col.startswith("3"):
                Rook((x, y), platforms, entities)
            if col.startswith("4"):
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
    def __init__(self, screen, platforms, pos, *groups):
        super().__init__(player_image, pos)
        
        # Atributos
        self.vel = pygame.Vector2((0, 0))
        self.platforms = platforms
        self.screen = screen

        self.onGround = False
        self.jump_strength = 14
        self.speed = 8

        self.max_jumps = 10
        self.jumps_left = self.max_jumps

        self.dash = False
        self.dash_timer = 0

        self.basic_attack = False
        self.long_attack = False
        self.strong_attack = False
        self.circle_attack = False

        # Habilidades
        self.jump_ability = False
        self.double_jump_ability = False
        self.dash_ability = False
        self.bounce_ability = False

        self.basic_attack_ability = False
        self.long_attack_ability = False
        self.strong_attack_ability = False
        self.circle_attack_ability = False
        
    def update(self):
        pressed = pygame.key.get_pressed()
        up = pressed[K_UP]
        space = pressed[K_SPACE]
        w = pressed[K_w]

        left = pressed[K_LEFT]
        a = pressed[K_a]

        right = pressed[K_RIGHT]
        d = pressed[K_d]

        shift = pressed[K_LSHIFT]

        one = pressed[K_1]
        two = pressed[K_2]
        three = pressed[K_3]
        four = pressed[K_4]
        
        if (up or space or w):
            if self.jumps_left > 0:
                if not self.onGround:
                    self.vel.y = 0
                self.vel.y -= self.jump_strength
                self.jumps_left -= 1
                print("JUMP")
        if left or a:
            self.vel.x = -self.speed
        if right or d:
            self.vel.x = self.speed
        if shift and not self.dash:
            self.vel.x *= 10
            self.dash = True
        if not self.onGround:
            self.vel += GRAVITY
            if self.vel.y > 100: self.vel.y = 100
        if not(left or right or a or d):
            self.vel.x = 0

        if self.dash:
            self.dash_timer += 1
            if self.dash_timer > 100:
                self.vel.x /= 5
                self.dash = False
                self.dash_timer = 0
        
        if one:
            # Dibujar el ataque básico (ataque corto hacia delante)
            pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.x + self.rect.width, self.rect.y, 100, 20))
            pygame.display.update()
            print("BASIC_ATTACK")
        elif two:
            # Dibujar el ataque largo (ataque mas largo hacia delante)
            pygame.draw.rect(self.screen, (0, 255, 0), (self.rect.x + self.rect.width, self.rect.y, 200, 20))
            pygame.display.update()
            print("LONG_ATTACK")
        elif three:
            # Dibujar el ataque fuerte (ataque corto hacia delante)
            pygame.draw.rect(self.screen, (0, 0, 255), (self.rect.x + self.rect.width, self.rect.y, 100, 20))
            pygame.display.update()
            print("STRONG_ATTACK")
        elif four:
            # Dibujar el ataque en círculo (ataque corto hacia delante y hacia atrás)
            pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.x + self.rect.width, self.rect.y, 100, 20))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.x - self.rect.width, self.rect.y, 100, 20))
            pygame.display.update()
            print("CIRCLE_ATTACK")
    
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

                if isinstance(p, Pawn):
                    print("Pawn")
                    self.pawn_atk = True
                    self.jump = True
                
                # Physics
                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.vel.x = 0
                    if not self.onGround:
                        self.jumps_left = self.max_jumps
                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.vel.x = 0
                    if not self.onGround:
                        self.jumps_left = self.max_jumps
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.vel.y = 0
                    self.jumps_left = self.max_jumps
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