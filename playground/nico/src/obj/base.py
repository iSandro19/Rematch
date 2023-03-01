from abc import ABC, abstractmethod
from multiprocessing import Pool
from bisect import insort
import ijson
import json
import pygame as pg
from functools import cmp_to_key


class GroupNotFoundError(ValueError):
	def __init__(self, objType):
		ValueError.__init__(
			self,
			"Group with TYPE=%s not found"%objType.__qualname__
		)

class GroupsTable:
	def __init__(self):
		self._grps = {}

	def add(self, group):
		self._grps[group.TYPE.__qualname__] = group

	def __getitem__(self, objType):
		if isinstance(objType, str):
			key = objType
		elif isinstance(objType, type):
			key = objType.__qualname__
		else:
			raise ValueError("only 'type' and 'str' are valid keys")

		try:
			return self._grps[key]
		except KeyError:
			raise GroupNotFoundError(objType)

	def __str__(self):
		return "{}({})".format(
			type(self).__qualname__,
			self._grps
		)

	def __repr__(self):
		return "<"+str(self)+">"


class UpdatingPipeline:
	def __init__(self):
		self._grps = []

	def add(self, group):
		self._grps.insert(group.TYPE.UPDT_POS, group)

	def update(self): 
		for group in self._grps:
			for obj in group:
				obj.update()

	def __str__(self):
		return "{}({})".format(
			type(self).__qualname__,
			self._grps
		)

	def __repr__(self):
		return "<"+str(self)+">"


class DrawingPipeline:
	def __init__(self):
		self._grps = []

	def add(self, group):
		self._grps.insert(group.TYPE.DRAW_LAYER, group)

	def draw(self): 
		for group in self._grps:
			for obj in group:
				obj.draw()

	def __str__(self):
		return "{}({})".format(
			type(self).__qualname__,
			self._grps
		)

	def __repr__(self):
		return "<"+str(self)+">"


class SavingGroups:
	def __init__(self):
		self._grps = []

	def add(self, group):
		self._grps.append(group)

	def save(self): 
		for group in self._grps:
			for obj in group:
				obj.save()

	def __str__(self):
		return "{}({})".format(
			type(self).__qualname__,
			self._grps
		)

	def __repr__(self):
		return "<"+str(self)+">"



class ObjNotFoundError(ValueError):
	def __init__(self, objType, objHash):
		ValueError.__init__(
			self,
			"Obj with type={} hash={} not found".format(objType, objHash)
		)

class Obj(ABC):
	GRPS_TABLE = GroupsTable()

	@abstractmethod
	def __init__(self, HASH, FATHR_HASH):
		self._HASH = HASH
		self._FATHR_HASH = FATHR_HASH
		self.GRPS_TABLE[type(self)].add(self)
		self.active = True

	@property
	def TYPE(self):
		return self.__class__

	@property
	def HASH(self):
		return self._HASH

	@property
	def FATHR_HASH(self):
		return self._FATHR_HASH
	
	def close(self):
		del self.GRPS_TABLE[type(self)][self._HASH]
		self.active = False

	def __eq__(self, value):
		return self._HASH == value._HASH

	def __ge__(self, value):
		return self._HASH >= value._HASH

	def __gt__(self, value):
		return self._HASH > value._HASH

	def __le__(self, value):
		return self._HASH <= value._HASH

	def __lt__(self, value):
		return self._HASH < value._HASH

	def __hash__(self):
		return self._HASH

class ObjUpdate(Obj):
	UPDT_PL = UpdatingPipeline()

	@classmethod
	def setUPDT_POS(cls, DRAW_LAYER):
		cls.DRAW_LAYER = DRAW_LAYER

	@abstractmethod
	def __init__(self, HASH, FATHR_HASH):
		Obj.__init__(self, HASH, FATHR_HASH)

	@abstractmethod
	def update(self):
		pass

class ObjDraw(Obj):
	DRAW_PL = DrawingPipeline()

	@classmethod
	def setDRAW_LAYER(cls, DRAW_LAYER):
		cls.DRAW_LAYER = DRAW_LAYER

	@abstractmethod
	def __init__(self, HASH, FATHR_HASH, image, rect):
		Obj.__init__(self, HASH, FATHR_HASH)
		self.image = image
		self.rect = rect
		self._BCKGND = pg.display.get_surface()

	def draw(self):
		self._BCKGND.blit(self.image, self.rect)

