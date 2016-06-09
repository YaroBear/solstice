#! /usr/bin/python
#masopust-26

import pygame
from pygame import *
import random
import time
import numpy as np

pygame.mixer.pre_init(48000,-16,2, 1024)
pygame.mixer.init()

display_width = 800
display_height = 600
half_w = display_width/2
half_h = display_height/2

snow_color = (153,189,201)
white = (255,255,255)
black = (0,0,0)
gray = (99,122,130)
green = (67,224,125)
sexy_font = ("assets/font/allura.otf")

pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))


snowtile = pygame.image.load("assets/snowtile.png")
snowtile.convert()
icetile = pygame.image.load("assets/ice.png")
icetile.convert()

tiles = {
		0: icetile,
		1: snowtile,
	}



def main():
	first_map = new_map(20,15,.50)
	start_music = pygame.mixer.Sound("assets/beginning.wav")
	lightSurface = pygame.image.load("assets/light_surface.png")
	pygame.display.set_caption('Solstice')
	clock = pygame.time.Clock()

	snow = ParticleSurface(gameDisplay, display_width, display_height, 50, 1)
	snow2 = ParticleSurface(gameDisplay, display_width, display_height, 50, 2)

	menu(gameDisplay,clock)

	viktor = Character("assets/torch.png", 400, 300)

	start_music.play()

	gameExit = False
	up = down = right = left = False

	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					left = True
				elif event.key == pygame.K_RIGHT:
					right = True
				elif event.key == pygame.K_UP:
					up = True
				elif event.key == pygame.K_DOWN:
					down = True

			if event.type ==  pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					left = False
					right = False
				elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					up = False
					down = False


		
# ---------------Order of blit -------------------------------------

		#ignore padding that was made for new_map()

		for row in range(1,21, 1):
			for col in range (1, 16, 1):
				gameDisplay.blit(tiles[first_map[row][col]], ((row-1)*40, (col-1)*40))

		gameDisplay.blit(viktor.image, (viktor.x, viktor.y))
		viktor.move_update(up, down, left, right)

		if 0 == viktor.rect.left:
			first_map = camera(viktor)
			viktor.x = 750
			viktor.rect.x = 750
		elif 750 == viktor.x:
			first_map = camera(viktor)
			viktor.x = 5
			viktor.rect.x = 5
		elif 0 == viktor.y:
			first_map = camera(viktor)
			viktor.y = 550
			viktor.rect.y = 550
		elif 550 == viktor.y:
			first_map = camera(viktor)
			viktor.y = 5
			viktor.rect.y = 5
		

				

		snow.show()
		snow2.show()
		lightx, lighty = viktor.rect.center
		gameDisplay.blit(lightSurface,(lightx-800, lighty-600))
		clock.tick(60)
		pygame.display.update()



class Sprites(pygame.sprite.Sprite):
	def __init_(self):
		pygame.spirte.Sprite.__init__(self)

class Character(Sprites):
	def __init__(self, image, x, y):
		Sprites.__init__(self)
		self.x = x
		self.y = y
		self.ymove = 0
		self.xmove = 0
		self.image = pygame.image.load(image)
		self.image.convert()
		self.rect = Rect(x, y, 78, 100)

	def move_update(self, up, down, left, right):
		if up:
			self.ymove = -5
		if down:
			self.ymove = 5
		if left:
			self.xmove = -5
		if right:
			self.xmove = 5

		if not(left or right):
			self.xmove = 0

		if not(up or down):
			self.ymove = 0

		self.rect.left += self.xmove
		self.rect.top += self.ymove
		#gameDisplay.scroll(0,-self.rect.top)
		self.x += self.xmove
		self.y += self.ymove



