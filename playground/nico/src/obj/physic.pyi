from typing import (
	Final
)
from obj.draw import ObjRelative
import pygame as pg
from abc import abstractmethod


class ObjPhysic(ObjRelative):
	vel:pg.math.Vector2
	acc:pg.math.Vector2
	@abstractmethod
	def __init__(self, INST_ID:int)->None: ...
	@abstractmethod
	def update(self): ...
	def updateVel(self)->None: ...
	def updateRect(self)->None: ...