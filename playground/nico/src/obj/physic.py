from obj.draw import ObjDraw
import pygame as pg
from abc import abstractmethod


class ObjRelative(ObjDraw):
	@abstractmethod
	def __init__(self, INST_ID):
		ObjDraw.__init__(self, INST_ID)

	@abstractmethod
	def update(self):
		pass

	def relativizeRect(self):
		self.rect.x = self.pos.x - self.REF_POINT.x
		self.rect.y = self.pos.y - self.REF_POINT.y

class ObjPhysic(ObjRelative):
	@abstractmethod
	def __init__(self, INST_ID):
		ObjRelative.__init__(self, INST_ID)

	@abstractmethod
	def update(self):
		pass

	def updateVel(self):
		self.vel.x += self.acc.x
		self.vel.y += self.acc.y

	def updatePos(self):
		self.pos += self.vel