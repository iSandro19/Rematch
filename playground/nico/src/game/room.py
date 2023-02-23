import obj
from game.cam import Cam

class Room(obj.ObjStaticR):
	CLASS_ID = 2
	INST_FILE = "game/data/rooms.json"

	def __init__(self, INST_ID, classXinstIDS):
		obj.ObjStaticR.__init__(self, INST_ID)
		self.classXinstIDS = classXinstIDS

		for inst in classXinstIDS:
			obj.base.TABLE[inst["classID"]].load(inst["instID"])

	def close(self):
		obj.ObjStaticR.close(self)

		for inst in self.classXinstIDS:
			obj.base.TABLE[inst["classID"]][inst["instID"]].close()
		
class Rooms(obj.ObjInstsStaticR):
	OBJ_CLASS = Room

	def __init__(self, iterable=()):
		obj.ObjInstsStaticR.__init__(self, iterable)


class RoomDirector(obj.ObjStaticR, obj.ObjUpdate):
	CLASS_ID = 3
	UPDT_POS = 0
	INST_FILE = "game/data/room_directors.json"
	MAX_ROOMS = 2

	def __init__(self, INST_ID, rooms, camInstID):
		obj.ObjStaticR.__init__(self, INST_ID)
		self.cam = obj.base.TABLE[Cam.CLASS_ID][camInstID]
		self.unloalRooms = rooms
		self.loadRooms = []

	def update(self):
		if self.cam.active:
			for roomXrect in self.unloalRooms:
				if cam.colliderect(roomXshape["shape"]):
					
					if len(self.unloalRoom) > MAX_ROOMS:
						self.unloalRooms.append(self.loadRooms.pop(0))
						obj.base.TABLE[Room.CLASS_ID][roomXshape["instID"]].close()

					self.loadRooms.append(roomXrect)
					self.unloalRooms.remove(roomXrect)
					obj.base.TABLE[Room.CLASS_ID].load(roomXshape["instID"])
		else:
			raise ObjInstNotFoundError(self.cam.CLASS_ID, self.cam.INST_ID)
