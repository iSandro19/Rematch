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