from obj.base import ObjDraw, ObjUpdate
import pygame as pg
from pygame.locals import *
from abc import abstractmethod


class SpriteSheet:
	"""
	Clase que representa un sprite sheet para poder acceder a sus sprites.

	Sus atributos son:
	- SHEET, pygame.Surface con el sprite sheet.
	- clip, pygame.Rect con la posicion y tamano del sprite.
	- w, numero de columnas que contiene el sprite sheet.
	- h, numero de filas que contiene el sprite sheet.
	"""
	def __init__(self, SHEET, w, h, colorkey=None):
		"""
		Sus argumentos son:
		-SHEET, pygame.Surface con el sprite sheet.
		- w, numero de columnas que contiene el sprite sheet.
		- h, numero de filas que contiene el sprite sheet.
		- colorkey, pygame.Color del fondo para hacerlo trasparente.
		"""
		self.SHEET = SHEET
		self.SHEET.set_colorkey(colorkey)
		self.clip = pg.Rect(0, 0, w, h)
		self._w = SHEET.get_width()//self.clip.w
		self._h = SHEET.get_height()//self.clip.w

	@property
	def w(self):
		return self._w

	@property
	def h(self):
		return self._h

	def __getitem__(self, rowXcol)->pg.Surface:
		"""
		Metodo para acceder al sprite del sprite sheet en la fila y columna
		entregados.
		"""
		self.clip.x = rowXcol[1]*self.clip.w
		self.clip.y = rowXcol[0]*self.clip.h

		return self.SHEET.subsurface(self.clip)


class Frame:
	"""
	Clase inmutable que representa un frame, un sprite o incluso un tile.

	Los atributos son:
	- COL, numero de la columna donde se encuentra el sprite.
	- ROW, numero de la fila donde se encuentra el sprite.
	- FLIP_X, flag para reflejar el sprite horizontalmente.
	- FLIP_Y, flag para reflejar el sprite verticalmente.
	- DUR, numero flotante con los fotogramas que dura la animacion.
	"""
	def __init__(
		self,
		COL,
		ROW, 
		FLIP_X = False,
		FLIP_Y = False,
		DUR = 0.
	):
		"""
		Los argumentos son:
		- COL, numero de la columna donde se encuentra el sprite.
		- ROW, numero de la fila donde se encuentra el sprite.
		- FLIP_X, flag para reflejar el sprite horizontalmente.
		- FLIP_Y, flag para reflejar el sprite verticalmente.
		- DUR, numero flotante con los fotogramas que dura la animacion.
		"""
		self.COL = COL
		self.ROW = ROW
		self.DUR = DUR
		self.FLIP_X = FLIP_X
		self.FLIP_Y = FLIP_Y

class ObjSprite(ObjDraw):
	"""
	Clase abstracta que representa los objetos dibujables a partir de un
	sprite sheet.

	Los atributos son:
	- SPRTS, SpriteSheet a usar para extraer los sprites.
	- frame, Frame a dibujar.
	"""
	@abstractmethod
	def __init__(self, HASH, FATHR_HASH, SPRTS, x, y):
		"""
		Inicilizador por defecto que se debe redefinir en una subclase para
		poder instanciarla. A mayores, es necesario llamar a
		ObjSprite.__init__(self, HASH, FATHR_HASH, SPRTS, x, y), siendo
		'SPRTS' el sprite sheet a usar para extraer los sprites, 'x' e 'y' las
		coordenadas en la ventana de la imagen.
		"""
		self.SPRTS = SPRTS
		self._frame = None

		ObjDraw.__init__(
			self,
			HASH,
			FATHR_HASH,
			None,
			pg.Rect(x, y, SPRTS.clip.w, SPRTS.clip.h)
		)

	@property
	def frame(self):
		return self._frame
	
	@frame.setter
	def frame(self, frame):
		self._frame = frame

		self.image = self.SPRTS[frame.ROW, frame.COL]

		if frame.FLIP_X or frame.FLIP_Y:
			self.image = pg.transform.flip(
				self.image,
				frame.FLIP_X,
				frame.FLIP_Y
			)


class Animation(tuple):
	"""
	Clase inmutable que representa una secuencia de frames o animacion.

	Los atributos son:
	- FRAMES, tupla con la secuencia de Frame.
	- LOOP, flag para reiniciar la animacion una vez completada. Si esta
		desactivado, cuando la animacion termine se mantendra en el ultimo
		Frame.
	"""
	def __new__(
		cls,
		FRAMES,
		LOOP=True
	):
		return tuple.__new__(cls, tuple(FRAMES))

	def __init__(
		self,
		FRAMES,
		LOOP=True
	):
		self.LOOP = LOOP

class ObjAnim(ObjDraw):
	"""
	Clase abstracta que representa a los objetos dibujables animados que usan
	un SpriteSheet.

	Los atributos son:
	- SPRTS, SpriteSheet a usar para extraer los sprites de la animacion.
	- anim, Animation a mostrar.
	- speed, flotante que representa el porcentaje de velocidad de la animacion.
	- done, flag que se activa cuando se a completado la animacion.
	"""
	speed = 1.
	done = False

	@abstractmethod
	def __init__(self, HASH, FATHR_HASH, SPRTS, x, y):
		"""
		Inicilizador por defecto que se debe redefinir en una subclase para
		poder instanciarla. A mayores, es necesario llamar a
		ObjAnim.__init__(self, HASH, FATHR_HASH, SPRTS, x, y) siendo,
		'SPRTS', el SpriteSheet a usar para extraer los sprites de la animacion,
		y 'x' e 'y' la coordenada en la ventana de la animacion.
		"""
		self.SPRTS = SPRTS
		self._anim = None

		ObjDraw.__init__(
			self,
			HASH,
			FATHR_HASH,
			None,
			pg.Rect(x, y, SPRTS.clip.w, SPRTS.clip.h)
		)

	@property
	def anim(self):
		return self._anim
	
	@anim.setter
	def anim(self, anim):
		self._anim = anim
		self._frameIt = iter(anim)
		self._steps = 0.
		self._frame = next(self._frameIt)
		self.done = False

	def draw(self):
		"""
		Metodo sobre-escrito de 'ObjDraw' para dibujar la animacion escogida.
		Este metodo en si no dibuja nada, se tiene que llamar luego a
		'ObjDraw.draw(self)' para ello.
		"""
		if not self.done:
			try:
				if self._steps < self._frame.DUR:
					self._steps += self.speed
				else:
					self._steps = 0.
					self._frame = next(self._frameIt)		
			except StopIteration:
				if self._anim.LOOP:
					self._frameIt = iter(self._anim)
					self._steps = 0.
					self._frame = next(self._frameIt)
				else:
					self.done = True

			self.image = self.SPRTS[self._frame.ROW, self._frame.COL]

			if self._frame.FLIP_X or self._frame.FLIP_Y:
				self.image = pg.transform.flip(
					self.image,
					self._frame.FLIP_X,
					self._frame.FLIP_Y
				)

