from typing import (
	Tuple,
	Iterable,
	Iterator,
	Optional,
	Final
)
import pygame as pg
from abc import abstractmethod
from obj.base import ObjDraw, ObjUpdate


class SpriteSheet:
	SHEET:Final[pg.Surface]
	clip:pg.Rect
	def __init__(
		self,
		SHEET:pg.Surface,
		w:int,
		h:int,
		colorkey:Optional[pg.Color]
	)->None: ...
	def __getitem__(self, rowXcol:Tuple[int, int])->pg.Surface: ...

class ObjSprite(ObjDraw):
	SPRTS:Final[SpriteSheet]
	row:int
	col:int
	@abstractmethod
	def __init__(
		self,
		INST_ID:int,
		SPRTS:SpriteSheet,
		row:int,
		col:int,
		x:int,
		y:int
	)->None: ...


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

class ObjAnim(ObjDraw, ObjUpdate):
	SPRTS:Final[SpriteSheet]
	_anim:Animation
	_frame:Frame
	_frameIt:Iterator[Frame]
	_steps:float
	speed:float
	done:bool
	@abstractmethod
	def __init__(self, INST_ID:int, SPRTS:SpriteSheet, x:int, y:int)->None: ...
	def startAnim(self, anim:Animation)->None: ...
	def update(self)->None: ...

class ObjRelative(ObjDraw, ObjUpdate):
	REF_POINT:Final[pg.Rect]
	pos:pg.Rect
	@abstractmethod
	def __init__(
		self,
		INST_ID:int,
		image:pg.Surface,
		rect:pg.Rect
	)->None: ...
	def update(self)->None: ...

class ObjParallax(ObjRelative):
	Z_OFFSET:Final[float]
	@abstractmethod
	def __init__(
		self,
		INST_ID:int,
		image:pg.Surface,
		rect:pg.Rect,
		Z_OFFSET:float
	)->None: ...
	def update(self)->None: ...