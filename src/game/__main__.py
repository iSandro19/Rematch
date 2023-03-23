import pygame as pg
from pygame.locals import *
from typing import List, Dict, Tuple, Union, Callable
import obj
import game.room
import game.tile
import game.cam
import game.player
import game.control
import game.bckgnd
import game.enemy
import game.menus
import game.teleporter
import game.boss
import game.teleporter
import game.powerup
import game.music

WIND_SIZE = 256,144
FPS = 60
WAIT_TIME = 200		# Tiempo a partir del cual se detecta Pulsado Largo en una tecla

INTRO = 0
GAME  = 1
PAUSE = 2

def main():
	pg.init()
	pg.display.init()
	pg.display.set_mode(WIND_SIZE, flags=SCALED|RESIZABLE, vsync=True)
	icon = pg.image.load('../assets/logo/icono.png')
	pg.display.set_icon(icon)
	pg.display.set_caption("Rematch 2D", "Rematch 2D")

	# Variables para control
	notExit = True	# Bucle de eventos
	gameScreen = INTRO 	# Si estamos en el menú (0), en gameplay (1) o pausados (2)

	clock = pg.time.Clock()
	wind = pg.display.get_surface()
	rect = pg.Rect(0,0,128,72)

	assert pg.image.get_extended()

	cam = None
	player = None 
	roomDir = None

	mainMenu = game.menus.MainMenu(0)

	
	#pg.mixer.music.set_volume(0.5)

	# Instanciar player para poder llamar las funciones
	while notExit:
		# Faltan los inputs que dependen de objetos en la pantalla (menú y pantalla de pausa)
		for event in pg.event.get():
			if gameScreen == INTRO:
				if event.type == pg.QUIT:
					#music.close()
					mainMenu.close()
					notExit = False

				elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
					# Objetos independientes de la sala
					cam = obj.load('Cam', 0, 0)
					player = obj.load('Player', 0, 0)
					roomDir = obj.load('RoomDirector', 0, 0)
					music = obj.load("MusicDirector", 0, 0)
					#music.close()
					mainMenu.close()

					gameScreen = GAME

			elif gameScreen == GAME:
				if event.type == pg.QUIT:
					cam.close()
					player.close()
					roomDir.close()
					music.close()

					notExit = False

				elif event.type == KEYDOWN:
					if event.key == K_SPACE:
						#jump and double jump
						player.jump()
						
					elif event.key == K_q:
						# dash
						player.dash()

					elif event.key == K_w:
						player.basic_attack()

					elif event.key == K_e:
						player.rotatory_attack()

					elif event.key == K_ESCAPE:
						player.active = False
						cam.active = False
						roomDir.active = False
						music.active = False
						pauseMenu = game.menus.PauseMenu(0)

						gameScreen = PAUSE
					elif event.key == K_UP:
						for smallDoor in obj.getGroup(game.teleporter.SmallDoor):
							if smallDoor.active:
								smallDoor.doTPifInDoor()

						for bigDoor in obj.getGroup(game.teleporter.BigDoor):
							if bigDoor.active:
								bigDoor.doTPifInDoor()
				
				elif event.type == KEYUP:
					if event.key == K_SPACE:
						player.fall()

			elif gameScreen == PAUSE:
				if event.type == pg.QUIT:
					cam.close()
					player.close()
					roomDir.close()
					pauseMenu.close()
					music.close()

					notExit = False

				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						player.active = True
						cam.active = True
						roomDir.active = True
						music.active = True
						pauseMenu.close()


						gameScreen = GAME

				elif event.type == MOUSEBUTTONDOWN:
					if pauseMenu.botonC.isSelected():
						player.active = True
						cam.active = True
						roomDir.active = True
						music.active = True
						pauseMenu.close()

						gameScreen = GAME

					elif pauseMenu.botonS.isSelected():
						cam.close()
						player.close()
						roomDir.close()
						pauseMenu.close()
						music.close()

						notExit = False
						#gameScreen = 0


		if gameScreen == GAME:
			keys = pg.key.get_pressed()

			if keys[pg.K_LEFT] and keys[pg.K_RIGHT]:
				player.stopMove()

			elif keys[pg.K_RIGHT]:
				player.moveRight()
				
			elif keys[pg.K_LEFT]:
				player.moveLeft()

			else: player.stopMove()



		obj.update()

		#wind.fill((128, 128, 128))
		obj.draw()

		if gameScreen == GAME:
			if player.life <= 0:
				cam.close()
				player.close()
				roomDir.close()

				mainMenu = game.menus.MainMenu(0)

				gameScreen = INTRO

		pg.display.flip()
		clock.tick(FPS)
	
	pg.display.quit()

	return 0

if __name__ == '__main__':
	main()
