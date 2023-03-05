from typing import (
	Tuple,
	Iterable,
	Iterator,
	Optional,
	Final
)
import pygame as pg
from abc import abstractmethod
from obj.base import ObjDraw


class SpriteSheet:
	SHEET:Final[pg.Surface]
	clip:pg.Rect
	w:Final[int]
	h:Final[int]
	def __init__(
		self,
		SHEET:pg.Surface,
		w:int,
		h:int,
		colorkey:Optional[pg.Color]
	)->None: ...
	def __getitem__(self, rowXcol:Tuple[int, int])->pg.Surface: ...

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
		FLIP_X:Optional[bool],
		FLIP_Y:Optional[bool],
		DUR:Optional[float]
	)->None: ...

class ObjSprite(ObjDraw):
	SPRTS:Final[SpriteSheet]
	frame:Frame
	@abstractmethod
	def __init__(
		self,
		HASH:int,
		FATHR_HASH:int,
		SPRTS:SpriteSheet,
		x:int,
		y:int
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
	anim:Animation
	_frame:Frame
	_frameIt:Iterator[Frame]
	_steps:float
	speed:float
	done:bool
	@abstractmethod
	def __init__(
		self,
		HASH:int,
		FATHR_HASH:int,
		SPRTS:SpriteSheet,
		x:int,
		y:int
	)->None: ...
	def draw(self)->None: ...
