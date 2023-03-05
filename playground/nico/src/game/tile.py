import obj
from game.image import SpriteSheet
from game.cam import Cam
import pygame as pg
import csrmat

import numpy as np
import json

class TileMap(obj.ObjStaticR, obj.physic.ObjRelative, obj.sprite.ObjSprite):
	DRAW_LAYER = 0
	GRP_FILE = "game/data/tile_maps.json"
	
	def __init__(
		self,
		HASH,
		FATHR_HASH,
		camHash,
		sprtShtHash,
		rowOffset,
		colOffset,
		csrMat
		):
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)

		cam = obj.getGroup(Cam)[camHash]
		try:
			self._sprtSht = obj.getGroup(SpriteSheet)[sprtShtHash]
			self._sprtSht.watch()
		except obj.ObjNotFoundError:
			self._sprtSht = obj.load(SpriteSheet,sprtShtHash, HASH)

		self._rowOffset = rowOffset
		self._colOffset = colOffset
		self._csrMat = csrmat.CSRMat(csrMat, ())

		self._gridCamH = cam.h//self._sprtSht.clip.h
		self._gridCamW = cam.w//self._sprtSht.clip.w


		self._vBeg = self._rowOffset - self._gridCamH
		self._hBeg = self._colOffset - self._gridCamW
		self._vEnd = self._rowOffset + self._csrMat.shape[0]
		self._hEnd = self._colOffset + self._csrMat.shape[1]

		obj.physic.ObjRelative.__init__(
			self,
			HASH,
			FATHR_HASH,
			None,
			self._sprtSht.clip.w,
			self._sprtSht.clip.h,
			cam,
			pg.math.Vector2(0, 0)
		)
		obj.sprite.ObjSprite.__init__(
			self,
			HASH,
			FATHR_HASH,
			self._sprtSht,
			0,
			0
		)

	def draw(self):
		if self.REF_POINT.active:
			gridCamY, gridCamYr = divmod(self.REF_POINT.y, self.rect.h)
			ceilY = int(bool(gridCamYr))
			gridCamX, gridCamXr = divmod(self.REF_POINT.x, self.rect.w)
			ceilX = int(bool(gridCamXr))

			if (gridCamY+ceilY > self._vBeg and
				gridCamY < self._vEnd and
				gridCamX+ceilX > self._hBeg and
				gridCamX < self._hEnd
			):
				esqSup = gridCamY - self._rowOffset
				esqInf = esqSup + self._gridCamH + ceilY

				esqIzq = gridCamX - self._colOffset
				esqDer = esqIzq + self._gridCamW + ceilX

				esqSup = max(0, esqSup)
				esqInf = min(self._csrMat.shape[0], esqInf)
				esqIzq = max(0, esqIzq)
				esqDer = min(self._csrMat.shape[1], esqDer)

				for row in range(esqSup, esqInf):
					for col, tile in self._csrMat[row]:
						if col >= esqDer:
							break
						elif col >= esqIzq:
							self.pos.y = (self._rowOffset + row)*self.rect.h
							self.pos.x = (self._colOffset + col)*self.rect.w
							self.frame = obj.sprite.Frame(*tile)
							obj.physic.ObjRelative.draw(self)						
							obj.sprite.ObjSprite.draw(self)
		else:
			raise obj.ObjNotFoundError(Cam, hash(self.REF_POINT))
		

	def close(self):
		self._sprtSht.watch()
		obj.ObjStaticR.close(self)


try:
	obj.getGroup(TileMap)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(TileMap))


VOID = 0
RECT = 1

class Tile:
	def __init__(self, form, rect):
		self._form = form
		self._rect = rect

	@property
	def form(self):
		return self._form

	@property
	def rect(self):
		return self._rect

	def __str__(self):
		return "{}(form={}, rect={})".format(
			Tile.__qualname__,
			self._form,
			self._rect
		)

	def __repr__(self):
		return "<{}>".format(self)
	
	
class TileCollision(obj.ObjStaticR):
	GRP_FILE = "game/data/tile_collisions.json"

	def __init__(
		self,
		HASH,
		FATHR_HASH,
		tile_w,
		tile_h,
		rowOffset,
		colOffset,
		csrMat
	):
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
		self._tile = pg.Rect(0,0,tile_w, tile_h)
		self._rowOffset = rowOffset
		self._colOffset = colOffset
		self._csrMat = csrmat.CSRMat(csrMat, VOID)

	@property
	def tile_w(self):
		return self._tile.w
	
	@property
	def tile_h(self):
		return self._tile.h

	def __getitem__(self, *args, **kwargs):
		if args:
			if len(args) == 1:
				y,x = args[0]

			elif len(args) == 2:
				y,x = args
			else:
				raise ValueError("first x, then y")
		elif kwargs:
			if len(kwargs) == 2:
				if not "x" in kwargs:
					raise ValueError("missing x kwarg")
				if not "y" in kwargs:
					raise ValueError("missing y kwarg")

				x = kwargs["x"]
				y = kwargs["y"]
			else:
				raise ValueError("missing x and y kwarg")
		else:
			raise ValueError("missing x and y")

		y = y//self._tile.h
		x = x//self._tile.w
		yRel = y - self._rowOffset
		xRel = x - self._colOffset

		if (y >= 0 and
			y - self._rowOffset < self._csrMat.shape[0] and
			x - self._colOffset >= 0 and
			x - self._colOffset < self._csrMat.shape[1]
		):
			return Tile(
				self._csrMat[yRel, xRel],
				self._tile.move(x*self._tile.w, y*self._tile.h)
			)
		else:
			return Tile(
				VOID,
				self._tile.move(x*self._tile.w, y*self._tile.h)
			)

