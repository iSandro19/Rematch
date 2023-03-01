import obj
import pygame as pg


class Cam(obj.ObjStaticR, pg.Rect):
	GRP_FILE = "game/data/cams.json"

	def __init__(self, HASH, FATHR_HASH, pos):
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
		pg.Rect.__init__(self, pos)

	def move_ip(self, x, y):
		pg.Rect.move_ip(self, x, y)

try:
	obj.getGroup(Cam)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Cam))
