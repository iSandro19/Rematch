from typing import (
	List,
	Dict,
	Tuple,
	Union,
	Callable
)
import pygame as pg
from pygame.locals import *
import obj


class Player(obj.ObjState, obj.ObjPhysic):
	# Actions
	
	def __init__(self): ...

	def goRight(self): ...

	def goLeft(self): ...

	def stop(self): ...


	# States

	def _standing(self): ...

	def _walking(self): ...