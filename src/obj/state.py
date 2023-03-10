from obj.base import ObjUpdate
from csrmat import CSRMat
from abc import abstractmethod


class FinishedError(Exception):
	def __init__(self, type, hash):
		Exception.__init__(
			"ObjState with type=%d and hash=%d \
			is unnitialized and can't be updated"%(
				type, hash
			)
		)

class ObjState(ObjUpdate):
	state = 0

	@abstractmethod
	def __init__(self, HASH, FATHR_HASH):
		ObjUpdate.__init__(self, HASH, FATHR_HASH)

	@classmethod
	def setSTATES(cls, *STATES):
		cls.STATES = STATES

	@classmethod
	def setARCS(cls, *ARCS):
		if len(ARCS) == 1:
			ARCS = ARCS[0]
			
		cls.ARCS = CSRMat(ARCS)

	def next(self, act):
		for nextState, acts in self.ARCS[self.state]:
			if act in acts:
				self.state = nextState
				return
		raise ValueError("{} not allowed in state {}".format(act, self.state))

	def update(self):
		if self.state != 0:
			self.STATES[iState](self.state-1)
		else:
			raise FinishedError(self.CLASS_ID, self.HASH)
