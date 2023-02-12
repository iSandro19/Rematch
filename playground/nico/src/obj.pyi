from typing import (
	List,
	Dict,
	Tuple,
	Union,
	Callable,
	Iterable,
	Final,
	Any
)
from abc import ABC, abstractmethod
import numpy as np
from csrmat import CSRMat


class ObjInsts(list):
	def __init__(self, iterable:Iterable['Obj'])->None: ...
	def update(self)->None: ...

class ObjInstsCon(ObjInsts):
	def __init__(self, iterable:Iterable['Obj'])->None: ...
	def update(self)->None: ...

class ObjsTable(np.ndarray):
	def __init__(self, iterable:Iterable[ObjInsts])->None: ...

class Obj(object):
	CLASS_ID:Final[np.uint]
	objs:ObjsTable
	@abstractmethod
	def __init__(self)->None: ...
	@abstractmethod
	def update(self)->None: ...

class ObjDynamic(Obj):
	@abstractmethod
	def __init__(self)->None: ...
	@abstractmethod
	def update(self)->None: ...

class ObjStatic(Obj):
	INST_ID:Final[np.uint]
	@abstractmethod
	def __init__(self)->None: ...
	@abstractmethod
	def update(self)->None: ...

class ObjState(Obj):
	state:int
	@abstractmethod
	def __init__(self)->None: ...
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
	def next(self, act:Callable[['ObjState', Any, Any], Any])->None: ...
	def update(self)->None: ...