from abc import ABC, abstractmethod
from multiprocessing import Pool
from bisect import insort
import ijson
import json
import pygame as pg
from functools import cmp_to_key


class Obj(ABC):
	@abstractmethod
	def __init__(self, INST_ID):
		self.INST_ID = INST_ID
		GRPS_TABLE[self.CLASS_ID].add(self)
		self.active = True

	def close(self):
		del GRPS_TABLE[self.CLASS_ID][self.INST_ID]
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

class ObjDraw(Obj):
	@abstractmethod
	def __init__(self, INST_ID, image, rect):
		Obj.__init__(self, INST_ID)
		self.image = image
		self.rect = rect
		self.BCKGND = pg.display.get_surface()

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

	def load(cls, INST_ID):
		with open(cls.GRP_FILE, "r") as fp:
			i = 0
			for obj in ijson.items(fp, "item"):
				if i < INST_ID:
					i += 1
				else:
					return cls(INST_ID, **obj)

			raise ValueError(
				"object with CLASS_ID={} and INST_ID={} not found".format(
					cls.CLASS_ID,
					INST_ID
				)
			)


class ObjStaticRW(ObjStaticR):
	@abstractmethod
	def __init__(self, INST_ID):
		ObjStaticR.__init__(self, INST_ID)

	@abstractmethod
	def save(self):
		pass

	def _save(self, **obj):
		with open(self.GRP_FILE, "r") as fp:
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

		with open(self.GRP_FILE, "w") as fp:
			json.dump(instList, fp)




class ObjInstNotFoundError(Exception):
	def __init__(self, class_id, inst_id):
		Exception.__init__(
			self,
			"object with CLASS_ID=%d INST_ID=%d not found"%(class_id, inst_id)
		)

class Group:
	@abstractmethod
	def __init__(self, OBJS_TYPE):
		self.OBJS_TYPE = OBJS_TYPE
		self.INSTS = []

	def add(self, obj):
		insort(self.INSTS, obj)

	def __getitem__(self, inst_id):
		for obj in self:
			if obj.INST_ID == inst_id:
				return obj
			elif obj.INST_ID > inst_id:
				break
		raise ObjInstNotFoundError(self.OBJS_TYPE.CLASS_ID, inst_id)

	def __delitem__(self, inst_id):
		i = 0
		for obj in self:
			if obj.INST_ID == inst_id:
				del self.INSTS[i]
				return
			elif obj.INST_ID > inst_id:
				break
			i += 1

		raise ObjInstNotFoundError(self.OBJS_TYPE.CLASS_ID, inst_id)

	def __iter__(self):
		return iter(self.INSTS)

	def __str__(self):
		return "<{}[{}]({})>".format(
			self.__class__.__qualname__,
			self.OBJS_TYPE.__qualname__,
			self.INSTS
		)

	def __repr__(self):
		return str(self)


class GroupsTable(tuple):
	def __new__(cls, iterable=()):
		return tuple.__new__(cls, tuple(iterable))

_cmp_class_id = cmp_to_key(
	lambda o0, o1: (
		1 if o0.OBJS_TYPE.CLASS_ID > o1.OBJS_TYPE.CLASS_ID else
		0 if o0.OBJS_TYPE.CLASS_ID == o1.OBJS_TYPE.CLASS_ID else
		-1
	)
)

class UpdatingPipeline(tuple):
	def __new__(cls, iterable=()):
		return tuple.__new__(cls, tuple(iterable))

	def update(self): 
		for group in self:
			map(group.OBJS_TYPE.update, group)

_cmp_updt_pos = cmp_to_key(
	lambda o0, o1: (
		1 if o0.OBJS_TYPE.UPDT_POS > o1.OBJS_TYPE.UPDT_POS else
		0 if o0.OBJS_TYPE.UPDT_POS == o1.OBJS_TYPE.UPDT_POS else
		-1
	)
) 

class DrawingPipeline(tuple):
	def __new__(cls, iterable=()):
		return tuple.__new__(cls, tuple(iterable))

	def draw(self): 
		for group in self:
			map(group.OBJS_TYPE.draw, group)

_cmp_draw_layer = cmp_to_key(
	lambda o0, o1: (
		1 if o0.OBJS_TYPE.DRAW_LAYER > o1.OBJS_TYPE.DRAW_LAYER else
		0 if o0.OBJS_TYPE.DRAW_LAYER == o1.OBJS_TYPE.DRAW_LAYER else
		-1
	)
)


def setGroups(*groups):
	global GRPS_TABLE
	global UPDT_PL
	global DRAW_PL

	GRPS_TABLE = tuple(sorted(groups, key=_cmp_class_id))

	updtGrps = [
		group
		for group in groups
		if issubclass(group.OBJS_TYPE, ObjUpdate)
	]
	updtGrps.sort(key=_cmp_updt_pos)

	UPDT_PL = UpdatingPipeline(updtGrps)

	drawGrps = [
		group
		for group in groups
		if issubclass(group.OBJS_TYPE, ObjDraw)
	]
	drawGrps.sort(key=_cmp_draw_layer)

	DRAW_PL = DrawingPipeline(drawGrps)

def getGroups(class_ids):
	return GRPS_TABLE[class_ids]

def update():
	UPDT_PL.update()

def draw():
	DRAW_PL.draw()

def loadR(class_id:int, inst_id:int):
	groupType = GRPS_TABLE[class_id].OBJS_TYPE
	return groupType.load(groupType, inst_id)

def loadRW(class_id:int, inst_id:int)->ObjStaticRW:
	return loadR(class_id, inst_id)
