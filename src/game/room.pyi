from typing import (
	List,
	Dict,
	Final,
	Any
)
import pygame as pg
from game.cam import Cam


class RoomDirector(obj.ObjStaticR, obj.ObjUpdate):
	MAX_ROOMS:Final[int]
	CAM:Final[Cam]
	unloadRooms:List[Dict[str, Any]]
	loadRooms:List[Dict[str, Any]]
	def __init__(self, HASH:int, FATHR_HASH:int, rooms:int, camID:int)->None: ...
	def update(self)->None: ...
	def close(self)->None: ...
