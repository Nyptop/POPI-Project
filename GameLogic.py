from random import randint
from random import choice

class Game:
    def __init__(self):
        self.current_fleet = self.randomly_place_all_ships() 
        self.shotsTaken = []
        self.win = False
        self.shots = 0
        self.gameOver = False
        self.current_row = None
        self.current_column = None

    def randomly_place_all_ships(self):
	    """places all the ships in a legal manner on the board to initialise the game"""
	    shipLengths = [4,3,3,2,2,2,1,1,1,1]
	    fleet = []
	    for shipLength in shipLengths:
	        row = randint(1,10)
	        column = randint(1,10)
	        horizontal = choice([True,False])
	        while self.ok_to_place_ship_at(row,column,horizontal,shipLength,fleet)!=True:
	            row = randint(1,10)
	            column = randint(1,10)
	            horizontal = choice([True,False])
	        fleet = self.place_ship_at(row,column,horizontal,shipLength,fleet)
	    return fleet

    def ok_to_place_ship_at(self, row, column, horizontal, length, fleet):
	    """scans a 2D grid around (and including) the coordinates of the proposed ship, only returning True if it is all open sea"""
	    if horizontal == True:
	        for i in range(row-1, row+2): #iterating over rows from 1 above coordinate to 1 below coordinate
	            for j in range(column-1,column+length+1): #iterating over columns from 1 left of coordinate to 1 right of coordinate
	                if self.is_open_sea(i,j,fleet)==False:
	                    return False
	        #checking the ship is on the board
	        if (column+length-1)>9:
	            return False
	    else:
	        for i in range(row-1, row+length+1): #iterating over rows from 1 above coordinate to 1 below coordinate
	            for j in range(column-1, column+2): #iterating over columns from 1 left of coordinate to 1 right of coordinate
	                if self.is_open_sea(i,j,fleet)==False:
	                    return False
	        #checking the ship is on the board
	        if (row+length-1)>9:
	            return False
	    return True

    def is_open_sea(self,row, column, fleet):
	    """goes through all the ships in the fleet, seeing whether any of them already occupy the coordinates in question"""
	    for ship in fleet:
	        horizontal = ship[2]
	        if horizontal==True:
	            for j in range(ship[1],ship[1]+ship[3]): #scanning along ship (left to right) to ensure coordinates not already occupied
	                if column==j and row == ship[0]:
	                    return False
	        else:
	            for i in range(ship[0],ship[0]+ship[3]): #scanning along ship (top to bottom) to ensure coordinates not already occupied
	                if row==i and column == ship[1]:
	                    return False
	    return True

    def place_ship_at(self, row, column, horizontal, length, fleet):
	    """uses the arguments given to append a ship to the fleet"""
	    emptySet = set()
	    fleet.append((row,column,horizontal,length,emptySet))
	    return fleet

    def handle_shot(self,row,column):
    	"""called after the submit button is pressed, this method processes the shot information"""
    	self.shotsTaken.append((row,column))
    	self.current_row = row
    	self.current_column = column
    	self.shots += 1
    	if self.check_if_hits():
            self.hit()

    def check_if_hits(self):#, row, column, fleet):
	    """for each ship in the fleet, checks whether the hit coordinates are in that ship"""
	    for ship in self.current_fleet:

	        horizontal = ship[2]
	        shipRow = ship[0]
	        shipCol = ship[1]
	        shipLength = ship[3]
	        shipRowCoords = None
	        ShipColCoords = None

	        if horizontal == True:
	            shipColCoords = range(shipCol, shipCol+shipLength) #finding the coordinates of a horizontal ship
	            shipRowCoords = range(shipRow,shipRow+1)
	        else:
	            shipColCoords = range(shipCol, shipCol+1) #finding the coordinates of a vertical ship
	            shipRowCoords = range(shipRow,shipRow+shipLength)

	        if (self.current_row in shipRowCoords) and (self.current_column in shipColCoords): 
	            return True

	    return False 

    def hit(self):#hitRow, hitColumn, fleet):
	    """registers the hit on the correct ship in the fleet, returning the updated fleet and updated ship"""
	    for ship in self.current_fleet:
	        shipRow,shipCol,horizontal,length,shipHits = ship
	        if horizontal==True:
	            shipColumns = range(shipCol, shipCol + length)
	            if (self.current_column in shipColumns) and (shipRow == self.current_row): #finding the correct ship
	                shipHits.add((self.current_row,self.current_column)) #this updates both the fleet and ship variables
	                #return (fleet, ship) 
	        else:
	            shipRows = range(shipRow, shipRow + length)
	            if (self.current_row in shipRows) and (shipCol == self.current_column): #finding the correct ship
	                shipHits.add((self.current_row,self.current_column)) #this updates both the fleet and ship variables
	                #return (fleet, ship) 

    def are_unsunk_ships_left(self):
	    """goes through each ship in the fleet, checking whether any of them have coordinates which have not yet been hit"""
	    for ship in self.current_fleet:
	        shipLength = ship[3]
	        shipHits = len(ship[4])
	        if shipLength > shipHits:
	            return True
	    return False