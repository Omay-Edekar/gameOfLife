import pygame
import random
import time
import variables
import functions
import classes

random.seed()

pygame.init()

pygame.display.set_caption("The Game of Life")

start_button = classes.Button(180, variables.heigth*5/8, 360, 90, "Start", 45, variables.BLACK, variables.LIGHTBLACK, variables.WHITE)
random_button = classes.Button(120, variables.heigth*5/6, 180, 90, "Random", 45, variables.BLACK, variables.LIGHTBLACK, variables.WHITE)
manual_button = classes.Button(420, variables.heigth*5/6, 180, 90, "Manual", 45, variables.BLACK, variables.LIGHTBLACK, variables.WHITE)

rows_inputBox = classes.inputBox(variables.width/2, variables.heigth/2, 200, 100, "rows", 80, variables.WHITE, variables.BLACK, variables.BLACK)
cols_inputBox = classes.inputBox(variables.width/2, variables.heigth/2, 200, 100, "columns", 80, variables.WHITE, variables.BLACK, variables.BLACK)
generationsLeft_inputBox = classes.inputBox(variables.width/2, variables.heigth/2, 200, 100, "generations", 80, variables.WHITE, variables.BLACK, variables.BLACK)
generation_inputBox = classes.inputBox(variables.width/2, variables.heigth/2, 200, 100, "generation", 80, variables.WHITE, variables.BLACK, variables.BLACK)

# -------- Main Program Loop -----------
while not variables.done:

	# --- Main event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			variables.done = True

	# --- Screen-clearing code goes here

	# Here, we clear the screen to white. Don't put other drawing commands
	# above this, or they will be erased with this command.

	# If you want a background image, replace this clear with blit'ing the
	# background image.
	variables.screen.fill(variables.WHITE)

	# --- Drawing code should go here

	if variables.phase == 1:
		variables.screen.fill(variables.WHITE)
		functions.render_text(80, "The Game of Life", variables.BLACK, variables.width/2, variables.heigth*3/8)
		start_button.click(functions.add_to_phase)

	if variables.phase == 2:
		variables.screen.fill(variables.WHITE)
		random_button.click(functions.add_to_phase)
		manual_button.click(functions.set_manual)

	if variables.phase == 3:
		variables.screen.fill(variables.WHITE)
		variables.rows = int(rows_inputBox.ask())
		if variables.rows != 0:
			variables.rows += 2
			variables.screen.fill(variables.WHITE)
			variables.cols = int(cols_inputBox.ask())
			if variables.cols != 0:
				variables.cols += 2
				variables.screen.fill(variables.WHITE)
				variables.generationsLeft = int(generationsLeft_inputBox.ask())
				if variables.generationsLeft != 0:
					functions.sets_phase_to(4)

	if variables.phase == 4:
		if variables.not_generated:
			if variables.grid_creation == False:
				grid = [[0 for i in range(variables.cols)] for j in range(variables.rows)]
				storageGrid = [[[0 for i in range(variables.cols)] for j in range(variables.rows)] for k in range(variables.generationsLeft)]
				displayGrid = classes.grid(variables.rows, variables.cols, variables.BLACK, variables.WHITE, variables.GREY)
				previous_button = classes.Button((displayGrid.width + 2*displayGrid.margin), ((displayGrid.rows-1)*displayGrid.height + displayGrid.rows*displayGrid.margin), displayGrid.width, displayGrid.height, "Previous", displayGrid.height/5, variables.BLACK, variables.LIGHTBLACK, variables.WHITE)
				next_button = classes.Button(((displayGrid.cols-2)*displayGrid.width + (displayGrid.cols-1)*displayGrid.margin), ((displayGrid.rows-1)*displayGrid.height + displayGrid.rows*displayGrid.margin), displayGrid.width, displayGrid.height, "Next", displayGrid.height/3, variables.BLACK, variables.LIGHTBLACK, variables.WHITE)
				play_button = classes.Button((previous_button.x + next_button.x)/2, ((displayGrid.rows-1)*displayGrid.height + displayGrid.rows*displayGrid.margin), displayGrid.width, displayGrid.height, "Play", displayGrid.height/3, variables.BLACK, variables.LIGHTBLACK, variables.WHITE)
				pause_button = classes.Button((previous_button.x + next_button.x)/2, ((displayGrid.rows-1)*displayGrid.height + displayGrid.rows*displayGrid.margin), displayGrid.width, displayGrid.height, "Pause", displayGrid.height/3, variables.BLACK, variables.LIGHTBLACK, variables.WHITE)
				go_to_button = classes.Button((previous_button.x + next_button.x)/2, displayGrid.margin, displayGrid.width, displayGrid.height, "Go To", displayGrid.height/3, variables.BLACK, variables.LIGHTBLACK, variables.WHITE)
				done_button = classes.Button((previous_button.x + next_button.x)/2, ((displayGrid.rows-1)*displayGrid.height + displayGrid.rows*displayGrid.margin), displayGrid.width, displayGrid.height, "Done", displayGrid.height/3, variables.BLACK, variables.LIGHTBLACK, variables.WHITE)
				variables.grid_creation = True

			if variables.manual:
				functions.initGrid(grid, storageGrid, variables.rows, variables.cols, variables.generation, False)
				displayGrid.toggleGrid(grid)
				for row in range(variables.rows):
					for col in range(variables.cols):
						storageGrid[0][row][col] = grid[row][col]
				variables.screen.fill(variables.GREY)
				displayGrid.displayGrid(storageGrid, variables.generation)
				done_button.click(functions.toggle_created)
			else:
				functions.initGrid(grid, storageGrid, variables.rows, variables.cols, variables.generation, True)
				variables.created = True
			
			if variables.created:
				if variables.manual:
					for row in range(variables.rows):
						for col in range(variables.cols):
							if grid[row][col] == 1:
								variables.population += 1
					variables.maxPopulation = variables.population
					variables.minPopulation = variables.population
					variables.storagePopulation.append(variables.population)
					variables.storageMaxPopulation.append(variables.population)
					variables.storageMinPopulation.append(variables.population)

				for i in range(variables.generationsLeft-1):
					variables.generation += 1
					functions.processGeneration(grid, storageGrid, variables.rows, variables.cols, variables.generation)
				variables.generation = 0
				variables.not_generated = False

		if variables.not_generated == False:
			variables.screen.fill(variables.GREY)
			displayGrid.displayGrid(storageGrid, variables.generation)
			displayGrid.displayInfo()

			if variables.play == False:
				previous_button.click(functions.remove_from_generation)
				next_button.click(functions.add_to_generation)
				play_button.click(functions.toggle_play)
				go_to_button.click(functions.add_to_phase)

			elif variables.play == True:
				if variables.queue == variables.fps/3:
					functions.add_to_generation()
					variables.queue = 0
				else: 
					variables.queue += 1
				pause_button.click(functions.toggle_play)

	if variables.phase == 5:
		variables.screen.fill(variables.WHITE)
		tempGeneration = variables.generation
		variables.generation = int(generation_inputBox.ask())-1
		functions.sets_phase_to(4)
		
	# --- Go ahead and update the scree10n with what we've drawn.
	pygame.display.flip()

	# --- Limit to 60 frames per second
	variables.clock.tick(variables.fps)

pygame.quit()