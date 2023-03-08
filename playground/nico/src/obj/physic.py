from obj.base import ObjDraw, ObjUpdate
import pygame as pg
from abc import abstractmethod


class ObjRelative(ObjDraw):
	"""
	Clase abstracta que implementa el metodo draw de 'ObjDraw' para dibujar
	'image' desde la perpectiva del punto 'REF_POINT'.

	Los atributos son:
	- REF_POINT, pygame.Rect que normamente sera la camara.
	- pos, pygame.math.Vector2 que sera la coordenada del objeto desde el
		origen de coordenadas.
	"""
	@abstractmethod
	def __init__(self, HASH, FATHR_HASH, image, w, h, REF_POINT, pos):
		"""
		Inicializador por defecto de los objetos relativos.
		Si se sobre-escribe, igualmente se debe inicializar la clase base con
		'ObjRelative.__init__(self, HASH, FATHR_HASH, image, w, h, REF_POINT,
		pos)' siendo 'image' la imagen deseada a dibujar, 'w' y 'h' su anchura y
		altura, 'REF_POINT' el punto de referencia o la camara, y pos el vector
		con la coordenada global de la imagen.
		"""
		ObjDraw.__init__(self, HASH, FATHR_HASH, image, pg.Rect(0,0,w,h))
		self.REF_POINT = REF_POINT
		self.pos = pos

	def draw(self):
		"""
		Metodo de dibujado que sobre-escribe el de 'ObjDraw' para relativizar la
		coordenada de la imagen 'pos' respecto al punto de referencia
		'REF_POINT', pero este metodo no dibuja nada mientras no se llame al de
		'ObjDraw.draw()', por lo que normalmente se debe sobre-escribir este
		metodo en la subclase para llamar a ambos metodos draw del las clases
		que heredan.
		"""
		self.rect.x = round(self.pos.x - self.REF_POINT.x)
		self.rect.y = round(self.pos.y - self.REF_POINT.y)

class ObjParallax(ObjDraw):
	"""
	Clase abstracta que implementa el metodo draw de 'ObjDraw' para dibujar
	'image' desde la perpectiva del punto 'REF_POINT' con paralax.

	Los atributos son:
	- REF_POINT, pygame.Rect que normamente sera la camara.
	- pos, pygame.math.Vector2 que sera la coordenada del objeto desde el
		origen de coordenadas.
	- Z_OFFSET, numero flotante entre 0 e infinito, si es 1, el objeto actuara
		como un 'ObjRelative', si es menor que 1, el objeto se movera mas lento,
		si es mayor que 1, se movera mas rapido.
	"""
	@abstractmethod
	def __init__(self, HASH, FATHR_HASH, image, w, h, REF_POINT, pos, Z_OFFSET):
		"""
		Inicializador por defecto de los objetos relativos.
		Si se sobre-escribe, igualmente se debe inicializar la clase base con
		'ObjRelative.__init__(self, HASH, FATHR_HASH, image, w, h, REF_POINT,
		pos)' siendo 'image' la imagen deseada a dibujar, 'w' y 'h' su anchura y
		altura, 'REF_POINT' el punto de referencia o la camara, pos el vector
		con la coordenada global de la imagen, y 'Z_OFFSET' el paralax.
		"""
		ObjDraw.__init__(self, HASH, FATHR_HASH, image, pg.Rect(0,0,w,h))
		self.REF_POINT = REF_POINT
		self.pos = pos
		self.Z_OFFSET = Z_OFFSET

	def draw(self):
		"""
		Metodo de dibujado que sobre-escribe el de 'ObjDraw' para relativizar la
		coordenada de la imagen 'pos' respecto al punto de referencia
		'REF_POINT', pero este metodo no dibuja nada mientras no se llame al de
		'ObjDraw.draw()', por lo que normalmente se debe sobre-escribir este
		metodo en la subclase para llamar a ambos metodos draw del las clases
		que heredan.
		"""
		self.rect.x = round(self.pos.x - self.REF_POINT.x*self.Z_OFFSET)
		self.rect.y = round(self.pos.y - self.REF_POINT.y*self.Z_OFFSET)

class ObjPhysic(ObjRelative, ObjUpdate):
	"""
	Clase abstracta que implementa 'update' para simular aceleracion y
	velocidad en la imagen 'image' que recibe.

	Los atributos son:
	- acc, pygame.math.Vector2 con la aceleracion horizontal y vertical de la
		imagen.
	- vel, pygame.math.Vector2 con la velocidad horizontal y vertical de la
		imagen.
	- cBox, pygame.Rect que representa la collide box del objeto fisico.
	"""
	@abstractmethod
	def __init__(
		self,
		HASH,
		FATHR_HASH,
		img,
		imgW,
		imgH,
		REF_POINT,
		pos,
		cBoxOffsetH,
		cBoxOffsetV,
		cBoxW,
		cBoxH,
		acc,
		vel
	):
		"""
		Inicializador por defecto de los objetos fisicos.
		Si se sobre-escribe, igualmente se debe inicializar la clase base con
		'ObjPhysic.__init__(self, HASH, FATHR_HASH, img, imgW, imgH, REF_POINT,
		pos, cBoxOffsetH, cBoxOffsetV, cBoxW, cBoxH, acc, vel)' siendo,
		'img' la imagen, 'imgW' y 'imgH' su anchura y altura, cBoxOffsetH y
		cBoxOffsetV el margen horizontal y vertical de la collide box respecto a
		'pos', 'acc' la aceleracion, 'vel' la velocidad.
		"""
		ObjRelative.__init__(
			self,
			HASH,
			FATHR_HASH,
			img,
			imgW,
			mgH,
			REF_POINT,
			pos
		)
		ObjUpdate.__init__(self, HASH, FATHR_HASH)
		self._cBoxOffsetH = cBoxOffsetH
		self._cBoxOffsetV = cBoxOffsetV
		self._cBoxW = cBoxW
		self._cBoxH = cBoxH
		self.acc = acc
		self.vel = vel

	@property
	def cBox(self):
		"""
		Se mantiene el offset con la collide box
		"""
		return pg.Rect(
			round(self.pos.x+cBoxOffsetH),
			round(self.pos.y+cBoxOffsetV),
			cBoxW,
			cBoxH
		)

	@cBox.setter
	def cBox(self, rect):
		"""
		Se mantiene el offset con la collide box
		"""
		self.pos.x = rect.x - self._cBoxOffsetH
		self.pos.y = rect.y - self._cBoxOffsetV

	def updateX(self):
		"""
		Se actualiza la posicion horizontal
		"""
		self.vel.x += self.acc.x
		self.pos.x += self.vel.x

	def updateY(self):
		"""
		Se actualiza la posicion vertical
		"""
		self.vel.y += self.acc.y
		self.pos.y += self.vel.y

	def update(self):
		"""
		Se actualizan la posicion horizontal y vertical.
		Sobre-escribir para extender la funcionalidad.
		"""
		self.updateX()
		self.updateY()
		
		