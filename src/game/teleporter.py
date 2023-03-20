import obj
from game.player import Player


class CollideTP(obj.ObjStaticR, obj.ObjUpdate):
	GRP_FILE = "game/data/collide_tps.json"
	UPDT_POS = 0

	def __init__(self, HASH, FATHR_HASH, triggerRect, destX, destY):
		obj.ObjStaticRW.__init__(self, HASH, FATHR_HASH)

		self._triggerRect = triggerRect
		self._destX = destX
		self._destY = destY


	def update(self):
		for player in obj.getGroup("Player"):
			if player.hitBox.colliderect(self._triggerRect):
				player.teleport(self._destX, self._destY)

try:
	obj.getGroup(CollideTP)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(CollideTP))