try:
	obj.getGroup(TileCollision)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(TileCollision))


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        else:
            return super().default(obj)

class TileEditor(obj.ObjDynamic, obj.sprite.ObjSprite, obj.ObjUpdate):
	UPDT_POS = 0
	DRAW_LAYER = 0

	def __init__(
		self,
		FATHR_HASH,
		sprtShtHash,
		room_w,
		room_h,
		outFile,
		inFile
	):
		obj.ObjDynamic.__init__(self, FATHR_HASH)

		if inFile:
			with open(inFile+"_tl_map.json", "r") as fp:
				self._tl_map = np.array(csrmat.CSRMat(json.load(fp))[:,:], dtype=object)

			with open(inFile+"_tl_col.json", "r") as fp:
				self._tl_col = np.array(csrmat.CSRMat(json.load(fp), VOID)[:,:])
		else:
			self._tl_map = np.full((room_h, room_w), None, dtype=object)
			self._tl_col = np.full((room_h, room_w), VOID, dtype=np.uint8)

		self._sprtSht = obj.getGroup(SpriteSheet)[sprtShtHash]

		self._room_w = room_w
		self._room_h = room_h

		self._col = 0
		self._row = 0

		self._flipX = False
		self._flipY = False

		self._colMode = False

		self._outFile = outFile

		obj.sprite.ObjSprite.__init__(self, hash(self), FATHR_HASH, self._sprtSht, 0, 0)
		self.frame = obj.sprite.Frame(0, 0)

	def update(self):
		x, y = pg.mouse.get_pos()

		gridX = x//self._sprtSht.clip.w
		gridY = y//self._sprtSht.clip.h

		self.rect.x = gridX*self._sprtSht.clip.w
		self.rect.y = gridY*self._sprtSht.clip.h

		for event in pg.event.get():
			if event.type == pg.QUIT:
				exit(0)

			if event.type == pg.MOUSEBUTTONDOWN:
				if event.button == pg.BUTTON_LEFT:
					if self._colMode:
						self._tl_col[gridY, gridX] = RECT
					else:
						self._tl_map[gridY, gridX] = [self._col, self._row, self._flipX, self._flipY]

				elif event.button == pg.BUTTON_RIGHT:
					if self._colMode:
						self._tl_col[gridY, gridX] = VOID
					else:
						self._tl_map[gridY, gridX] = None

			if event.type == pg.KEYDOWN:
				if event.key == pg.K_g:
					with open(self._outFile+"_tl_map.json", "w") as fp:
						json.dump(csrmat.CSRMat(self._tl_map.tolist(), None).asdict, fp, cls=NumpyArrayEncoder)

					with open(self._outFile+"_tl_col.json", "w") as fp:
						json.dump(csrmat.CSRMat(self._tl_col.tolist(), VOID).asdict, fp, cls=NumpyArrayEncoder)

					print("SAVED!")

				if event.key == pg.K_c:
					self._colMode = not self._colMode

				if event.key == pg.K_w:
					if self._row > 0:
						self._row -= 1
						self.frame = obj.sprite.Frame(self._col, self._row, self._flipX, self._flipY)

				elif event.key == pg.K_s:
					if self._row < self._sprtSht.h-1:
						self._row += 1
						self.frame = obj.sprite.Frame(self._col, self._row, self._flipX, self._flipY)

				elif event.key == pg.K_a:
					if self._col > 0:
						self._col -= 1
						self.frame = obj.sprite.Frame(self._col, self._row, self._flipX, self._flipY)

				elif event.key == pg.K_d:
					if self._col < self._sprtSht.w-1:
						self._col += 1
						self.frame = obj.sprite.Frame(self._col, self._row, self._flipX, self._flipY)

				elif event.key == pg.K_h:
					self._flipX = not self._flipX
					self.frame = obj.sprite.Frame(self._col, self._row, self._flipX, self._flipY)

				elif event.key == pg.K_v:
				    self._flipY = not self._flipY
				    self.frame = obj.sprite.Frame(self._col, self._row, self._flipX, self._flipY)
		

	def draw(self):
		prevFrame = self.frame
		prevRect = self.rect.copy()
		obj.sprite.ObjSprite.draw(self)

		for row in range(self._room_h):
			for col in range(self._room_w):
				tl = self._tl_map[row, col]
				if tl:
					self.frame = obj.sprite.Frame(*tl)
					self.rect.y = row*self._sprtSht.clip.h
					self.rect.x = col*self._sprtSht.clip.w
					obj.sprite.ObjSprite.draw(self)

		self.frame = prevFrame

		if self._colMode:
			pg.draw.rect(self._BCKGND, (255,0,0), prevRect, 1)
			
			for row in range(self._room_h):
				for col in range(self._room_w):
					tl = self._tl_col[row, col]
					if tl != VOID:
						pg.draw.rect(
							self._BCKGND,
							(255,0,0),
							pg.Rect(
								col*self._sprtSht.clip.w, row*self._sprtSht.clip.h,
								self._sprtSht.clip.w, self._sprtSht.clip.h
							),						
							1
						)

try:
	obj.getGroup(TileEditor)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(TileEditor))
