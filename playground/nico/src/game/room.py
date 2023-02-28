import obj
from game.cam import Cam
from game.loader import Loader


class RoomDirector(obj.ObjStaticR, obj.ObjUpdate):
	UPDT_POS = 0
	GRP_FILE = "game/data/room_directors.json"
	MAX_ROOMS = 2

	def __init__(self, HASH, FATHR_HASH, rooms, camID):
		obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
		self.CAM = obj.getGroup(Cam)[camID]
		self.unloadRooms = rooms
		self.loadRooms = []

	def update(self):
		if self.CAM.active:
			for roomXshape in self.unloadRooms:
				if self.CAM.colliderect(roomXshape["shape"]):
					print(roomXshape)
					if len(self.loadRooms) >= self.MAX_ROOMS:
						closedRoom = self.loadRooms.pop(0)
						closedRoom.save()
						closedRoom.close()
						self.unloalRooms.append(closedRoom)

					self.loadRooms.append(roomXshape)
					self.unloadRooms.remove(roomXshape)
					obj.load(Loader, roomXshape["loaderHash"], self.HASH)
		else:
			raise obj.ObjNotFoundError(self.CAM, self.CAM.HASH)

	def close(self):
		for roomXshape in self.loadRooms:
			closedRoom = obj.getGroups(Loader)[roomXshape["loaderHash"]]
			closedRoom.close()


try:
	obj.getGroup(RoomDirector)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(RoomDirector))
