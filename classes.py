import pygame
import time
import functions
import variables

class Button(pygame.Rect):

	def __init__(self, x, y, width, height, message, font_size, inactive_color, active_color, text_color):
		super().__init__(x, y, width, height)
		self.message = message
		self.font_size = int(font_size)
		self.inactive_color = inactive_color
		self.active_color = active_color
		self.text_color = text_color

	def click(self, action=None):

		mouse_pos = pygame.mouse.get_pos()

		if self.collidepoint(mouse_pos):
			pygame.draw.rect(variables.screen, self.active_color, (self.x, self.y, self.width, self.height))
			if functions.get_click() and action is not None:
				action()
		else:
			pygame.draw.rect(variables.screen, self.inactive_color, (self.x, self.y, self.width, self.height))	

		button_font = pygame.font.Font(variables.font, self.font_size)
		text_surface, text_rect = functions.text_object(self.message, button_font, self.text_color)
		text_rect.center = ((self.x + (self.width / 2)), (self.y + (self.height / 2)))
		variables.screen.blit(text_surface, text_rect)

class inputBox(pygame.Rect):

	def __init__(self, x, y, width, height, message, font_size, box_color, border_color, text_color):
		super().__init__(x, y, width, height)
		self.message = message
		self.font_size = font_size
		self.box_color = box_color
		self.border_color = border_color
		self.text_color = text_color

	def display(self, string):
		if self.message == "generation":
			dist = .55

			fontMiddle = pygame.font.Font(variables.font, self.font_size)
			text_surface_middle, text_rect_middle = functions.text_object("Go to", fontMiddle, self.text_color)
			text_rect_middle.center = (self.x, self.y - self.font_size * dist)
	
			variables.screen.blit(text_surface_middle, text_rect_middle)

			functions.render_text(45, ''.join(["Max generation: ", str(variables.generationsLeft)]), variables.BLACK, variables.width/2, variables.heigth * 5/6)

		else:
			dist = 1.1

			fontTop = pygame.font.Font(variables.font, self.font_size)
			text_surface_top, text_rect_top = functions.text_object("Input the", fontTop, self.text_color)
			text_rect_top.center = (self.x, self.y - self.font_size * dist)

			fontMiddle = pygame.font.Font(variables.font, self.font_size)
			text_surface_middle, text_rect_middle = functions.text_object("number of", fontMiddle, self.text_color)
			text_rect_middle.center = (self.x, self.y)

			variables.screen.blit(text_surface_top, text_rect_top)
			variables.screen.blit(text_surface_middle, text_rect_middle)

		dummy1FontBottom = pygame.font.Font(variables.font, self.font_size)
		dummy1_text_surface_bottom, dummy1_text_rect_bottom = functions.text_object(''.join([self.message, ": 777"]), dummy1FontBottom, self.text_color)
		dummy1_text_rect_bottom.center = (self.x, self.y + self.font_size * dist)

		dummy2FontBottom = pygame.font.Font(variables.font, self.font_size)
		dummy2_text_surface_bottom, dummy2_text_rect_bottom = functions.text_object(''.join([self.message, ": "]), dummy2FontBottom, self.text_color)
		dummy2_text_rect_bottom.top = dummy1_text_rect_bottom.top
		dummy2_text_rect_bottom.left = dummy1_text_rect_bottom.left

		fontBottom = pygame.font.Font(variables.font, self.font_size)
		text_surface_bottom, text_rect_bottom = functions.text_object(''.join([self.message, ": ", string]), fontBottom, self.text_color)
		text_rect_bottom.top = dummy1_text_rect_bottom.top
		text_rect_bottom.left = dummy1_text_rect_bottom.left

		pygame.draw.rect(variables.screen, variables.WHITE, (dummy2_text_rect_bottom.right - self.font_size/6, text_rect_bottom.top + self.font_size/6, dummy1_text_rect_bottom.right - dummy2_text_rect_bottom.right + self.font_size/6, text_rect_bottom.height - self.font_size/3), 0)
		pygame.draw.rect(variables.screen, variables.BLACK, (dummy2_text_rect_bottom.right - self.font_size/6, text_rect_bottom.top + self.font_size/6, (dummy1_text_rect_bottom.right - dummy2_text_rect_bottom.right + self.font_size/6) * 1.1, (text_rect_bottom.height - self.font_size/3) * 1.1), 1)

		variables.screen.blit(text_surface_bottom, text_rect_bottom)

		pygame.display.flip()

	def ask(self):
		string = ""

		variables.screen.fill(variables.WHITE)
		self.display(string)

		while True:
			variables.screen.fill(variables.WHITE)
			inkey = functions.get_key()
			if inkey == pygame.K_BACKSPACE:
				string = string[:-1]
			elif inkey == pygame.K_RETURN and string != "":
				break
			elif inkey <= 127 and chr(inkey).isnumeric():
				string += chr(inkey)
			self.display(string)
		
		return string

