from abc import ABC, abstractmethod
from multiprocessing import Pool
from bisect import insort
import ijson
import json
import pygame as pg
from functools import cmp_to_key


class GroupNotFoundError(ValueError):
	"""
	Excepcion usada para detectar cuando no se existe un grupo de un tipo de
	objetos
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
		si no, se lanza la excepcion GroupNotFoundError.
		'objType' puede ser un string con el nombre de la clase o la propia
		clase
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
		Se anade el grupo 'group' a la lista en la posicion determinada por el
		atributo 'UPDT_POS' definido en la clase de los objetos que contiene el
		grupo
		"""
		i = 0
		for grp in self._grps:
			if grp.TYPE.UPDT_POS > group.TYPE.UPDT_POS:
				break
			i += 1
		
		self._grps.insert(i, group)

	def update(self): 
		"""
		Los objetos de un mismo grupo se actualizan antes que los de otro
		si su atributo 'UPDT_POS' es inferior.
		Solo se actualizan los objetos activos.
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
		Se anade el grupo 'group' a la lista en la posicion determinada por el
		atributo 'DRAW_LAYER' definido en la clase de los objetos que contiene
		el grupo
		"""
		i = 0
		for grp in self._grps:
			if grp.TYPE.DRAW_LAYER > group.TYPE.DRAW_LAYER:
				break
			i += 1

		self._grps.insert(i, group)

	def draw(self): 
		"""
		Los objetos de un mismo grupo se dibujan en una capa mas proxima a la
		camara que otros si su atributo 'DRAW_LAYER' es inferior.
		Solo se dibujan los objetos activos.
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
	Excepcion usada para detectar cuando no se existe un grupo de un tipo de
	objetos
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
	Concentra la informacion y comportamientos comunes a todos los objetos del
	juego

	Los atributos son:
	- GRPS_TABLE, atributo estatico final de la clase base que comparten todos
		los objetos y contiene la tabla con todos los grupos de objetos, para
		que estos puedan acceder a los grupos de otros objetos

	- TYPE, atributo final que mantine el tipo del objeto. Su valor es siempre
		el mismo que usando la funcion built-in 'type'

	- HASH, atributo final unico para cada instancia usado para identificarla.
		tambien se puede usar la funcion built-in 'hash' para obtenerlo

	- FATHR_HASH, atributo final usado para guardar la instancia que ha creado
		el objeto.

	- active, atributo booleano que indica cuando el objeto esta activo, es
		decir, que se puede acceder a su informacion, que se actualiza, y que
		se dibuja. Poner el atributo a False hara que no ocurra todo lo
		anterior y que se encuentre pausado, pudiendo reanudarlo poniendolo a
		True
	"""
	GRPS_TABLE = GroupsTable()

	@abstractmethod
	def __init__(self, HASH, FATHR_HASH):
		"""
		Inicilizador por defecto que se debe redefinir en una subclase para
		poder instanciarla. A mayores, es necesario llamar a
		Obj.__init__(self, HASH, FATHR_HASH) desde el metodo redefinido para
		poder darle un hash y fathr_hash, anadir la instancia al grupo de ese
		tipo de objetos y activarla
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
		return self._active

	@active.setter
	def active(self, value):
		self._active = value
	
	def close(self):
		"""
		Finalizador por defecto que sera llamado por el mismo objeto o desde
		otro para eliminarlo del grupo al que pertenece, y a mayores
		desactivarlo por si algun objeto tiene guardada una referencia a este y
		pueda saber que no existe
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
	"""
	Clase abstracta para que los objetos actualizables la deriven y
	definan como se actualiza con el metodo 'update'.

	Los atributos son:
	- UPDT_PL, atributo estatico final de la clase base que concentra todos los
		grupos de objetos actualizables. Sirve para actualizar todos los
		objetos con un foreach en 'obj.update()'.
	- UPDT_POS, atributo estatico final de la clase derivada que determina la
		preferencia para actualizarse antes que otros. Todas las instancias de
		la misma clase y del mismo grupo tienen la misma preferencia. 
	"""
	UPDT_PL = UpdatingPipeline()

	@classmethod
	def setUPDT_POS(cls, UPDT_POS):
		"""
		Setter del atributo de preferencia 'UPDT_POS'.
		Cuanto menor sea su valor, antes se actualizan los objetos de ese tipo.
		Tambien se puede inicializar en el cuerpo de la clase.
		"""
		cls.UPDT_POS = UPDT_POS

	@abstractmethod
	def __init__(self, HASH, FATHR_HASH):
		"""
		Inicializador por defecto de los objetos actualizables.
		Si se sobre-escribe, igualmente se debe inicializar la clase base con
		'ObjUpdate.__init__(self, HASH, FATHR_HASH)'.
		"""
		Obj.__init__(self, HASH, FATHR_HASH)

	@abstractmethod
	def update(self):
		"""
		Metodo actualizador del objeto, sera llamado en cada frame por la
		funcion 'obj.update()' segun el orden determinado por 'UPDT_POS'.
		Solo se actualiza si esta activo.
		"""
		pass

