import obj
import pygame as pg

class MusicDirector(obj.ObjStaticR):

    GRP_FILE = "game/data/music.json"

    def play_music(self):
        pg.mixer.music.play(-1)

    def stop_music(self):
        pg.mixer.music.stop()

    @property
    def active(self):
        return self._active

    def active(self, value):
        if value: 
            self.play_music()
        else:
            self.stop_music()

        self._active = value


    def __init__(self, HASH, FATHR_HASH, song):

        obj.ObjStaticR.__init__(self, HASH, FATHR_HASH)

        pg.mixer.music.load(song)
        pg.mixer.music.set_volume(0.15)

        self.play_music()


    
    def close(self):

        pg.mixer.music.stop()
        obj.Obj.close(self)

try:
	obj.getGroup(MusicDirector)
except obj.GroupNotFoundError:
	obj.addGroup(obj.Group(MusicDirector))
