import obj
import pygame as pg
from pygame.locals import *
from abc import abstractmethod


class AbsImage(obj.ObjStaticR):
	@abstractmethod
	def __init__(self, HASH, FATHR_HASH):
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
		self.watchers = 1

	def watch(self):
		self.watchers += 1

	def leave(self):
		if self.watchers > 1:
			self.watchers -= 1
		else:
			self.close()


class Surface(AbsImage):
	GRP_FILE = "game/data/surfaces.json"

	def __init__(self, HASH, FATHR_HASH, file):
		AbsImage.__init__(self, HASH, FATHR_HASH)
		self._image = pg.image.load(file)

	@property
	def image(self):
		return self._image
	
try:
	obj.getGroup(Surface)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Surface))


class SpriteSheet(AbsImage, obj.draw.SpriteSheet):
	GRP_FILE = "game/data/sprite_sheets.json"

	def __init__(self, HASH, FATHR_HASH, file, w, h, colorkey=None):
		AbsImage.__init__(self, HASH, FATHR_HASH)
		obj.draw.SpriteSheet.__init__(self, pg.image.load(file), w, h, colorkey)

try:
	obj.getGroup(SpriteSheet)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(SpriteSheet))
