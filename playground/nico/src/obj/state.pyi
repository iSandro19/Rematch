from typing import (
	List,
	Callable,
	Iterable,
	Optional,
	Final,
	Any,
	Tuple,
	Union
)
from obj.base import ObjUpdate
from csrmat import CSRMat
from abc import abstractmethod


Act = Callable[['ObjState', Any], Any]
State = Callable[['ObjState'], None]


class FinishedError(Exception):
	def __init__(self, class_id:int, inst_id:int)->None: ...

class ObjState(ObjUpdate):
	STATES:Final[Tuple[State]]#classattr
	ARCS:Final[CSRMat[Tuple[Act, ...]]]#classattr
	state:int
	@abstractmethod
	def __init__(self, HASH:int, FATHR_HASH:int)->None: ...
	@classmethod
	def setSTATES(cls, *STATES:State)->None: ...
	@classmethod
	def setARCS(
		cls,
		*ARCS:Union[
			Iterable[Iterable[State]],
			Iterable[Iterable[Iterable[State]]]
		]
	)->None: ...
	def next(self, act:Act)->None: ...
	def update(self)->None: ...
