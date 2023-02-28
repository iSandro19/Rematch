from typing import (
	Any
)
import obj
import pygame as pg


class Cam(obj.ObjDynamic, pg.Rect):
	def __init__(
		self,
		HASH:int,
		FATHR_HASH:int,
		x:int,
		y:int,
		w:int,
		h:int
	)->None: ...
	def move_ip(self, x:Any, y:int)->None: ...