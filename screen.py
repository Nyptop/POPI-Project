from color import Color
from InputBox import *
from Button import *

class Screen:
	def __init__(self, gridHeight = 11* 30,gridSize = 30, gridWidth = 11* 30,legendSize = 200, backgroundColor = Color.BACKGROUNDBLUE, fontType = "Arial", smallFontSize = 18, bigFontSize = 30):
	    """Initialising all the items on the screen and the variables that control them"""
	    self.gridHeight = gridHeight
	    self.gridWidth = gridWidth
	    self.gridSize = gridSize
	    self.legendSize = legendSize
	    self.gridBorder = 5
	    self.backgroundColor = backgroundColor
	    self.fontType = fontType
	    self.smallFontSize = smallFontSize
	    self.bigFontSize = bigFontSize
	    self.screen = pygame.display.set_mode((gridWidth + legendSize,gridHeight + 40 * 4),0,32)
	    self.smallFont = pygame.font.SysFont(fontType, smallFontSize)
	    self.bigFont = pygame.font.SysFont(fontType, bigFontSize)
	    self.input_box1 = InputBox(30, gridHeight + 40 , 120, 32)
	    self.input_box2 = InputBox(30, gridHeight + 40 * 3, 140, 32)
	    self.input_boxes = [self.input_box1, self.input_box2]
	    self.submitButton = button((0,255,0),245, gridHeight + 5 , 80, 40*4 - 10,'Submit')

	def refresh_background(self):
		"""refreshes the background colour of the screen"""
		self.screen.fill(self.backgroundColor)

	def draw_grid(self):
	    #drawing numbers outside the grid to label the rows and columns
	    self.draw_numbers()

	    #now drawing the grid
	    for y in range(1,11):
	        row = []
	        for x in range(1,11):
	            #drawing squares which represent open ocean, this will be drawn over later if necessary
	            r = pygame.Rect((x*self.gridSize, y*self.gridSize), (self.gridSize - self.gridBorder,self.gridSize - self.gridBorder))
	            pygame.draw.rect(self.screen,(0,0,150), r)

	            #drawing all shots taken as missed shots (hit shots will be drawn over the top later)
	            if (x,y) in self.shotsTaken:
	                r = pygame.Rect((x*self.gridSize, y*self.gridSize), (self.gridSize - self.gridBorder,self.gridSize - self.gridBorder))
	                pygame.draw.rect(self.screen,(173,216,230), r)

	    			#drawing the shots that hit ships over the top
	                self.draw_hit_shot(x,y)

	def draw_numbers(self):
	    """draws numbers on the outside of the grid to label the rows and columns"""
	    for column in range(1,11):
	        num = self.smallFont.render(str(column), False, (0,0,150))
	        self.screen.blit(num,(column*self.gridSize,5))

	    for row in range(1,11):
	        num = self.smallFont.render(str(row), False, (0,0,150))
	        self.screen.blit(num,(5,row*self.gridSize))

	def draw_hit_shot(self,x,y):
		"""given a row and column (x,y), detects whether this hits a ship.
		If a ship is hit, it checks whether it is sunk, and finally draws a square in the appropriate colour."""
	
		#filling up a list with all the coordinates which have been hit, ready for drawing
		coordsHit = []
		for ship in self.current_fleet:
		    if ship[4] != set():
		        ls = list(ship[4])
		        for item in ls:
		            coordsHit.append(item)

		
		if len(coordsHit) == 0: #if no coordinates have been hit, there is nothing to draw
		    pass
		else:
		    #checkShip = None
		    if (x,y) in coordsHit:

		        hitShip = None # this variable will hold information on the ship that has been hit

		        # find the ship
		        for ship in self.current_fleet:
		            if (x,y) in ship[4]:
		                hitShip = ship
		                notHit = False
		                break

		        if self.is_sunk(hitShip): #checking whether the ship is sunk
		            name = self.ship_type(hitShip) 
		            if name == 'battleship': #if a ship is sunk, drawing it in the appropriate colour
		                r = pygame.Rect((x*self.gridSize, y*self.gridSize), (self.gridSize - self.gridBorder,self.gridSize - self.gridBorder))
		                pygame.draw.rect(self.screen,(255,51,78), r)
		            elif name == 'cruiser':
		                r = pygame.Rect((x*self.gridSize, y*self.gridSize), (self.gridSize - self.gridBorder,self.gridSize - self.gridBorder))
		                pygame.draw.rect(self.screen,(255,180,51), r)
		            elif name == 'destroyer':
		                r = pygame.Rect((x*self.gridSize, y*self.gridSize), (self.gridSize - self.gridBorder,self.gridSize - self.gridBorder))
		                pygame.draw.rect(self.screen,(255,248,51), r)
		            elif name == 'submarine':
		                r = pygame.Rect((x*self.gridSize, y*self.gridSize), (self.gridSize - self.gridBorder,self.gridSize - self.gridBorder))
		                pygame.draw.rect(self.screen,(92,255,51), r)
		        else: # if the ship is not sunk, draws the in pink to represent a hit, but not a sinking
		            r = pygame.Rect((x*self.gridSize, y*self.gridSize), (self.gridSize - self.gridBorder,self.gridSize - self.gridBorder))
		            pygame.draw.rect(self.screen,(255,50,255), r) 


	def draw_legend(self):
	    """Draws the legend to the screen"""

	    legendText = self.bigFont.render('Legend: ', False, (0, 0, 150)) #drawing the title of the legend
	    self.screen.blit(legendText,(self.gridWidth +10,5 ))

	    r = pygame.Rect((self.gridWidth +10, 45), (25,25)) # drawing a square in deep blue, corresponding to open ocean
	    pygame.draw.rect(self.screen,(0,0,150), r)
	    oceanText = self.smallFont.render('Open Ocean ', False, (0, 0, 150))
	    self.screen.blit(oceanText,(self.gridWidth + 30 + 10, 45))

	    r = pygame.Rect((self.gridWidth +10, 45 + 30), (25,25)) # drawing a square light blue, corresponding to a miss
	    pygame.draw.rect(self.screen,(173,216,230), r)
	    oceanText = self.smallFont.render('Miss', False, (0, 0, 150))
	    self.screen.blit(oceanText,(self.gridWidth + 30 + 10, 45 + 30 ))

	    r = pygame.Rect((self.gridWidth +10, 45 + 30 * 2), (25,25)) #drawing a square in pink, representing a hit
	    pygame.draw.rect(self.screen,(255,50,255), r)
	    oceanText = self.smallFont.render('Hit', False, (0, 0, 150))
	    self.screen.blit(oceanText,(self.gridWidth + 30 + 10, 45 + 30 * 2))

	    r = pygame.Rect((self.gridWidth + 10, 45 + 30 * 3), (25,25)) # draws a square green, representing a submarine
	    pygame.draw.rect(self.screen,(92,255,51), r)
	    oceanText = self.smallFont.render('Submarine', False, (0, 0, 150))
	    self.screen.blit(oceanText,(self.gridWidth + 30 + 10, 45 + 30 * 3))

	    for i in range(0,2): #loop draws two squares in yellow to represent a destroyer
	        r = pygame.Rect((self.gridWidth + 10 + 30 * i, 45 + 30 * 4), (25,25))
	        pygame.draw.rect(self.screen,(255,248,51), r)
	    oceanText = self.smallFont.render('Destroyer', False, (0, 0, 150))
	    self.screen.blit(oceanText,(self.gridWidth + 30 * 2 + 10, 45 + 30 * 4))

	    for i in range(0,3): #loop draws three squares in orange to represent a cruiser
	        r = pygame.Rect((self.gridWidth + 10 + 30 * i, 45 + 30 * 5), (25,25))
	        pygame.draw.rect(self.screen,(255,180,51), r)
	    oceanText = self.smallFont.render('Cruiser', False, (0, 0, 150))
	    self.screen.blit(oceanText,(self.gridWidth + 30 * 3 + 10, 45 + 30 * 5))

	    for i in range(0,4): # loop draws four squares in red to represent a battle ship
	        r = pygame.Rect((self.gridWidth + 10 + 30 * i, 45 + 30 * 6), (25,25))
	        pygame.draw.rect(self.screen,(255,51,78), r)
	    oceanText = self.smallFont.render('Battleship', False, (0, 0, 150))
	    self.screen.blit(oceanText,(self.gridWidth + 30 * 4 + 10, 45 + 30 * 6))

	def draw_instructions(self):
		"""draws the instructions above the input boxes"""
		instructionX = self.bigFont.render('Enter Row: ', False, Color.DARKBLUE)
		instructionY = self.bigFont.render('Enter Column: ', False, Color.DARKBLUE)
		self.screen.blit(instructionX,(35,self.gridHeight +5 ))
		self.screen.blit(instructionY,(35,self.gridHeight + 40 * 2))

	def draw_input_boxes(self):
		"""draws the two input boxes to the screen"""
		for box in self.input_boxes:
			box.update()
		for box in self.input_boxes:
			box.draw(self.screen)

	def ship_type(self, ship):
	    """returns a string of the type of the ship depending on the ship's length"""
	    length = ship[3]
	    if length == 4:
	        return "battleship"
	    elif length == 3:
	        return "cruiser" 
	    elif length == 2:
	        return "destroyer"
	    elif length == 1:
	        return "submarine"

	def is_sunk(self,ship):
	    """checks if the number of hits equals the length of the ship to determine whether it is sunk"""
	    hits = ship[4]
	    shipLength = ship[3]
	    if len(hits)==shipLength:
	        return True
	    return False

	def update_screen(self,shotsTaken,current_fleet):
		"""this method is called each time through the game loop, updating the screen appropriatly depending on the events"""
		self.shotsTaken = shotsTaken
		self.current_fleet = current_fleet
		
		self.refresh_background()
		self.draw_grid()
		self.draw_legend()
		self.draw_instructions()
		self.submitButton.draw(self.screen)
		self.draw_input_boxes()
		pygame.display.flip()