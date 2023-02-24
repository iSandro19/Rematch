from typing import (
	Dict,
	List,
	Tuple,
	Callable,
	Iterable,
	Iterator,
	Optional,
	Final,
	Any,
	TypeVar,
	Generic,
	Union
)
from abc import ABC, abstractmethod
import pygame as pg


class Obj(ABC):
	CLASS_ID:Final[int]
	INST_ID:Final[int]
	active:bool
	@abstractmethod
	def __init__(self, INST_ID:int)->None: ...
	def close(self)->None: ...
	def __eq__(self, value:Any)->bool: ...
	def __ge__(self, value:Any)->bool: ...
	def __gt__(self, value:Any)->bool: ...
	def __le__(self, value:Any)->bool: ...
	def __lt__(self, value:Any)->bool: ...
	def __hash__(self)->int: ...

class ObjUpdate(Obj):
	UPDT_POS:Final[int]
	@abstractmethod
	def __init__(self, INST_ID:int)->None: ...
	@abstractmethod
	def update(self): ...

class ObjDraw(Obj):
	DRAW_LAYER:Final[int]
	image:pg.Surface
	rect:pg.Rect
	BCKGND:Final[pg.Surface]
	@abstractmethod
	def __init__(
		self,
		INST_ID:int,
		image:pg.Surface,
		rect:pg.Rect
	)->None: ...
	def draw(self)->None: ...

class ObjDynamic(Obj):
	@abstractmethod
	def __init__(self)->None: ...

class ObjStaticR(Obj):
	GRP_FILE:Final[str]
	@abstractmethod
	def __init__(self, INST_ID:int)->None: ...
	def load(cls, INST_ID:int)->ObjStaticR: ...

class ObjStaticRW(ObjStaticR):
	@abstractmethod
	def __init__(self, INST_ID:int)->None: ...
	def load(cls, INST_ID:int)->ObjStaticRW: ...
	@abstractmethod
	def save(self)->None: ...
	def _save(self, **obj:Any)->None: ...



class ObjInstNotFoundError(Exception):
	def __init__(self, class_id:int, inst_id:int)->None: ...

T = TypeVar("T")
class Group(Generic[T]):
	OBJS_TYPE:Final[type]
	OBJS:List[T]
	@abstractmethod
	def __init__(self, OBJS_TYPE:type)->None: ...
	def add(self, obj:T)->None: ...
	def __getitem__(self, inst_id:int)->T: ...
	def __delitem__(self, inst_id:int)->T: ...
	def __iter__(self)->Iterator[T]: ...
	def __str__(self)->str: ...
	def __repr__(self)->str: ...


class GroupsTable(Tuple[Obj]):
	def __new__(
		self, iterable:Optional[Iterable[Group[Obj]]]
	)->GroupsTable: ...

# Variable global para contener las clases de objetos (filas)
# y sus intancias (columnas) con el fin de que estas se comuniquen.
GRPS_TABLE:Final[GroupsTable]

class UpdatingPipeline(Tuple[ObjUpdate]):
	def __new__(
		self,
		iterable:Optional[Iterable[Group[ObjUpdate]]]
	)->UpdatingPipeline: ...
	def update(self)->None: ...

# Variable global para contener las clases de objetos actualizables
# (filas) y sus intancias (columnas) con el fin de actualizarlos en
# el orden en que se situan en el pipeline.
UPDT_PL:Final[UpdatingPipeline]

class DrawingPipeline(Tuple[ObjDraw]):
	def __new__(
		self,
		iterable:Optional[Iterable[Group[ObjDraw]]]
	)->DrawingPipeline: ...
	def draw(self)->None: ...

# Variable global para contener las clases de objetos dibujables
# (filas) y sus intancias (columnas) con el fin de dibujarlos en
# el orden en que se situan en el pipeline sobre el fondo.
DRAW_PL:Final[DrawingPipeline]

def setGroups(*groups:Group[Obj])->None: ...

def getGroups(class_ids:Union[int, slice])->Union[Group[Obj], GroupsTable]: ...

def update()->None: ...

def draw()->None: ...

def loadR(class_id:int, inst_id:int)->ObjStaticR: ...

def loadRW(class_id:int, inst_id:int)->ObjStaticRW: ...
