import obj
from game.cam import VisibleArea, Cam
import pygame as pg

class MusicDirector(obj.ObjStaticR, obj.ObjUpdate):
    GRP_FILE = "game/data/music.json"
    UPDT_POS = 2

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        if value: 
            pg.mixer.music.unpause()
        else:
            pg.mixer.music.pause()

        self._active = value


    def __init__(self, HASH, FATHR_HASH, camHash, songAreas):

        obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)
        obj.ObjUpdate.__init__(self, HASH, FATHR_HASH)

        self._songAreas = songAreas

        self._playingSong = None

        self._cam = obj.getGroup(Cam)[camHash]

        self._vol = 0.

    def update(self):
        prevSong = self._playingSong

        for sa in self._songAreas:
            for va in sa["areaHashes"]:
                try:
                    inst = obj.getGroup(VisibleArea)[va]
                    if inst.active and inst.colliderect(self._cam):
                        if self._playingSong:
                            self._songAreas.append(self._playingSong)

                        self._playingSong = sa
                        self._songAreas.remove(sa)

                        pg.mixer.music.load(self._playingSong["song"])
                        pg.mixer.music.play(-1)
                        break

                except obj.ObjNotFoundError:
                    pass

        if prevSong and prevSong == self._playingSong:
            anyVA = False
            for va in self._playingSong["areaHashes"]:
                try:
                    inst = obj.getGroup(VisibleArea)[va]
                    anyVA = anyVA or inst.active and inst.colliderect(self._cam)
                except obj.ObjNotFoundError:
                    pass

            if not anyVA:
                self._songAreas.append(self._playingSong)
                self._playingSong = None   
                pg.mixer.music.stop()


    def close(self):
        pg.mixer.music.stop()
        obj.Obj.close(self)

    def volUp(self):
        if self._vol < 1.:
            self._vol += 0.05

        pg.mixer.music.set_volume(self._vol)

    def volDown(self):
        if self._vol > 0.:
            self._vol -= 0.05

        pg.mixer.music.set_volume(self._vol)

try:
	obj.getGroup(MusicDirector)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(MusicDirector))
