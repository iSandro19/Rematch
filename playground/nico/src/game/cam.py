import obj
import pygame as pg


class Cam(obj.ObjStaticR, pg.Rect):
	GRP_FILE = "game/data/cams.json"
	CLASS_ID = 4
	def __init__(self, INST_ID, rect):
		obj.ObjStaticR.__init__(self, INST_ID)
		pg.Rect.__init__(self, rect)

	def move_ip(self, x, y):
		self.move_ip(x, y)

cams = obj.Group(Cam)
