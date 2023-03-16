import obj
import pygame as pg
from game.image import SpriteSheet
from game.image import Surface
from game.cam import Cam


class PauseMenu(obj.ObjStaticR, obj.physics.ObjRelative):

    GRP_FILE = "game/data/pausemenus.json"
    DRAW_LAYER = 11

    def __init__(self, HASH, FATHR_HASH, camHash, surfHash, sprtShtHash, x, y):
        
        try:
            self.surf = obj.getGroup(Surface)[surfHash]
            self.surf.watch()
        except obj.ObjNotFoundError:
            self.surf = obj.load(Surface, surfHash, HASH)
        
        try:
            self._sprtSht = obj.getGroup(SpriteSheet)[sprtShtHash]
            self._sprtSht.watch()
        except obj.ObjNotFoundError:
            self._sprtSht = obj.load(SpriteSheet, sprtShtHash, HASH)

        cam = obj.getGroup(Cam)[camHash]

        obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
        obj.physic.ObjRelative.__init__(
			self,
			HASH,
			FATHR_HASH,
			self.surf.image,
			self.surf.image.get_width(),
			self.surf.image.get_height(),
			cam,
			pg.math.Vector2(x, y)
		)

    def draw(self):
        obj.ObjDraw.draw(self)

    def close(self):
        self.surf.leave()

try:
	obj.getGroup(PauseMenu)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(PauseMenu))