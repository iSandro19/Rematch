import obj
from game.image import SpriteSheet
from game.tile import TileMap, TileCollision, VOID, RECT
import csrmat
import pygame as pg
import numpy as np
import json


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