class ParticleSurface(object):
	def __init__(self, display, width, height, intensity, speed):
		self.width = width
		self.height = height
		self.intensity = intensity
		self.display = display
		self.speed = speed
		self.list = []

		for i in range(self.intensity):
		    sx = random.randrange(0, self.width)
		    sy = random.randrange(0, self.height)
		    self.list.append([sx, sy])


	def show(self):
		for i in range(len(self.list)):
			pygame.draw.circle(self.display, white, self.list[i], 2)
			self.list[i][1] += self.speed

			# If the snow flake has moved off the bottom of the screen
			if self.list[i][1] > self.height:
			# Reset
				sy = random.randrange(-50, -10)
				self.list[i][1] = sy
			# New x position
				sx = random.randrange(0, self.width)
				self.list[i][0] = sx

class Map(object):
	def __init__(self, size, probability):
		pass

def new_map(row, col, prob):
	grid = np.ones((row+2,col+2), dtype=np.int)
	randX = random.randrange(0,row)
	randY = random.randrange(0,col)
	grid[randX][randY] = 2

	#padding so grid check works
	for i in range(col+2):
		grid[0][i] = 0
		grid[row+1][i] = 0	

	for i in range(row+1):
		grid[i][0] = 0
		grid[i][col+1] = 0

	while 2 in grid:
		for i in range(row+2):
			for j in range(col+2):
				if grid[i][j] == 2:
					if grid[i+1][j] == 1:
						randFloat = random.random()
						if randFloat <= prob:
							grid[i+1][j] = 2
					if grid[i-1][j] == 1:
						randFloat = random.random()
						if randFloat <= prob:
							grid[i-1][j] = 2
					if grid[i][j+1] == 1:
						randFloat = random.random()
						if randFloat <= prob:
							grid[i][j+1] = 2
					if grid[i][j-1] == 1:
						randFloat = random.random()
						if randFloat <= prob:
							grid[i][j-1] = 2
					grid[i][j] = 0
	print(grid)
	return grid

def camera(following):
		new = new_map(20, 15, .50)
		return new

def off_screen(newmap, direction,following):
	if direction == 4:
		for row in range(1,21, 1):
			for col in range (1, 16, 1):
				gameDisplay.blit(tiles[newmap[row][col]], (((row-1)*40)-800, (col-1)*40))
	elif direction == 3:
		for row in range(1,21, 1):
			for col in range (1, 16, 1):
				gameDisplay.blit(tiles[newmap[row][col]], (((row-1)*40)-800, (col-1)*40))
	elif direction == 2:
		for row in range(1,21, 1):
			for col in range (1, 16, 1):
				gameDisplay.blit(tiles[newmap[row][col]], (((row-1)*40)-800, (col-1)*40))
	elif direction == 1:
		for row in range(1,21, 1):
			for col in range (1, 16, 1):
				gameDisplay.blit(tiles[newmap[row][col]], (((row-1)*40)-800, (col-1)*40))


def menu(display,clock):
	menu = True

	while menu:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		display.fill(snow_color)
		menu_text = pygame.font.Font(sexy_font, 80)
		TextSurf, TextRect = text_object("Solstice", menu_text)
		TextRect.center = ((display_width/2),(display_height/3))
		display.blit(TextSurf, TextRect)

		cursor_pos = pygame.mouse.get_pos()
		clicked = pygame.mouse.get_pressed()

		if 450 > cursor_pos[0] > 350 and 350 > cursor_pos[1] > 300:
			pygame.draw.rect(display, green, ((display_width/2)-50, display_height/2, 100, 50))
			if clicked[0] == 1:
				return
		else:
			pygame.draw.rect(display, gray, ((display_width/2)-50, display_height/2, 100, 50))
		play_button = pygame.font.Font(sexy_font, 45)
		Text, Rectangle = text_object("Play", play_button)
		Rectangle.center = (400,325)
		display.blit(Text, Rectangle)

		pygame.display.update()
		clock.tick(15)

def text_object(text, font):
	textSurface = font.render(text, True, black) 
	#arg2 is anti-aliasing
	return textSurface, textSurface.get_rect()



if __name__ == "__main__":
	main()