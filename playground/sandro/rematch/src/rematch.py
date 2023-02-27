import sys
import pygame
from pygame import *

sys.path.append("src/levels")
import jardin, sala, biblioteca, torre, catacumbas, pasillo1, pasillo2

SCREEN_SIZE = pygame.Rect((0, 0, 800, 640))
TILE_SIZE = 64 
GRAVITY = pygame.Vector2((0, 0.3))

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
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y), platforms, entities)
            if col == "G":
                Ground((x, y), platforms, entities)
            if col == "D":
                Door((x, y), platforms, entities)
            if col == "E":
                Enemy((x, y), platforms, entities)
            if col == "X":
                Xtroy((x, y), platforms, entities)
            if col == "A":
                Alt((x, y), platforms, entities)
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
            
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE.size)
    timer = pygame.time.Clock()
    
    platforms = pygame.sprite.Group()
    player = Player(platforms, (TILE_SIZE, TILE_SIZE))

    entities = update_level("jardin", player, platforms)
    
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

class Entity(pygame.sprite.Sprite):
    def __init__(self, color, pos, *groups):
        super().__init__(*groups)
        self.image = Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

class Player(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(Color("#0000FF"), pos)
        self.vel = pygame.Vector2((0, 0))
        self.onGround = False
        self.platforms = platforms
        self.speed = 8
        self.jump_strength = 15
        
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
                if isinstance(p, Door):
                    print("Update to sala")
                    update_level("sala", self, platforms)
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

class Wall(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#b4b1ae"), pos, *groups)

class Ground(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#95a984"), pos, *groups)

class Door(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#616667"), pos, *groups)

class Enemy(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#faa0a0"), pos, *groups)

class Xtroy(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#766333"), pos, *groups)

class Alt(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#fffb00"), pos, *groups)

if __name__ == "__main__":
    main()