from abc import ABC, abstractmethod
from multiprocessing import Pool
from bisect import insort
import ijson
import json
import pygame as pg
from functools import cmp_to_key

def _update(obj):
	obj.update()

def _draw(obj):
	obj.draw()

class ObjInstNotFoundError(Exception):
	def __init__(self, class_id, inst_id):
		Exception.__init__(
			self,
			"object with CLASS_ID=%d INST_ID=%d not found"%(class_id, inst_id)
		)

class ObjInsts(ABC):
	@abstractmethod
	def __init__(self, INSTS=()):
		self.INSTS = list(INSTS)

	def add(self, obj):
		insort(self.INSTS, obj)

	def __getitem__(self, inst_id):
		for obj in self:
			if obj.INST_ID == inst_id:
				return obj
			elif obj.INST_ID > inst_id:
				break
		raise ObjInstNotFoundError(self.OBJ_CLASS.CLASS_ID, inst_id)

	def __delitem__(self, inst_id):
		i = 0
		for obj in self:
			if obj.INST_ID == inst_id:
				del self.INSTS[i]
				return
			elif obj.INST_ID > inst_id:
				break
			i += 1

		raise ObjInstNotFoundError(self.OBJ_CLASS.CLASS_ID, inst_id)

	def __iter__(self):
		return iter(self.INSTS)

	def __str__(self):
		return str(self.INSTS)

class ObjInstsUpdate(ObjInsts):
	@abstractmethod
	def __init__(self, INSTS=()):
		ObjInsts.__init__(self, INSTS)

	def update(self): 
		map(_update, self)

class ObjInstsUpdateCon(ObjInstsUpdate):
	@abstractmethod
	def __init__(self, INSTS=()):
		ObjInstsUpdate.__init__(self, INSTS)

	def update(self):
		with Pool() as p:
			p.map(_update, self)

class ObjInstsDraw(ObjInstsUpdate):
	@abstractmethod
	def __init__(self, INSTS=()):
		ObjInstsUpdate.__init__(self, INSTS)

	def draw(self):
		map(_draw, self)

class ObjInstsDynamic(ObjInsts):
	@abstractmethod
	def __init__(self, INSTS=()):
		ObjInsts.__init__(self, INSTS)

class ObjInstsStaticR(ObjInsts):
	@abstractmethod
	def __init__(self, INSTS=()):
		ObjInsts.__init__(self, INSTS)

	def __getitem__(self, inst_id):
		try:
			return ObjInsts.__getitem__(self, inst_id)
		except ObjInstNotFoundError:
			return self.OBJ_CLASS.load(self.OBJ_CLASS, inst_id)

	def load(self, inst_id):
		return self.OBJ_CLASS.load(self.OBJ_CLASS, inst_id)

class ObjInstsStaticRW(ObjInstsStaticR):
	@abstractmethod
	def __init__(self, INSTS=()):
		ObjInstsStatic_R.__init__(self, INSTS)

	def save(self, inst_id, obj):
		self.OBJ_CLASS.save(self[inst_id], obj)


class Table(tuple):
	def __new__(cls, iterable=()):
		return tuple.__new__(cls, tuple(iterable))

_cmp_class_id = cmp_to_key(
	lambda o0, o1: (
		1 if o0.OBJ_CLASS.CLASS_ID > o1.OBJ_CLASS.CLASS_ID else
		0 if o0.OBJ_CLASS.CLASS_ID == o1.OBJ_CLASS.CLASS_ID else
		-1
	)
)

class UpdatingPipeline(tuple):
	def __new__(cls, iterable=()):
		return tuple.__new__(cls, tuple(iterable))

	def update(self): 
		map(_update, self)

_cmp_updt_pos = cmp_to_key(
	lambda o0, o1: (
		1 if o0.OBJ_CLASS.UPDT_POS > o1.OBJ_CLASS.UPDT_POS else
		0 if o0.OBJ_CLASS.UPDT_POS == o1.OBJ_CLASS.UPDT_POS else
		-1
	)
) 

class DrawingPipeline(tuple):
	def __new__(cls, iterable=()):
		return tuple.__new__(cls, tuple(iterable))

	def draw(self): 
		map(_draw, self)

_cmp_draw_layer = cmp_to_key(
	lambda o0, o1: (
		1 if o0.OBJ_CLASS.DRAW_LAYER > o1.OBJ_CLASS.DRAW_LAYER else
		0 if o0.OBJ_CLASS.DRAW_LAYER == o1.OBJ_CLASS.DRAW_LAYER else
		-1
	)
) 

def setObjInsts(*objInstsTuple):
	global TABLE
	global UPDT_PL
	global DRAW_PL

	TABLE = tuple(sorted(objInstsTuple, key=_cmp_class_id))

	aux = [
		objInsts
		for objInsts in objInstsTuple
		if isinstance(objInsts, ObjInstsUpdate)
	]
	aux.sort(key=_cmp_updt_pos)

	UPDT_PL = tuple(aux)

	aux = [
		objInsts
		for objInsts in objInstsTuple
		if isinstance(objInsts, ObjInstsDraw)
	]
	aux.sort(key=_cmp_draw_layer)

	DRAW_PL = tuple(aux)

class Obj(ABC):
	@abstractmethod
	def __init__(self, INST_ID):
		self.INST_ID = INST_ID
		TABLE[self.CLASS_ID].add(self)
		self.active = True

	def close(self):
		del TABLE[self.CLASS_ID][self.INST_ID]
		self.active = False

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

class ObjDraw(ObjUpdate):
	@abstractmethod
	def __init__(self, INST_ID, image, rect, BCKGND):
		ObjUpdate.__init__(self, INST_ID)
		self.image = image
		self.rect = rect
		self.BCKGND = BCKGND

	def draw(self):
		BCKGND.blit(self.image, self.rect)

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
		ObjStaticR.__init__(self, INST_ID)

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
