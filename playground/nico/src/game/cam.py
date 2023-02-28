import obj
import pygame as pg


class Cam(obj.ObjStaticR, pg.Rect):
	GRP_FILE = "game/data/cams.json"

	def __init__(self, HASH, FATHR_HASH, rect):
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
		pg.Rect.__init__(self, rect)

	def move_ip(self, x, y):
		self.move_ip(x, y)

obj.addGroup(obj.Group(Cam))
