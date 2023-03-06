from abc import ABC, abstractmethod
from multiprocessing import Pool
from bisect import insort
import ijson
import json
import pygame as pg
from functools import cmp_to_key


class GroupNotFoundError(ValueError):
	"""
	Excepcion usada para detectar cuando no se existe un grupo de un tipo de objetos
	"""
	def __init__(self, objType):
		"""
		objType: clase del objeto solicitado
		"""
		ValueError.__init__(
			self,
			"Group with TYPE=%s not found"%objType.__qualname__
		)

class GroupsTable:
	"""
	Tabla que contiene todos los grupos de objetos como un diccionario
	"""
	def __init__(self):
		"""
		El diccionario de grupos comienza vacio
		"""
		self._grps = {}

	def add(self, group):
		"""
		Se anade el grupo 'group' al diccionario de grupos
		"""
		self._grps[group.TYPE.__qualname__] = group

	def close(self):
		"""
		Se cierran todo los objetos de todos los grupos del diccionario
		"""
		for group in self._grps.values():
			for obj in group:
				obj.close()

	def __getitem__(self, objType):
		"""
		Se obtiene el grupo con objetos de tipo 'objType' si existe,
		si no, se lanza la excepcion GroupNotFoundError
		"""
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
		"""
		Representacion de la tabla con un string
		"""
		return "{}({})".format(
			type(self).__qualname__,
			self._grps
		)

	def __repr__(self):
		"""
		Representacion de la tabla con un string en el interprete interacctivo
		"""
		return "<"+str(self)+">"


class UpdatingPipeline:
	"""
	Lista ordenada de los grupos a actualizarse derivados de 'ObjUpdate'
	"""
	def __init__(self):
		"""
		La lista de grupos comienza vacia
		"""
		self._grps = []

	def add(self, group):
		"""
		Se anade el grupo 'group' a la lista en la posicion determinada por el atributo
		'UPDT_POS' definido en la clase de los objetos que contiene el grupo
		"""
		self._grps.insert(group.TYPE.UPDT_POS, group)

	def update(self): 
		"""
		Los objetos de un mismo grupo se actualizan antes que los de otro
		si su atributo 'UPDT_POS' es inferior
		"""
		for group in self._grps:
			for obj in group:
				if obj._active:
					obj.update()

	def __str__(self):
		"""
		Representacion de la lista con un string
		"""
		return "{}({})".format(
			type(self).__qualname__,
			self._grps
		)

	def __repr__(self):
		"""
		Representacion de la lista con un string en el interprete interacctivo
		"""
		return "<"+str(self)+">"


class DrawingPipeline:
	"""
	Lista ordenada de los grupos a dibujarse derivados de 'ObjDraw'
	"""
	def __init__(self):
		"""
		La lista de grupos comienza vacia
		"""
		self._grps = []

	def add(self, group):
		"""
		Se anade el grupo 'group' a la lista en la posicion determinada por el atributo
		'DRAW_LAYER' definido en la clase de los objetos que contiene el grupo
		"""
		self._grps.insert(group.TYPE.DRAW_LAYER, group)

	def draw(self): 
		"""
		Los objetos de un mismo grupo se dibujan en una capa mas proxima a la
		camara que otros si su atributo 'DRAW_LAYER' es inferior
		"""
		for group in self._grps:
			for obj in group:
				if obj._active:
					obj.draw()

	def __str__(self):
		"""
		Representacion de la lista con un string
		"""
		return "{}({})".format(
			type(self).__qualname__,
			self._grps
		)

	def __repr__(self):
		"""
		Representacion de la lista con un string en el interprete interacctivo
		"""
		return "<"+str(self)+">"


class SavingGroups:
	"""
	Lista de los grupos a guardarse derivados de 'ObjStaticRW'
	"""
	def __init__(self):
		"""
		La lista de grupos comienza vacia
		"""
		self._grps = []

	def add(self, group):
		"""
		Se anade el grupo 'group' a la lista
		"""
		self._grps.append(group)

	def save(self):
		"""
		Se guardan todos los objetos de cada grupo
		"""
		for group in self._grps:
			for obj in group:
				obj.save()

	def __str__(self):
		"""
		Representacion de la lista con un string
		"""
		return "{}({})".format(
			type(self).__qualname__,
			self._grps
		)

	def __repr__(self):
		"""
		Representacion de la lista con un string en el interprete interacctivo
		"""
		return "<"+str(self)+">"



class ObjNotFoundError(ValueError):
	"""
	Excepcion usada para detectar cuando no se existe un grupo de un tipo de objetos
	"""
	def __init__(self, objType, objHash):
		"""
		objType: clase del objeto solicitado
		objHash: hash del objeto solicitado
		"""
		ValueError.__init__(
			self,
			"Obj with type={} hash={} not found".format(objType, objHash)
		)

class Obj(ABC):
	"""
	Clase abstracta base para derivar en objetos mas especializados
	Concentra la informacion y comportamientos comunes a todos los objetos del juego

	Los atributos son:
	- GRPS_TABLE, atributo estatico final que comparten todos los objetos y contiene
		la tabla con todos los grupos de objetos, para que estos puedan acceder a los
		grupos de otros objetos

	- TYPE, atributo final que mantine el tipo del objeto. Su valor es siempre el mismo que
		usando la funcion built-in 'type'

	- HASH, atributo final unico para cada instancia usado para identificarla.
		tambien se puede usar la funcion built-in 'hash' para obtenerlo

	- FATHR_HASH, atributo final usado para guardar la instancia que ha creado el 
		objeto.

	- active, atributo booleano que indica cuando el objeto esta activo, es decir,
		que se puede acceder a su informacion, que se actualiza, y que se dibuja.
		Poner el atributo a False hara que no ocurra todo lo anterior y que se encuentre pausado,
		pudiendo reanudarlo poniendolo a True
	"""
	GRPS_TABLE = GroupsTable()

	@abstractmethod
	def __init__(self, HASH, FATHR_HASH):
		"""
		Inicilizador por defecto que se debe redefinir en una subclase para poder
		instanciarla. A mayores, es necesario llamar a Obj.__init__(self, HASH, FATHR_HASH)
		desde el metodo redefinido para poder darle un hash y fathr_hash, anadir la
		instancia al grupo de ese tipo de objetos y activarla
		"""
		self._HASH = HASH
		self._FATHR_HASH = FATHR_HASH
		self.GRPS_TABLE[type(self)].add(self)
		self._active = True

	@property
	def TYPE(self):
		return self.__class__

	@property
	def HASH(self):
		return self._HASH

	@property
	def FATHR_HASH(self):
		return self._FATHR_HASH

	@property
	def active(self):
		self._active = True

	@active.setter
	def active(self, value):
		self._active = value
	
	def close(self):
		"""
		Finalizador por defecto que sera llamado por el mismo objeto o desde otro para
		eliminarlo del grupo al que pertenece, y a mayores desactivarlo por si algun objeto tiene
		guardada una referencia a este y pueda saber que no existe
		"""
		del self.GRPS_TABLE[type(self)][self._HASH]
		self._active = False

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

def close():
	Obj.GRPS_TABLE.close()
