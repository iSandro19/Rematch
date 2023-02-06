from typing import List, Dict, Tuple, Union, Callable


class ParamError(Exception):
	def __init__(self, msg:str=""):
		super(ParamError, self).__init__(msg)

class FinishedError(Exception):
	def __init__(self, msg:str=""):
		super(FinishedError, self).__init__(msg)

class ObjState(object):
	state:int = 0
	states:List[Callable[[object], None]] = None
	arcs:List[List[List[Callable[[object], object]]]] = None

	def next(self, act:Callable[[object], object])->None:
		for nState in range(len(self.arcs)):
			if act in self.arcs[self.state][nState]:
				self.state = nState
				return

		raise ParamError("{} not allowed in state {}".format(act, self.state))

	def update(self):
		iState = self.state-1

		if iState != -1:
			self.states[iState](self)
		else:
			raise FinishedError()
