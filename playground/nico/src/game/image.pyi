from typing import (
	Optional,
	Iterable
)
import obj
import pygame as pg
from abc import abstractmethod


class AbsImage(obj.ObjStaticR):
	@abstractmethod
	def __init__(self, INST_ID:int)->None: ...
	def watch(self)->None: ...
	def leave(self)->None: ...

class Image(obj.ObjStaticR):
	image:pg.Surface
	watchers:int
	def __init__(self, INST_ID:int, file:str)->None: ...
	def watch(self)->None: ...
	def leave(self)->None: ...

class SpriteSheet(obj.ObjStaticR, obj.draw.SpriteSheet):
	def __init__(
		self,
		INST_ID:int,
		file:str,
		w:int,
		h:int,
		colorkey:Optional[pg.Color]
	)->None: ...
	def watch(self)->None: ...
	def leave(self)->None: ...

class Images(obj.ObjInstsStaticR):
	def __init__(self, iterable:Optional[Iterable[Image]])->None: ...

class SpriteSheets(obj.ObjInstsStaticR):
	def __init__(self, iterable:Optional[Iterable[SpriteSheet]])->None: ...