class ObjDraw(Obj):
	"""
	Clase abstracta para que los objetos dibujables la deriven y
	definan como se dibuja con el metodo 'draw'.

	Los atributos son:
	- DRAW_PL, atributo estatico final de la clase base que concentra todos los
		grupos de objetos dibujables. Sirve para dibujar todos los
		objetos con un foreach en 'obj.draw()'.
	- DRAW_LAYER, atributo estatico final de la clase derivada que determina la
		preferencia para dibujarse antes que otros, o la capa en la que se
		situa. Todas las instancias de la misma clase y del mismo grupo tienen
		la misma preferencia. 
	- image, atributo que contiene la pygame.Surface a mostrar por el objeto.
	- rect, atributo que contiene el pygame.Rect que determina la ubicacion de
		de 'image' en la pantalla.
	"""
	DRAW_PL = DrawingPipeline()

	@classmethod
	def setDRAW_LAYER(cls, DRAW_LAYER):
		"""
		Setter del atributo de preferencia 'DRAW_LAYER'.
		Cuanto menor sea su valor, antes se dibujaran los objetos de ese tipo.
		Tambien se puede inicializar en el cuerpo de la clase.
		"""
		cls.DRAW_LAYER = DRAW_LAYER

	@abstractmethod
	def __init__(self, HASH, FATHR_HASH, image, rect):
		"""
		Inicializador por defecto de los objetos actualizables.
		Si se sobre-escribe, igualmente se debe inicializar la clase base con
		'ObjDraw.__init__(self, HASH, FATHR_HASH, image, rect)'.
		"""
		Obj.__init__(self, HASH, FATHR_HASH)
		self.image = image
		self.rect = rect
		self._BCKGND = pg.display.get_surface()

	def draw(self):
		"""
		Metodo dibujador del objeto, sera llamado en cada frame por la
		funcion 'obj.draw()' segun el orden determinado por 'DRAW_LAYER'.
		Puede ser sobre-escrito para extender su funcionabilidad y seguir
		usandolo con 'ObjDraw.draw(self)'.
		Solo se dibuja si esta activo.
		"""
		self._BCKGND.blit(self.image, self.rect)

class ObjDynamic(Obj):
	"""
	Clase abstracta para que los objetos creados en tiempo de ejecucion la
	deriven.
	"""
	@abstractmethod
	def __init__(self, FATHR_HASH):
		"""
		Inicializador por defecto de los objetos dinamicamente creados.
		Por lo que no sera necesario asignarle un hash unico, se usa la
		direccion de memoria como identificador.
		Si se sobre-escribe, igualmente se debe inicializar la clase base con
		'ObjDynamic.__init__(self, FATHR_HASH)'.
		"""
		Obj.__init__(self, object.__hash__(self), FATHR_HASH)

class ObjStaticR(Obj):
	"""
	Clase abstracta para que los objetos cargables de disco la deriven.

	Los atributos son:
	- GRP_FILE, atributo estatico final de la clase derivada que contiene la 
		direccion del fichero json que contiene una lista con todas
		las instancias de la clase derivada ordenadas por su hash.
		Se usa para cargar las instancias con el metodo estatico de la clase
		derivada 'load'.
	"""
	@classmethod
	def setGRP_FILE(cls, GRP_FILE):
		"""
		Setter del atributo 'GRP_FILE'.
		Tambien se puede inicializar en el cuerpo de la clase.
		"""
		self.GRP_FILE = GRP_FILE

	@abstractmethod
	def __init__(self, HASH, FATHR_HASH):
		"""
		Inicializador por defecto de los objetos cargables de disco.
		Si se sobre-escribe, igualmente se debe inicializar la clase base con
		'ObjStaticR.__init__(self, HASH, FATHR_HASH)'.
		"""
		Obj.__init__(self, HASH, FATHR_HASH)

	@classmethod
	def load(cls, HASH, FATHR_HASH):
		"""
		Metodo estatico de la clase derivada que crea e inicializa una nueva
		instancia con los argumentos guardados en el json 'GRP_FILE'. 
		"""
		with open(cls.GRP_FILE, "r") as fp:
			i = 0
			for obj in ijson.items(fp, "item"):
				if i < HASH:
					i += 1
				else:
					return cls(HASH, FATHR_HASH, **obj)

			raise ObjNotFoundError(cls, HASH)


