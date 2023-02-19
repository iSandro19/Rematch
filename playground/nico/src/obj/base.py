from abc import ABC, abstractmethod
from multiprocessing import Pool
from bisect import insort
import ijson
import json


def _update(obj):
	obj.update()
		
class ObjInsts(list):
	@abstractmethod
	def __init__(self, iterable=()):
		list.__init__(self, iterable)

	def add(self, obj):
		insort(self, obj)

	def __getitem__(self, inst_id):
		for obj in self:
			if obj.INST_ID == inst_id:
				return obj
			elif obj.INST_ID > inst_id:
				raise ValueError(
					"object with CLASS_ID={} and INST_ID={} not found".format(
						obj.CLASS_ID,
						inst_id
					)
				)

class ObjInstsUpdate(ObjInsts):
	@abstractmethod
	def __init__(self, iterable=()):
		ObjInsts.__init__(iterable)

	def update(self): 
		map(_update, self)

class ObjInstsUpdateCon(ObjInstsUpdate):
	@abstractmethod
	def __init__(self, iterable=()):
		ObjInstsUpdate.__init__(iterable)

	def update(self):
		with Pool() as p:
			p.map(_update, self)

class ObjInstsDynamic(ObjInsts):
	@abstractmethod
	def __init__(self, iterable=()):
		ObjInsts.__init__(iterable)

class ObjInstsStaticR(ObjInsts):
	@abstractmethod
	def __init__(self, iterable=()):
		ObjInsts.__init__(iterable)

	def load(self, inst_id):
		return self.OBJ_CLASS.load(self.OBJ_CLASS, inst_id)

class ObjInstsStaticRW(ObjInstsStaticR):
	@abstractmethod
	def __init__(self, iterable=()):
		ObjInstsStatic_R.__init__(iterable)

	def save(self, inst_id, obj):
		self.OBJ_CLASS.save(self[inst_id], obj)


class Table(tuple):
	def __init__(self, iterable=()):
		tuple.__init__(iterable)

class Pipeline(tuple):
	def __init__(self, iterable=()):
		tuple.__init__(iterable)

	def update(self): 
		map(_update, self)


class Obj(ABC):
	@abstractmethod
	def __init__(self, INST_ID):
		self.INST_ID = INST_ID
		TABLE[self.CLASS_ID].add(self)

	def __eq__(self, value):
		return self.INST_ID == value.INST_ID

	def __ge__(self, value):
		return self.INST_ID >= value.INST_ID

	def __gt__(self, value):
		return self.INST_ID > value.INST_ID

	def __le__(self, value):
		return self.INST_ID <= value.INST_ID

	def __lt__(self, value):
		return self.INST_ID < value.INST_ID

	def __hash__(self):
		return self.INST_ID

class ObjUpdate(Obj):
	@abstractmethod
	def __init__(self, INST_ID):
		Obj.__init__(self, INST_ID)

	@abstractmethod
	def update(self):
		pass

class ObjDynamic(Obj):
	@abstractmethod
	def __init__(self):
		Obj.__init__(self, object.__hash__(self))

class ObjStaticR(Obj):
	@abstractmethod
	def __init__(self, INST_ID):
		Obj.__init__(self, INST_ID)

	def load(cls, inst_id):
		with open(cls.INST_FILE, "r") as fp:
			i = 0
			for obj in ijson.items(fp, "item"):
				if i < inst_id:
					i += 1
				else:
					return cls(inst_id, **obj)
			raise ValueError(
				"object with CLASS_ID={} and INST_ID={} not found".format(
					cls.CLASS_ID,
					inst_id
				)
			)


class ObjStaticRW(ObjStaticR):
	@abstractmethod
	def __init__(self, INST_ID):
		Obj.__init__(self, INST_ID)

	def save(self, obj):
		with open(self.INST_FILE, "r") as fp:
			instList = json.load(fp)

		if self.INST_ID < len(instList):
			instList[self.INST_ID] = obj
		else:
			raise ValueError(
				"object with CLASS_ID={} and INST_ID={} not found".format(
					cls.CLASS_ID,
					inst_id
				)
			)

		with open(self.INST_FILE, "w") as fp:
			json.dump(fp, instList)
