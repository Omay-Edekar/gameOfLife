import pygame
import os
import sys
import random
import variables
import classes

# Pygame Logic Functions

_image_library = {}

def get_image(path):
	"""Grabs image"""
	global _image_library
	image = _image_library.get(path)
	if image is None:
		canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
		image = pygame.image.load(canonicalized_path)
		_image_library[path] = image
	return image

def text_object(text, font, color):
	"""Creates object for text to be created on"""
	text_surface = font.render(text, True, color)
	return text_surface, text_surface.get_rect()

def render_text(font_size, text, color, x, y):
	"""function to render centered text"""
	font = pygame.font.Font(variables.font, font_size)
	text_surface, text_rect = text_object(text, font, color)
	text_rect.center = (x, y)
	variables.screen.blit(text_surface, text_rect)

def get_key():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				return event.key
			else:
				pass

def get_click():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				return True
			else:
				return False

def set_manual():
	"""sets toggleable grid and increases variable.phase by 1"""
	variables.manual = True
	variables.phase += 1

def add_to_phase():
	"""increase variables.phase by 1"""
	variables.phase += 1

def sets_phase_to(num):
	"""changes value of variables.phase"""
	variables.phase = num

def add_to_generation():
	"""increase variables.generation by 1"""
	variables.generation += 1
	if variables.generation == variables.generationsLeft:
		variables.generation = 0

def remove_from_generation():
	"""increase variables.generation by 1"""
	variables.generation -= 1
	if variables.generation < 0:
		variables.generation = variables.generationsLeft - 1

def toggle_play():
	if variables.play: variables.play = False
	else: variables.play = True

def toggle_created():
	if variables.created: variables.created = False
	else: variables.created = True


# def

# Game of Life Logic Functions

def countNeighbors(grid, rows, cols, x, y):
	neighbors = 0
	for i in range(x-1, x+2):
		for j in range(y-1, y+2):
			if (i < 0 or j < 0 or i > rows-1 or j > cols-1 or (i == x and j ==y)):
				continue
			elif (grid[i][j] != -1):
				neighbors += grid[i][j]
	return neighbors

def processGeneration(grid, storageGrid, rows, cols, generation):
	tempGrid = [[0 for x in range(cols)] for x in range(rows)]
	for i in range(rows):
		for j in range(cols):
			neighbors = countNeighbors(grid, rows, cols, i, j)
			if (grid[i][j] == -1):
				tempGrid[i][j] = -1
			elif (grid[i][j] == 1 and (neighbors < 2 or neighbors > 3)):
				tempGrid[i][j] = 0
			elif (grid[i][j] == 0 and (neighbors == 3)):
				tempGrid[i][j] = 1
			else:
				tempGrid[i][j] = grid[i][j]

	variables.population = 0
	for i in range(rows):
		for j in range(cols):
			if (grid[i][j] == -1):
				continue
			elif (tempGrid[i][j] == 1):
				variables.population += 1
			grid[i][j] = tempGrid[i][j]
	
	if (variables.population > variables.maxPopulation):
		variables.maxPopulation = variables.population
	if (variables.population < variables.minPopulation or variables.minPopulation == 0):
		variables.minPopulation = variables.population
	
	variables.storagePopulation.append(variables.population)
	variables.storageMaxPopulation.append(variables.maxPopulation)
	variables.storageMinPopulation.append(variables.minPopulation)

	for i in range(rows):
		for j in range(cols):
			storageGrid[generation][i][j] = grid[i][j]

def initGrid(grid, storageGrid, rows, cols, generation, not_manual):
	for i in range(rows):
		for j in range(cols):
			if (i == 0 or i == rows-1 or j == 0 or j == cols-1):
				grid[i][j] = -1
			elif not_manual:
				cell = random.randint(1, 3) % 3
				if (cell == 0):
					grid[i][j] = 1
					variables.population += 1
				else:
					grid[i][j] = 0
	if not_manual:
		variables.maxPopulation = variables.population
		variables.minPopulation = variables.population

		variables.storagePopulation.append(variables.population)
		variables.storageMaxPopulation.append(variables.maxPopulation)
		variables.storageMinPopulation.append(variables.minPopulation)

		for i in range(rows):
			for j in range(cols):
				storageGrid[generation][i][j] = grid[i][j]

def printGrid(grid, rows, cols, generation, population, maxPopulation, minPopulation):
	print("\nGeneration: ", generation+1, "\nCurrent Population: ", population, "\nMaximum Population: ", maxPopulation, "\nMinimum Population: ", minPopulation, '\n', end = '')
	for i in range(rows):
		for j in range(cols):
			if (grid[i][j] == -1):
				print("-", ' ',  end = '')
			elif (grid[i][j] == 0):
				print('0', ' ', end = '')
			elif (grid[i][j] == 1):
				print("1", ' ', end = '')
			else:
				print(grid[i][j], ' ', end = '')
		print('')