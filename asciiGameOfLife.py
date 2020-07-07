import random

def countNeighbors(grid, rows, cols, x, y):
	neighbors = 0
	for i in range(x-1, x+2):
		for j in range(y-1, y+2):
			if (i < 0 or j < 0 or i > rows-1 or j > cols-1 or (i == x and j ==y)):
				continue
			elif (grid[i][j] != -1):
				neighbors += grid[i][j]
	return neighbors

def processGeneration(grid, storageGrid, rows, cols, generation, population, maxPopulation, minPopulation):
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

	population = 0
	for i in range(rows):
		for j in range(cols):
			if (grid[i][j] == -1):
				continue
			elif (tempGrid[i][j] == 1):
				population += 1
			grid[i][j] = tempGrid[i][j]
	
	if (population > maxPopulation):
		maxPopulation = population
	if (population < minPopulation or minPopulation == 0):
		minPopulation = population
	
	for i in range(rows):
		for j in range(cols):
			storageGrid[generation][i][j] = grid[i][j]

def initGrid(grid, storageGrid, rows, cols, generation, population, maxPopulation, minPopulation):
	for i in range(rows):
		for j in range(cols):
			if (i == 0 or i == rows-1 or j == 0 or j == cols-1):
				grid[i][j] = -1
			else:
				cell = random.randint(1, 3) % 3
				if (cell == 0):
					grid[i][j] = 1
					population += 1
				else:
					grid[i][j] = 0
	
	maxPopulation = population
	minPopulation = population

	for i in range(rows):
		for j in range(cols):
			storageGrid[generation][i][j] = grid[i][j]

def printGrid(grid, rows, cols, generation):
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

random.seed()

generation = 0
population = 0
maxPopulation = 0
minPopulation = 0

rows = int(input("Welcome to the Game of Life!\nInput the number of rows: "))
cols = int(input("Input the number of columns: "))
generationsLeft = int(input("Input the number of generations: "))

rows += 2
cols += 2

grid = [[0 for i in range(cols)] for i in range(rows)]
storageGrid = [[[0 for i in range(cols)] for i in range(rows)] for i in range(generationsLeft)]

initGrid(grid, storageGrid, rows, cols, generation)
# printGrid(grid, rows, cols, generation)

for i in range(generationsLeft-1):
	generation += 1
	processGeneration(grid, storageGrid, rows, cols, generation)
	# printGrid(grid, rows, cols, generation)

for i in range(generationsLeft):
	print("Generation: ", i+1)
	for j in range(rows):
		for k in range(cols):
			if (storageGrid[i][j][k] == -1):
				print('-', ' ', end = '')
			elif (storageGrid[i][j][k] == 0):
				print('0', ' ', end = '')
			elif (storageGrid[i][j][k] == 1):
				print('1', ' ', end = '')
			else:
				print(storageGrid[i][j][k], ' ', end = '')
		print('')
	print("-"*2*cols)

print("\nThank you for playing the Game of Life!")