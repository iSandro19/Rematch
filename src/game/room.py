import obj
from game.cam import Cam
from game.loader import Loader


def _pauseObjs(room, rooms):
	if room in rooms:
		rooms = rooms.copy()
		rooms.remove(room)

	for o in room["objs"]:
		single = True

		for r in rooms:
			if o in r["objs"]:
				single = False
				break
	
		if single:
			try:
				obj.getGroup(o["type"])[o["hash"]].active = False
			except obj.ObjNotFoundError:
				pass

def _resumeObjs(objs):
	for objIDs in objs:
		try:
			obj.getGroup(objIDs["type"])[objIDs["hash"]].active = True
		except obj.ObjNotFoundError:
			pass

def _saveObjs(objs):
	for objIDs in objs:
		grp = obj.getGroup(objIDs["type"])

		if issubclass(grp.TYPE, obj.ObjStaticRW):
			try:
				grp[objIDs["hash"]].save()
			except obj.ObjNotFoundError:
				pass

def _closeObjs(room, rooms):
	if room in rooms:
		rooms = rooms.copy()
		rooms.remove(room)

	for o in room["objs"]:
		single = True

		for r in rooms:
			if o in r["objs"]:
				single = False
				break
	
		if single:
			try:	
				obj.getGroup(o["type"])[o["hash"]].close()
			except obj.ObjNotFoundError:
				pass

def _loadObjs(objs, FATHR_HASH):
	for objIDs in objs:
		obj.load(objIDs["type"], objIDs["hash"], FATHR_HASH)


class RoomDirector(obj.ObjStaticR, obj.ObjUpdate):
	UPDT_POS = 0
	GRP_FILE = "game/data/room_directors.json"
	MAX_ROOMS = 4

	def __init__(self, HASH, FATHR_HASH, rooms, camHash):
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
		self._cam = obj.getGroup(Cam)[camHash]
		self._unloadRooms = rooms
		self._loadRooms = []
		self._activeRooms = []

	@property
	def active(self):
		return self._active
	
	@active.setter
	def active(self, value):
		if value:
			for room in self._activeRooms:
				_resumeObjs(room["objs"])
		else:
			for room in self._activeRooms:
				_pauseObjs(room, [])

		self._active = value


	def update(self):
		if self._cam.active:
			for room in self._activeRooms:
				if not self._cam.colliderect(room["rect"]):
					_pauseObjs(room, self._activeRooms)
					self._activeRooms.remove(room)

			for room in self._loadRooms:
				if (
					self._cam.colliderect(room["rect"]) and
					room not in self._activeRooms
				):
					_resumeObjs(room["objs"])
					self._activeRooms.append(room)

			for room in self._unloadRooms:
				if self._cam.colliderect(room["rect"]):
					
					if len(self._loadRooms) >= self.MAX_ROOMS:
						closedRoom = self._loadRooms.pop(0)
						if closedRoom in self._activeRooms:
							self._activeRooms.remove(closedRoom)
						_saveObjs(closedRoom["objs"])
						_closeObjs(closedRoom, self._loadRooms)
						self._unloadRooms.append(closedRoom)

					self._loadRooms.append(room)
					if room not in self._activeRooms:
						self._activeRooms.append(room)
					self._unloadRooms.remove(room)
					_loadObjs(room["objs"], hash(self))
		else:
			raise obj.ObjNotFoundError(Cam, self._cam.HASH)

	def saveAndClose(self):
		for room in self._loadRooms:
			_saveObjs(room["objs"])
			_closeObjs(room, [])

		obj.Obj.close(self)

	def close(self):
		for room in self._loadRooms:
			_closeObjs(room, [])

		obj.Obj.close(self)


try:
	obj.getGroup(RoomDirector)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(RoomDirector))
