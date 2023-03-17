import obj
import pygame as pg


class Control(obj.ObjStaticRW, dict):
	GRP_FILE = "game/data/controls.json"

	def __init__(self, HASH, FATHR_HASH, keys):
		obj.ObjStaticRW.__init__(self, HASH, FATHR_HASH)
		dict.__init__(self, keys)

	def save(self):
		obj._save(keys=self)

try:
	obj.getGroup(Control)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(Control))
