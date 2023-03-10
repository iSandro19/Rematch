from typing import (
	Tuple,
	Union,
	Iterable,
	Generic,
	TypeVar,
	Optional,
	Final,
	overload,
	SupportsIndex,
	Dict,
	Any
)
import numpy as np


T = TypeVar('T')

class CSRMatIterator(Generic[T]):
	def __init__(self, csrMat:'CSRMat')->None: ...
	def __iter__(self)->'CSRMatIterator': ...
	def __next__(self)->Tuple[Node, ...]: ...

class Node(Tuple[int, T]):
	x:Final[SupportsIndex]
	d:T
	def __new__(
		cls,
		*args:Union[int, T, Tuple[int, T]],
		**kwargs:Union[int, T]
	)->"Node": ...
	def __str__(self)->str: ...
	def __repr__(self)->str: ...

class CSRMat(Generic[T]):
	null:Optional[T]
	shape:Final[Tuple[int, int]]
	asdict:Dict[str, Any]
	def __init__(
		self,
		matrix:Iterable[Iterable[T]],
		none:Optional[T],
		dtype=Optional[np.number]
	)->None: ...
	"""
	@overload
	def __getitem__(self, indices:int)->Tuple[Node, ...]: ...
	@overload
	def __getitem__(
		self,
		indices:Union[
			Iterable[SupportsIndex],
			Union[slice, Tuple[slice]],
			Union[None, Tuple[Node]],
			Union[EllipsisType, Tuple[EllipsisType]]
		]
	)->Tuple[Tuple[Node, ...], ...]: ...
	@overload
	def __getitem__(
		self,
		indices:Tuple[
			Union[SupportsIndex, Tuple[SupportsIndex]],
			Union[SupportsIndex, Tuple[SupportsIndex]]
		]
	)->Optional[T]: ...
	@overload
	def __getitem__(
		self, 
		indices:Tuple[
			Union[
				Iterable[SupportsIndex],
				Union[slice, Tuple[slice]],
				Union[None, Tuple[Node]],
				Union[EllipsisType, Tuple[EllipsisType]]
			],
			Union[
				Iterable[int],
				Union[slice, Tuple[slice]],
				Union[None, Tuple[Node]],
				Union[EllipsisType, Tuple[EllipsisType]]
			]
		]
	)->Tuple[Tuple[Optional[T], ...], ...]: ...
	"""
	def __iter__(self)->CSRMatIterator[T]: ...
	def __str__(self)->str: ...
	def __repr__(self)->str: ...
