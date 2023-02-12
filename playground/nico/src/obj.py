from abc import ABC, abstractmethod
import numpy as np
from multiprocessing import Pool
from csrmat import CSRMat


def _objUpdate(obj):
	obj.update()
		
class ObjInsts(list):
	def __init__(self, iterable=())->None:
		super().__init__(iterable)

	def update(self)->None: 
		self = list(map(_objUpdate, self))

class ObjInstsCon(ObjInsts):
	def __init__(self, iterable=())->None:
		super().__init__(iterable)

	def update(self)->None:
		with Pool() as p:
			self = list(p.map(_objUpdate, self))

class ObjsTable(np.ndarray):
	def __init__(self, iterable=())->None:
		super().__init__(iterable, dtype=np.uint)

class Obj(ABC):
	@abstractmethod
	def __init__(self)->None: ...
	@abstractmethod
	def update(self)->None: ...

class ObjDynamic(Obj):
	pass

class ObjStatic(Obj):
	pass

class ParamError(Exception):
	def __init__(self, msg=""):
		super().__init__(msg)

class FinishedError(Exception):
	def __init__(self, msg=""):
		super().__init__(msg)

class ObjState(Obj):
	@abstractmethod
	def __init__(self)->None:
		pass

	def setStates(states):
		ObjState._states = np.array(states)
	def setArcs(arcs):
		ObjState._arcs = csrmat(arcs)

	def next(self, act):
		for row in ObjState._arcs[self.state]:
			for acts, nextState in row:
				if act in acts:
					self.state = nState
					return
		raise ParamError("{} not allowed in state {}".format(act, self.state))

	def update(self):
		iState = self.state-1

		if iState != -1:
			self._states[iState](self)
		else:
			raise FinishedError()