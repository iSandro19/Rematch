from typing import (
	Final
)
from obj.base import ObjDraw, ObjUpdate
import pygame as pg
from abc import abstractmethod


class ObjRelative(ObjDraw):
	REF_POINT:Final[pg.Rect]
	pos:pg.Rect
	@abstractmethod
	def __init__(
		self,
		HASH:int,
		FATHR_HASH:int,
		image:pg.Surface,
		rect:pg.Rect,
		REF_POINT:pg.Rect,
		pos:pg.math.Vector2
	)->None: ...
	def draw(self)->None: ...

class ObjParallax(ObjRelative):
	Z_OFFSET:Final[float]
	@abstractmethod
	def __init__(
		self,
		HASH:int,
		FATHR_HASH:int,
		image:pg.Surface,
		rect:pg.Rect,
		REF_POINT:pg.Rect,
		pos:pg.math.Vector2,
		Z_OFFSET:float
	)->None: ...
	def draw(self)->None: ...

class ObjPhysic(ObjRelative, ObjUpdate):
	vel:pg.math.Vector2
	acc:pg.math.Vector2
	cBox:pg.Rect
	@abstractmethod
	def __init__(
		self,
		HASH:int,
		FATHR_HASH:int,
		image:pg.Surface,
		rect:pg.Rect,
		REF_POINT:pg.Rect,
		pos:pg.math.Vector2,
		cBoxOffsetH:int,
		cBoxOffsetV:int,
		cBoxW:int,
		cBoxH:int,
		acc:pg.math.Vector2,
		vel:pg.math.Vector2
	)->None: ...
	def updateX(self)->None: ...
	def updateY(self)->None: ...
	def update(self)->None: ...
