import obj
import pygame as pg
from game.image import SpriteSheet
from game.image import Surface
from game.cam import Cam


class Boton(obj.ObjStaticR, obj.ObjDraw, obj.ObjUpdate):
     
    GRP_FILE = "game/data/botones.json"
    DRAW_LAYER = 12
    UPDT_POS = 0

    def __init__(self, HASH, FATHR_HASH, sprtShtHash, x, y):

        self.selected = False

        try:
            self._sprtSht = obj.getGroup(SpriteSheet)[sprtShtHash]
            self._sprtSht.watch()
        except obj.ObjNotFoundError:
            self._sprtSht = obj.load(SpriteSheet, sprtShtHash, HASH)

        rect = pg.Rect(x,y, self._sprtSht.clip.w, self._sprtSht.clip.h)

        obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
        obj.ObjDraw.__init__(self, HASH, FATHR_HASH, sprtShtHash, rect)
        obj.ObjUpdate.__init__(self, HASH, FATHR_HASH)


    def isSelected(self): return self.selected

    def update(self):
        self.selected = self.rect.collidepoint(pg.mouse.get_pos())

        if self.selected:  self.image = self._sprtSht[0,0]
        else: self.image = self._sprtSht[1,0]

    def close(self):
        self._sprtSht.leave()
        obj.Obj.close(self)

try:
	obj.getGroup(Boton)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Boton))


class PauseMenu(obj.ObjDraw, obj.ObjDynamic):


    DRAW_LAYER = 11

    def __init__(self, FATHR_HASH):

        obj.ObjDynamic.__init__(self, FATHR_HASH)

        self.surfHash = 9

        try:
            self.surf = obj.getGroup(Surface)[self.surfHash]
            self.surf.watch()
        except obj.ObjNotFoundError:
            self.surf = obj.load(Surface, self.surfHash, hash(self))

        obj.ObjDraw.__init__(self, hash(self), FATHR_HASH, self.surf.image, self.surf.image.get_rect().move(72, 11))

        self.botonC = obj.load("Boton", 0, 0)
        self.botonS = obj.load("Boton", 1, 0)


    def close(self):
        self.botonC.close()
        self.botonS.close()
        self.surf.leave()
        obj.Obj.close(self)

try:
	obj.getGroup(PauseMenu)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(PauseMenu))
        

class Parpadeables(obj.ObjStaticR, obj.ObjDraw):
     
    GRP_FILE = "game/data/parpadeables.json"
    DRAW_LAYER = 13

    def __init__(self, HASH, FATHR_HASH, sprtShtHash, x, y):

        self.visible = False
        self.i = 0

        try:
            self._sprtSht = obj.getGroup(SpriteSheet)[sprtShtHash]
            self._sprtSht.watch()
        except obj.ObjNotFoundError:
            self._sprtSht = obj.load(SpriteSheet, sprtShtHash, HASH)

        rect = pg.Rect(x,y, self._sprtSht.clip.w, self._sprtSht.clip.h)

        obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
        obj.ObjDraw.__init__(self, HASH, FATHR_HASH, sprtShtHash, rect)
        obj.ObjUpdate.__init__(self, HASH, FATHR_HASH)

    def draw(self):
        self.i += 1

        if self.i < 30: self.visible = True
        elif self.i < 60: self.visible = False
        else: self.i = 0


        if self.visible:  self.image = self._sprtSht[0,0]
        else: self.image = self._sprtSht[1,0]

        obj.ObjDraw.draw(self)

    def close(self):
        self._sprtSht.leave()
        obj.Obj.close(self)

try:
	obj.getGroup(Parpadeables)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Parpadeables))
        
class MainMenu (obj.ObjDraw, obj.ObjDynamic):

    DRAW_LAYER = 11

    def __init__(self, FATHR_HASH):

        obj.ObjDynamic.__init__(self, FATHR_HASH)

        self.surfHash = 10

        try:
            self.surf = obj.getGroup(Surface)[self.surfHash]
            self.surf.watch()
        except obj.ObjNotFoundError:
            self.surf = obj.load(Surface, self.surfHash, hash(self))

        obj.ObjDraw.__init__(self, hash(self), FATHR_HASH, self.surf.image, self.surf.image.get_rect())

        self.botonC = obj.load("Boton", 2, 0)
        self.botonS = obj.load("Boton", 3, 0)


    def close(self):
        self.botonC.close()
        self.botonS.close()
        self.surf.leave()
        obj.Obj.close(self)

try:
	obj.getGroup(MainMenu)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(MainMenu))


DM_SURF_HASH = 18

class DeadMenu(obj.ObjDynamic, obj.ObjDraw):
    DRAW_LAYER = 12
    UPDT_POS = 0

    def __init__(self, FATHR_HASH):
        obj.ObjDynamic.__init__(self, FATHR_HASH)

        try:
            self._surf = obj.getGroup(Surface)[DM_SURF_HASH]
            self._surf.watch()
        except obj.ObjNotFoundError:
            self._surf = obj.load(Surface, DM_SURF_HASH, hash(self))

        obj.ObjDraw.__init__(self, hash(self), FATHR_HASH, self._surf.image, self._surf.image.get_rect())


    def draw(self):
        obj.ObjDraw.draw(self)
        self.active = False

    def close(self):
        self._surf.leave()
        obj.Obj.close(self)

try:
    obj.getGroup(DeadMenu)
except obj.GroupNotFoundError:
    obj.addGroup(obj.Group(DeadMenu))