class grid():

	def __init__(self, rows, cols, alive_color, dead_color, frame_color):
		super().__init__()
		self.rows = rows
		self.cols = cols
		if rows  >= 100 or cols >= 100 : self.margin = 1
		elif rows >= 25 or cols >= 25 : self.margin = 5
		else : self.margin = 10
		self.width = (variables.width-self.margin-cols*self.margin)/(cols)
		self.height = (variables.heigth-self.margin-rows*self.margin)/(rows)
		self.alive_color = alive_color
		self.dead_color = dead_color
		self.frame_color = frame_color

	def displayGrid(self, grid, generation):
		for row in range(self.rows):
			for col in range(self.cols):
				if grid[generation][row][col] == -1:
					color = self.frame_color
				elif grid[generation][row][col] == 0:
					color = self.dead_color
				elif grid[generation][row][col] == 1:
					color = self.alive_color
				pygame.draw.rect(variables.screen, color, (0 + col*self.width + (col+1)*self.margin, 0 + row*self.height + (row+1)*self.margin, self.width, self.height))

	def displayInfo(self):
		fontGen = pygame.font.Font(variables.font, int(self.height/2))
		text_surface_gen, text_rect_gen = functions.text_object(''.join(["Gen: ", str(variables.generation+1)]), fontGen, variables.WHITE)
		text_rect_gen.left = self.width + 2*self.margin
		text_rect_gen.centery = .5*self.height + self.margin

		dummyFontPop = pygame.font.Font(variables.font, int(self.height/3))
		dummy_text_surface_pop, dummy_text_rect_pop = functions.text_object(''.join(["Population: ", str(self.rows*self.cols)]), dummyFontPop, variables.WHITE)
		dummy_text_rect_pop.right = self.width*(self.cols-1) + (self.cols-1)*self.margin + self.margin
		dummy_text_rect_pop.centery = .5*self.height + self.margin

		fontPop = pygame.font.Font(variables.font, int(self.height/3))
		text_surface_pop, text_rect_pop = functions.text_object(''.join(["Population: ", str(variables.storagePopulation[variables.generation])]), fontPop, variables.WHITE)
		text_rect_pop.left = dummy_text_rect_pop.left
		text_rect_pop.centery = dummy_text_rect_pop.centery - (self.height/3) * 1.1

		text_surface_maxPop, text_rect_maxPop = functions.text_object(''.join(["Max Population: ", str(variables.storageMaxPopulation[variables.generation])]), fontPop, variables.WHITE)
		text_rect_maxPop.left = dummy_text_rect_pop.left
		text_rect_maxPop.centery = dummy_text_rect_pop.centery

		text_surface_minPop, text_rect_minPop = functions.text_object(''.join(["Min Population: ", str(variables.storageMinPopulation[variables.generation])]), fontPop, variables.WHITE)
		text_rect_minPop.left = dummy_text_rect_pop.left
		text_rect_minPop.centery = dummy_text_rect_pop.centery + (self.height/3) * 1.1

		variables.screen.blit(text_surface_gen, text_rect_gen)
		variables.screen.blit(text_surface_pop, text_rect_pop)
		variables.screen.blit(text_surface_maxPop, text_rect_maxPop)
		variables.screen.blit(text_surface_minPop, text_rect_minPop)

	def toggleGrid(self, grid):
		if functions.get_click():
			pos = pygame.mouse.get_pos()
			row = int(pos[1]/(self.width + self.margin))
			column = int(pos[0]/(self.height + self.margin))
			if grid[row][column] == 1:
				grid[row][column] = 0
			elif grid[row][column] == 0:
				grid[row][column] = 1