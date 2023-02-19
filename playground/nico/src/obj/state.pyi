from typing import (
	List,
	Callable,
	Iterable,
	Optional,
	Final,
	Any
)
from obj.base import ObjUpdate
from csrmat import CSRMat
from abc import abstractmethod

class ParamError(Exception):
	def __init__(self, msg:Optional[str])->None: ...

class FinishedError(Exception):
	def __init__(self, msg:Optional[str])->None: ...

class ObjState(ObjUpdate):
	_STATES:Final[tuple]
	_ARCS:Final[CSRMat]
	state:int
	@abstractmethod
	def __init__(self, INST_ID:int)->None: ...
	def setStates(
		states:Iterable[
			Callable[['ObjState'], None]
		]
	)->None: ...
	def setArcs(
		arcs:Iterable[
			Iterable[
				Iterable[
					Callable[['ObjState', Any, Any], Any]
				]
			]
		]
	)->None: ...
	def next(
		self,
		act:Callable[['ObjState', Any, Any], Any]
	)->None: ...
	def update(self)->None: ...
