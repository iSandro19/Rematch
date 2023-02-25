from typing import (
	Tuple,
	Dict,
	Callable,
	Iterable,
	Optional,
	Final,
	Any
)
import pygame as pg


class Room(obj.ObjStaticR, obj.ObjUpdate):
	SHAPE:Final[pg.Rect]
	OBJ_IDS:Final[Tuple[int]]
	CAM:Final[pg.Rect]
	def __init__(
		self,
		INST_ID:int,
		SHAPE:pg.Rect,
		OBJ_IDS:Iterable[int],
		CAM_INST_ID:int
	)->None: ...
	def update(self)->None: ...

class RoomDirector(obj.ObjStaticR, obj.ObjUpdate):
	ROOM_IDS:Final[Tuple[int]]
