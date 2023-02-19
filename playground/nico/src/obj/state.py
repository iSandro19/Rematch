from obj.base import ObjUpdate
from csrmat import CSRMat
from abc import abstractmethod

class ParamError(Exception):
	def __init__(self, msg=""):
		Exception.__init__(msg)

class FinishedError(Exception):
	def __init__(self, msg=""):
		Exception.__init__(msg)

class ObjState(ObjUpdate):
	state = 0

	@abstractmethod
	def __init__(self, INST_ID):
		Obj.__init__(self, INST_ID)

	def setSTATES(STATES):
		ObjState.STATES = tuple(STATES)
	def setARCS(ARCS):
		ObjState.ARCS = CSRMat(ARCS)

	def next(self, act):
		for actsXnextState in ObjState.ARCS[self.state]:
			if act in actsXnextState[0]:
				self.state = actXnextState[1]
				return
		raise ParamError("{} not allowed in state {}".format(act, self.state))

	def update(self):
		iState = self.state-1

		if iState != -1:
			ObjState.STATES[iState](self)
		else:
			raise FinishedError()
