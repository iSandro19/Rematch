from typing import (
	Tuple,
	Iterable,
	Iterator,
	Optional,
	Final
)
import pygame as pg
from abc import abstractmethod
from obj.base import ObjUpdate


class ObjDraw(ObjUpdate, pg.sprite.Sprite):
	@abstractmethod
	def __init__(self, INST_ID:int)->None: ...
	@abstractmethod
	def update(self): ...


class SpriteSheet:
	SHEET:Final[pg.Surface]
	_clip:pg.Rect
	def __init__(
		self,
		SHEET:pg.Surface,
		w:int,
		h:int,
		colorkey:Optional[pg.Color]
	)->None: ...
	def __getitem__(self, rowXcol:Tuple[int, int])->pg.Surface: ...

class ObjTile(ObjDraw):
	SPRTS:Final[SpriteSheet]
	@abstractmethod
	def __init__(self, INST_ID:int)->None: ...
	@abstractmethod
	def update(self): ...
	def updateImage(self, row:int, col:int)->None: ...


class Frame:
	COL:Final[int]
	ROW:Final[int]
	DUR:Final[float]
	FLIP_X:Final[bool]
	FLIP_Y:Final[bool]
	def __init__(
		self,
		COL:int,
		ROW:int,
		DUR:Optional[float],
		FLIP_X:Optional[bool],
		FLIP_Y:Optional[bool]
	)->None: ...

class Animation(tuple):
	LOOP:Final[bool]
	FLIP_X:Final[bool]
	FLIP_Y:Final[bool]
	def __new__ (
		cls,
		FRAMES:Iterable[Frame],
		LOOP:Optional[bool]
	)->Animation: ...
	def __init__(
		self,
		FRAMES:Iterable[Frame],
		LOOP:Optional[bool]
	)->None: ...

class ObjAnim(ObjDraw):
	SPRTS:Final[SpriteSheet]
	_anim:Animation
	_frame:Frame
	_frameIt:Iterator[Frame]
	_steps:float
	speed:float
	done:bool
	@abstractmethod
	def __init__(self, INST_ID:int)->None: ...
	@abstractmethod
	def update(self): ...
	def startAnim(self, anim:Animation)->None: ...
	def updateImage(self)->None: ...
