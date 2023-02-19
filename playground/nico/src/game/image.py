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
			del obj.TABLE[self.CLASS_ID][self.INST_ID]

class Image(AbsImage):
	CLASS_ID = 0
	INST_FILE = "obj/data/images.json"

	def __init__(self, INST_ID, file):
		AbsImage.__init__(self, INST_ID)
		self.image = pg.image.load(file)
		
class SpriteSheet(AbsImage, obj.draw.SpriteSheet):
	CLASS_ID = 1
	INST_FILE = "obj/data/sprite_sheets.json"

	def __init__(self, INST_ID, file, w, h, colorkey=None):
		AbsImage.__init__(self, INST_ID)
		obj.draw.SpriteSheet.__init__(self, pg.image.load(file), w, h, colorkey)

class Images(obj.ObjInstsStaticR):
	OBJ_CLASS = Image

	def __init__(self, iterable=()):
		obj.ObjInstsStaticR.__init__(self, iterable)

class SpriteSheets(obj.ObjInstsStaticR):
	OBJ_CLASS = SpriteSheet

	def __init__(self, iterable=()):
		obj.ObjInstsStaticR.__init__(self, iterable)
