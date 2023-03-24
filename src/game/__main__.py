import pygame as pg
from pygame.locals import *
from distutils.dir_util import copy_tree
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
import game.chandelier
import game.interact

WIND_SIZE = 256,144
FPS = 60

INTRO = 0
GAME  = 1
PAUSE = 2
DEAD = 3
END = 4
CREDITS = 5

def main():
	pg.init()
	pg.display.init()
	pg.display.set_mode(WIND_SIZE, flags=SCALED|FULLSCREEN, vsync=True)
	icon = pg.image.load('../assets/logo/icono.png')
	pg.display.set_icon(icon)
	pg.display.set_caption("Rematch 2D", "Rematch 2D")

	# Variables para control
	notExit = True	# Bucle de principal
	fullscreen = True
	gameScreen = INTRO

	clock = pg.time.Clock()
	wind = pg.display.get_surface()
	rect = pg.Rect(0,0,128,72)

	assert pg.image.get_extended()

	cam = None
	player = None 
	roomDir = None

	mainMenu = game.menus.MainMenu(0)

	# Instanciar player para poder llamar las funciones
	while notExit:
		# Faltan los inputs que dependen de objetos en la pantalla (menú y pantalla de pausa)
		for event in pg.event.get():
			if event.type == KEYDOWN and event.key == K_F11:
				if fullscreen:
					pg.display.set_mode(WIND_SIZE, flags=SCALED|RESIZABLE, vsync=True)
					fullscreen = False

				else:
					pg.display.set_mode(WIND_SIZE, flags=SCALED|FULLSCREEN, vsync=True)
					fullscreen = True


			if gameScreen == INTRO:
				if event.type == pg.QUIT:
					mainMenu.close()
					notExit = False

				elif event.type == MOUSEBUTTONDOWN:
					if mainMenu.botonC.isSelected():
						copy_tree("game/rom", "game/data")

						mainMenu.close()
						cam = obj.load('Cam', 0, 0)
						player = obj.load('Player', 0, 0)
						roomDir = obj.load('RoomDirector', 0, 0)
						music = obj.load("MusicDirector", 0, 0)

						gameScreen = GAME

					elif mainMenu.botonS.isSelected():					
						mainMenu.close()
						cam = obj.load('Cam', 0, 0)
						player = obj.load('Player', 0, 0)
						roomDir = obj.load('RoomDirector', 0, 0)
						music = obj.load("MusicDirector", 0, 0)

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

						for portal in obj.getGroup(game.interact.Portal):
							if portal.active:
								cam.close()
								player.close()
								roomDir.close()
								music.close()
								endMenu = game.menus.EndMenu(0)

								gameScreen = END
				
					elif event.key == K_PLUS:
						music.volUp()

					elif event.key == K_MINUS:
						music.volDown()

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

			elif gameScreen == DEAD:
				if event.type == pg.QUIT:
					deadMenu.close()
					notExit = False

				elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
					deadMenu.close()
					mainMenu = game.menus.MainMenu(0)

					gameScreen = INTRO

			elif gameScreen == END:
				if event.type == pg.QUIT:
					endMenu.close()
					notExit = False

				elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
					creditMenu = game.menus.CreditMenu(0)

					gameScreen = CREDITS

			elif gameScreen == CREDITS:
				if event.type == pg.QUIT:
					creditMenu.close()
					notExit = False

				elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
					creditMenu.close()
					mainMenu = game.menus.MainMenu(0)

					gameScreen = INTRO


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
				music.close()

				deadMenu = game.menus.DeadMenu(0)

				gameScreen = DEAD

		pg.display.flip()
		clock.tick(FPS)
	
	pg.display.quit()

	return 0

if __name__ == '__main__':
	main()