class ObjDynamic(Obj):
	@abstractmethod
	def __init__(self, FATHR_HASH):
		Obj.__init__(self, object.__hash__(self), FATHR_HASH)

class ObjStaticR(Obj):
	@abstractmethod
	def __init__(self, HASH, FATHR_HASH):
		Obj.__init__(self, HASH, FATHR_HASH)

	@classmethod
	def load(cls, HASH, FATHR_HASH):
		with open(cls.GRP_FILE, "r") as fp:
			i = 0
			for obj in ijson.items(fp, "item"):
				if i < HASH:
					i += 1
				else:
					return cls(HASH, FATHR_HASH, **obj)

			raise ObjNotFoundError(self.TYPE, HASH)


class ObjStaticRW(ObjStaticR):
	SAVE_GRPS = SavingGroups()

	@abstractmethod
	def __init__(self, HASH, FATHR_HASH):
		ObjStaticR.__init__(self, HASH, FATHR_HASH)

	@abstractmethod
	def save(self):
		pass

	def _save(self, **obj):
		with open(self.GRP_FILE, "r") as fp:
			instList = json.load(fp)

		if self.HASH < len(instList):
			instList[self.HASH] = obj
		else:
			raise ObjNotFoundError(self.TYPE, self.HASH)

		with open(self.GRP_FILE, "w") as fp:
			json.dump(instList, fp)


class Group:
	@abstractmethod
	def __init__(self, TYPE):
		self._OBJS = []
		self._TYPE = TYPE

	@property
	def TYPE(self):
		return self._TYPE
	
	def add(self, obj):
		if not obj in self._OBJS:
			insort(self._OBJS, obj)


	def __getitem__(self, objHash):
		if isinstance(objHash, int):
			for obj in self._OBJS:
				if obj.HASH == objHash:
					return obj
				elif obj.HASH > objHash:
					break
			raise ObjNotFoundError(self._TYPE, objHash)

		elif isinstance(objHash, slice):
			subGroup = Group(self._TYPE)
			i = 0

			for obj in self._OBJS:
				if obj.HASH >= objHash.start and not i%objHash.step:
					subGroup._OBJS.append(obj)
				elif obj.HASH == objHash.stop:
					break
				i += 1
			return subGroup

		else:
			raise TypeError(
				"%s indices must be integers or slices, \
				not str"%self.__class__.__qualname__
			)

	def __delitem__(self, objHash):
		if isinstance(objHash, int):
			i = 0
			for obj in self._OBJS:
				if obj.HASH == objHash:
					del self._OBJS[i]
					return
				elif obj.HASH > objHash:
					break
				i += 1

			raise ObjNotFoundError(self._TYPE, objHash)

		elif isinstance(objHash, slice):
			i = 0

			for obj in self:
				if obj.HASH >= objHash.start and not i%objHash.step:
					del self._OBJS[i]
				elif obj.HASH == objHash.stop:
					break
				i += 1
		else:
			raise TypeError(
				"%s indices must be integers or slices, \
				not str"%self.__class__.__qualname__
			)

		raise ObjNotFoundError(self._TYPE, objHash)

	def __iter__(self):
		return iter(self._OBJS)

	def __str__(self):
		return "{}({}, TYPE={})".format(
			type(self).__qualname__,
			self._OBJS,
			self._TYPE.__qualname__
		)

	def __repr__(self):
		return "<"+str(self)+">"



def addGroup(group):	
	Obj.GRPS_TABLE.add(group)
	if issubclass(group.TYPE, ObjUpdate):
		ObjUpdate.UPDT_PL.add(group)
	if issubclass(group.TYPE, ObjDraw):
		ObjDraw.DRAW_PL.add(group)
	if issubclass(group.TYPE, ObjStaticRW):
		ObjStaticRW.SAVE_GRPS.add(group)

def getGroup(objType):
	return Obj.GRPS_TABLE[objType]

def update():
	ObjUpdate.UPDT_PL.update()

def draw():
	ObjDraw.DRAW_PL.draw()

def load(objType, objHash, fathrHash):
	return Obj.GRPS_TABLE[objType].TYPE.load(objHash, fathrHash)

def save():
	ObjStaticRW.SAVE_GRPS.save()
