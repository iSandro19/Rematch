import obj
import pygame as pg

class VisibleArea(obj.ObjStaticR, pg.Rect):
	GRP_FILE = "game/data/visible_areas.json"

	def __init__(self, HASH, FATHR_HASH, rect):
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
		pg.Rect.__init__(self, rect)

try:
	obj.getGroup(VisibleArea)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(VisibleArea))


class Cam(obj.ObjStaticR, pg.Rect):
	GRP_FILE = "game/data/cams.json"

	def __init__(self, HASH, FATHR_HASH, rect):
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
		pg.Rect.__init__(self, rect)

	def correctPos(self):
		for va in obj.getGroup(VisibleArea):
			if va.collidepoint(self.center):
				self.clamp_ip(va)

try:
	obj.getGroup(Cam)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Cam))
