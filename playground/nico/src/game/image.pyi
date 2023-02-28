from typing import (
	Optional,
	Iterable,
	Final
)
import obj
import pygame as pg
from abc import abstractmethod


class AbsImage(obj.ObjStaticR):
	watchers:int
	@abstractmethod
	def __init__(self, HASH:int, FATHR_HASH:int)->None: ...
	def watch(self)->None: ...
	def leave(self)->None: ...


class Surface(obj.ObjStaticR, pg.Surface):
	def __init__(self, HASH:int, FATHR_HASH:int, file:str)->None: ...


class SpriteSheet(obj.ObjStaticR, obj.draw.SpriteSheet):
	def __init__(
		self,
		HASH:int,
		FATHR_HASH:int,
		file:str,
		w:int,
		h:int,
		colorkey:Optional[pg.Color]
	)->None: ...
