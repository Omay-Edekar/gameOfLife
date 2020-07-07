import pygame

pygame.init()

# initialize pygame variables
width = 720
heigth = 720
fps = 60
screen = pygame.display.set_mode((width, heigth))
clock = pygame.time.Clock()

# Color Constants
WHITE = (248, 248, 255)
BLACK = (53, 56, 57)
GREY = (192, 192, 192)
LIGHTBLACK = (83, 86, 87)
BROWN = (150, 81, 16)

# Counting Variables
queue = 0
phase = 1

rows = 0
cols = 0
generationsLeft = 0
generation = 0

population = 0
maxPopulation = 0
minPopulation = 0

storagePopulation = []
storageMaxPopulation = []
storageMinPopulation = []

# Boolean Variables
done = False
not_generated = True
grid_creation = False
manual = False
created = False
play = False

# Random Variables
font = "open-sans\\OpenSans-Regular.ttf"