from typing import (
	Tuple,
	Union,
	Iterable,
	Generic,
	TypeVar
)
import numpy as np


T = TypeVar('T')

class CSRMatIterator(Generic[T]):
	def __init__(self, csrMat:'CSRMat')->None: ...
	def __iter__(self)->'CSRMatIterator': ...
	def __next__(self)->np.ndarray: ...

class CSRMat(Generic[T]):
	null:T
	shape:Tuple[int, int]
	def __init__(self, matrix:Iterable[Iterable[T]], null:T)->None: ...
	def __getitem__(
		self,
		indices: Union[
			Union[int, Iterable[int]],
			Tuple[Union[int, Iterable[int]],
				Union[int, Iterable[int]]
			]
		]
	)->Union[T, np.ndarray]: ...
	def __iter__(self)->CSRMatIterator: ...