class ObjStaticRW(ObjStaticR):
	"""
	Clase abstracta para que los objetos cargables y guardables en disco la
	deriven.

	Los atributos son:
	- SAVE_GRPS, atributo estatico final de la clase base que concentra todos
		los grupos de objetos guardables. Sirve para guardar todos los
		objetos con un foreach en 'obj.save()'.
	"""
	SAVE_GRPS = SavingGroups()

	@abstractmethod
	def __init__(self, HASH, FATHR_HASH):
		"""
		Inicializador por defecto de los objetos cargables y guardables en
		disco.
		Si se sobre-escribe, igualmente se debe inicializar la clase base con
		'ObjStaticRW.__init__(self, HASH, FATHR_HASH)'.
		"""
		ObjStaticR.__init__(self, HASH, FATHR_HASH)

	@abstractmethod
	def save(self):
		"""
		Metodo abstracto que se llamara cuando un objeto quiera guardar a otro
		o al llamar a la funcion del modulo 'obj.save'.
		Normalmente, en la definicion de la clase derivada, se llamara al
		metodo privado self._save() entregandole como parametro al metodo los
		atributos a guardar en el json, p.e. self._save(x=self.x, y=self.y).
		"""
		pass

	def _save(self, **obj):
		"""
		Metodo privado para guardar los atributos del propio objeto en el json
		especificado en 'GRP_FILE'.
		"""
		with open(self.GRP_FILE, "r") as fp:
			instList = json.load(fp)

		if self.HASH < len(instList):
			instList[self.HASH] = obj
		else:
			raise ObjNotFoundError(self.TYPE, self.HASH)

		with open(self.GRP_FILE, "w") as fp:
			json.dump(instList, fp)


class Group:
	"""
	Contenedor de instancias de la misma clase.

	Los atributos son:
	- TYPE, atributo final que contiene la clase de las instancias que contiene.
	"""
	@abstractmethod
	def __init__(self, TYPE):
		"""
		El contenedor comienza vacio.
		"""
		self._OBJS = []
		self._TYPE = TYPE

	@property
	def TYPE(self):
		return self._TYPE
	
	def add(self, obj):
		"""
		Se anade el objeto 'obj' al contenedor.
		"""
		if not obj in self._OBJS:
			insort(self._OBJS, obj)


	def __getitem__(self, objHash):
		"""
		Se obtiene el objeto con hash 'objHash' del contenedor si existe,
		si no, se lanza la excepcion ObjNotFoundError.
		Se puede obtener un subgrupo de instancias con group[n:n].
		"""
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
		"""
		Se elimina el objeto con hash 'objHash' del contenedor si existe,
		si no, se lanza la excepcion ObjNotFoundError.
		Se puede eliminar un subgrupo de instancias con group[n:n].
		"""
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
	"""
	Se anade el grupo a la tabla de objetos, si es un objeto actualizable,
	tambien al pipeline de objetos actualizables, si es dibujable,
	tambien al pipeline de objetos dibujables, y si es guardable,
	tambien a la lista de objetos guradables.
	"""
	Obj.GRPS_TABLE.add(group)
	if issubclass(group.TYPE, ObjUpdate):
		ObjUpdate.UPDT_PL.add(group)
	if issubclass(group.TYPE, ObjDraw):
		ObjDraw.DRAW_PL.add(group)
	if issubclass(group.TYPE, ObjStaticRW):
		ObjStaticRW.SAVE_GRPS.add(group)

def getGroup(objType):
	"""
	Se obtiene el grupo con objetos de tipo 'objType' si existe,
	si no, se lanza la excepcion GroupNotFoundError.
	'objType' puede ser un string con el nombre de la clase o la propia
	clase
	"""
	return Obj.GRPS_TABLE[objType]

def update():
	"""
	Se actualizan todos los objetos actualizables.
	"""
	ObjUpdate.UPDT_PL.update()

def draw():
	"""
	Se dibujan todos los objetos dibujables.
	"""
	ObjDraw.DRAW_PL.draw()

def load(objType, objHash, fathrHash):
	"""
	Se carga el objeto de la clase 'objType' con hash 'objHash' y se le entrega
	el hash del objeto creador.
	"""
	return Obj.GRPS_TABLE[objType].TYPE.load(objHash, fathrHash)

def save():
	"""
	Se guardan todos los objetos guardables.
	"""
	ObjStaticRW.SAVE_GRPS.save()

def close():
	"""
	Se cierran todos los objetos.
	"""
	Obj.GRPS_TABLE.close()
