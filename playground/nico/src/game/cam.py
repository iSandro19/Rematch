import obj
import pygame as pg


class Cam(obj.ObjDynamic, pg.Rect):
	def __init__(self, INST_ID, x, y, w, h):
		obj.ObjStaticR.__init__(INST_ID)
		pg.Rect.__init__(self, x, y, w, h)

	def move_ip(self, x, y):
		self.move_ip(x, y)