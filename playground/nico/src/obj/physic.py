from obj.draw import ObjRelative
import pygame as pg
from abc import abstractmethod


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
		self.pos.move_ip(self.vel)