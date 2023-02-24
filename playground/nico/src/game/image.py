import obj
import pygame as pg
from pygame.locals import *
from abc import abstractmethod


class AbsImage(obj.ObjStaticR):
	@abstractmethod
	def __init__(self, INST_ID):
		obj.ObjStaticR.__init__(self, INST_ID)
		self.watchers = 1

	def watch(self):
		self.watchers += 1

	def leave(self):
		if self.watchers > 1:
			self.watchers -= 1
		else:
			self.close()


class Image(AbsImage):
	CLASS_ID = 0
	GRP_FILE = "game/data/images.json"

	def __init__(self, INST_ID, file):
		AbsImage.__init__(self, INST_ID)
		self.image = pg.image.load(file)

images = obj.Group(Image)

class SpriteSheet(AbsImage, obj.draw.SpriteSheet):
	CLASS_ID = 1
	GRP_FILE = "game/data/sprite_sheets.json"

	def __init__(self, INST_ID, file, w, h, colorkey=None):
		AbsImage.__init__(self, INST_ID)
		obj.draw.SpriteSheet.__init__(self, pg.image.load(file), w, h, colorkey)


spriteSheets = obj.Group(SpriteSheet)
