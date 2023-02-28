import obj


class Loader(obj.ObjStaticRW):
	GRP_FILE = "game/data/loaders.json"

	def __init__(self, HASH, FATHR_HASH, objs):
		obj.ObjStaticRW.__init__(self, HASH, FATHR_HASH)
		self.objs = objs

		for inst in objs:
			obj.load(inst["type"], inst["hash"], HASH)


	def save(self):
		self._save(objs=self.objs)


	def close(self):
		for inst in self.objs:
			try:
				obj.getGroups(inst["type"])[inst["hash"]].close()

			except obj.ObjNotFoundError:
				pass

		obj.ObjStaticRW.close(self)

obj.addGroup(obj.Group(Loader))
