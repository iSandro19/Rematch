import obj
from game.cam import Cam

class Room(obj.ObjStaticRW):
	CLASS_ID = 2
	GRP_FILE = "game/data/rooms.json"

	def __init__(self, INST_ID, classXinstIDS):
		obj.ObjStaticRW.__init__(self, INST_ID)
		self.classXinstIDS = classXinstIDS

		for inst in classXinstIDS:
			obj.loadR(inst["classID"], inst["instID"])


	def save(self):
		for inst in self.classXinstIDS:
			try:
				group = obj.getGroups(inst["classID"])
				if issubclass(group.OBJS_TYPE, obj.ObjStaticRW):
					group[inst["instID"]].save()

			except obj.ObjInstNotFoundError:
				pass

		self._save(classXinstIDS=self.classXinstIDS)


	def close(self):
		for inst in self.classXinstIDS:
			try:
				obj.getGroups(inst["classID"])[inst["instID"]].close()

			except obj.ObjInstNotFoundError:
				pass

		obj.ObjStaticRW.close(self)

		
rooms = obj.Group(Room)


class RoomDirector(obj.ObjStaticR, obj.ObjUpdate):
	CLASS_ID = 3
	UPDT_POS = 0
	GRP_FILE = "game/data/room_directors.json"
	MAX_ROOMS = 2

	def __init__(self, INST_ID, rooms, camID):
		obj.ObjStaticR.__init__(self, INST_ID)
		self.cam = obj.getGroups(Cam.CLASS_ID)[camID]
		self.unloadRooms = rooms
		self.loadRooms = []

	def update(self):
		print("RoomDirector")
		if self.cam.active:
			print("Cam activa")
			for roomXshape in self.unloadRooms:
				print(roomXshape)
				if self.cam.colliderect(roomXshape["shape"]):
					print("cargar")
					
					if len(self.loadRooms) > self.MAX_ROOMS:
						print("cola llena")
						print(self.loadRooms)
						self.unloalRooms.append(self.loadRooms.pop(0))

						closedRoom = obj.getGroups(Room.CLASS_ID)[roomXshape["roomID"]]
						closedRoom.save()
						closedRoom.close()

					self.loadRooms.append(roomXshape)
					self.unloadRooms.remove(roomXshape)
					obj.loadR(Room.CLASS_ID, roomXshape["roomID"])
		else:
			raise obj.ObjInstNotFoundError(self.cam.CLASS_ID, self.cam.INST_ID)

	def close(self):
		for roomXshape in self.loadRooms:
			closedRoom = obj.getGroups(Room.CLASS_ID)[roomXshape["roomID"]]
			closedRoom.close()


roomDirectors = obj.Group(RoomDirector)
