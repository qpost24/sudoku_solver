import csv
import pygame
import time

#If you don't already have Python, install the latest version from:
#https://www.python.org/downloads/
#If you need pygame:
#Open the command prompt
#Type 'python -m pip install pygame' (Not including the apostrophes/single quotes)

#To run this program type in a command prompt 'Python sudoku_solver.py'
#The program will ask for a file name, make sure the file is in the same folder
#as the program


width = 40
height = 40
margin = 5
white = (255, 255, 255)
black = (0, 0, 0)

while(True):
	print("Enter the name of the file you'd like to solve or 'quit' to quit: ")
	fileName = input()
		
	while(not fileName.endswith('.csv')):
		#Leave this loop if the user wants to quit
		if(fileName.lower() == "quit"):
			break
		print("Invalid file type, please enter a .csv file or 'quit' to quit: ")
		fileName = input()
	
	#Leave the loop if the user wants to quit
	if(fileName.lower() == "quit"):
		print("Quitting")
		break
	
	#Check the file exists, otherwise ask again
	try:
		f = open(fileName)
		f.close()
	except IOError:
		print("Error: File does not exist, please check the file name you entered with the files in the folder")
		continue
		
	row_nums = [[]]
	column_nums = [[]]
	box_nums = [[]]
	flags = []
	empty_spots = []

	#read the csv file into a 2D list
	with open(fileName) as csv_file:
		reader = csv.reader(csv_file, delimiter=',')
		
		x = 0
		box_x = 0
		for row in reader:
			#If the row is empty, ignore it
			if(not row):
				continue
			y = 0
			for column in row:
				#Check if row_nums is large enough to hold the next row, if not, expand
				if(x >= len(row_nums)):
					row_nums.append([])
					
				#If a new box is entered into, adjust the box index
				if(x % 3 == 0 or y % 3 == 0):
					box_x = int(y / 3) + int(x / 3) * 3 #(x / 3) * 3 will take the x value and bring it to the closest value that is a multiple of 3
					#Check if box_nums is large enough to hold the next box, if not, expand
					if(box_x >= len(box_nums)):
						box_nums.append([])
							
				#Check if column_nums is large enough to hold the next column, if not, expand
				if(y >= len(column_nums)):
					column_nums.append([])
					
				#check if any numbers conflict and flag the index
				if(column and (column in row_nums[x] or column in column_nums[y] 
					or column in box_nums[box_x])):
					flags.append([x, y])
					if(column in row_nums[x]):
						flags[len(flags) - 1].append(x)
						flags[len(flags) - 1].append(row_nums[x].index(column))
					elif(column in column_nums[y]):
						flags[len(flags) - 1].append(column_nums[y].index(column))
						flags[len(flags) - 1].append(y)
					elif(column in box_nums[box_x]):
						flags[len(flags) - 1].append("Box " + str(box_x))
				
				#Store all possible values for the empty spot in the array empty_spots
				#Record the index of that empty slot's values in the spot of the puzzle
				#it is at
				if(not column):
					empty_spots.append(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
					row_nums[x].append(len(empty_spots) - 1)
					column_nums[y].append(len(empty_spots) - 1)
					box_nums[box_x].append(len(empty_spots) - 1)
				else:
					#Record the value read in into each array
					row_nums[x].append(column)				
					column_nums[y].append(column)
					box_nums[box_x].append(column)
				
				y += 1
			x += 1
		
	if(flags):
		print("\nError: The intial data contains conflicting data values in the following areas:")
		for index in flags:
			message = "Violation at (" + str(index[0]) + ", " + str(index[1]) + ") for value " + row_nums[index[0]][index[1]] + ", conflicting with a value "
			if(len(index) == 4):
				message += "at (" + str(index[2]) + ", " + str(index[3]) + ").\n"
			else:
				message += "in " + str(index[2]) + ".\n"
			print(message)
		continue
		
	#Check the rows for starting values that can remove a value from the empty spots
	for x in range(len(row_nums)):
		for y in range(len(row_nums[x])):
			if(not isinstance(row_nums[x][y], int)):
				for i in range(len(empty_spots)):
					if(i in row_nums[x] and row_nums[x][y] in empty_spots[i]):
						empty_spots[i].remove(row_nums[x][y])
						
	#Check the columns for starting values that can remove a value from the empty spots
	for y in range(len(column_nums)):
		for x in range(len(column_nums[y])):
			if(not isinstance(column_nums[y][x], int)):
				for i in range(len(empty_spots)):
					if(i in column_nums[y] and column_nums[y][x] in empty_spots[i]):
						empty_spots[i].remove(column_nums[y][x])
				
	#Check the boxes for starting values that can remove a value from the empty spots			
	for x in range(len(box_nums)):
		for y in range(len(box_nums[x])):
			if(not isinstance(box_nums[x][y], int)):
				for i in range(len(empty_spots)):
					if(i in box_nums[x] and box_nums[x][y] in empty_spots[i]):
						empty_spots[i].remove(box_nums[x][y])
						
	#Initialize the display for the results
	pygame.init()
	screen = pygame.display.set_mode(((width + margin) * len(row_nums) + 5, (height + margin) * len(row_nums[0]) + 5))
	screen.fill(black)
	#Draw the board with the numbers
	x = 0
	for row in row_nums:
		y = 0
		for column in row_nums:
			pygame.draw.rect(screen, white, [(margin + width) * y + margin, 
				(margin + height) * x + margin, width, height])
			#Display the starting values
			if(not isinstance(row_nums[x][y], int)):
				font = pygame.font.Font('freesansbold.ttf', 20)
				screen.blit(font.render(row_nums[x][y], True, black), [(margin + width) * y + margin, 
				(margin + height) * x + margin] )
			#Display the possible values in the empty spaces
			else:
				font = pygame.font.Font('freesansbold.ttf', 10)
				text = ""
				for item in empty_spots[row_nums[x][y]]:
					text += item
				screen.blit(font.render(text, True, black), [(margin + width) * y + margin, 
				(margin + height) * x + margin] )
				
			#Update the display
			pygame.display.flip()
			y += 1
		x += 1
				
	#Show the display until the user clicks out of it
	done = False
	while not done:
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				done = True
					
	#Clean up
	pygame.quit()	
	csv_file.close()
pygame.quit()