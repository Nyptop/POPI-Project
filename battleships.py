''' This is the basic version of the game without the visualisation. See extension.py for the complete version of the project'''
from random import randint,choice

def is_sunk(ship):
    """checks if the number of hits equals the length of the ship to determine whether it is sunk"""
    hits = ship[4]
    shipLength = ship[3]
    if len(hits)==shipLength:
        return True
    return False

def ship_type(ship):
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

def is_open_sea(row, column, fleet):
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

def ok_to_place_ship_at(row, column, horizontal, length, fleet):
    """scans a 2D grid around (and including) the coordinates of the proposed ship, only returning True if it is all open sea"""
    if horizontal == True:
        for i in range(row-1, row+2): #iterating over rows from 1 above coordinate to 1 below coordinate
            for j in range(column-1,column+length+1): #iterating over columns from 1 left of coordinate to 1 right of coordinate
                if is_open_sea(i,j,fleet)==False:
                    return False
        #checking the ship is on the board
        if (column+length-1)>9:
            return False
    else:
        for i in range(row-1, row+length+1): #iterating over rows from 1 above coordinate to 1 below coordinate
            for j in range(column-1, column+2): #iterating over columns from 1 left of coordinate to 1 right of coordinate
                if is_open_sea(i,j,fleet)==False:
                    return False
        #checking the ship is on the board
        if (row+length-1)>9:
            return False
    return True

def place_ship_at(row, column, horizontal, length, fleet):
    """uses the arguments given to append a ship to the fleet"""
    emptySet = set()
    fleet.append((row,column,horizontal,length,emptySet))
    return fleet

def randomly_place_all_ships():
    """places all the ships in a legal manner on the board to initialise the game"""
    shipLengths = [4,3,3,2,2,2,1,1,1,1]
    fleet = []
    for shipLength in shipLengths:
        row = randint(0,9)
        column = randint(0,9)
        horizontal = choice([True,False])
        while ok_to_place_ship_at(row,column,horizontal,shipLength,fleet)!=True:
            row = randint(0,9)
            column = randint(0,9)
            horizontal = choice([True,False])
        fleet = place_ship_at(row,column,horizontal,shipLength,fleet)
    return fleet


def check_if_hits(row, column, fleet):
    """for each ship in the fleet, checks whether the hit coordinates are in that ship"""
    for ship in fleet:

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

        if (row in shipRowCoords) and (column in shipColCoords): 
            return True

    return False 

def hit(hitRow, hitColumn, fleet):
    """registers the hit on the correct ship in the fleet, returning the updated fleet and updated ship"""
    for ship in fleet:
        shipRow,shipCol,horizontal,length,shipHits = ship
        if horizontal==True:
            shipColumns = range(shipCol, shipCol + length)
            if (hitColumn in shipColumns) and (shipRow == hitRow): #finding the correct ship
                shipHits.add((hitRow,hitColumn)) #this updates both the fleet and ship variables
                return (fleet, ship) 
        else:
            shipRows = range(shipRow, shipRow + length)
            if (hitRow in shipRows) and (shipCol == hitColumn): #finding the correct ship
                shipHits.add((hitRow,hitColumn)) #this updates both the fleet and ship variables
                return (fleet, ship) 

def are_unsunk_ships_left(fleet):
    """goes through each ship in the fleet, checking whether any of them have coordinates which have not yet been hit"""
    for ship in fleet:
        shipLength = ship[3]
        shipHits = len(ship[4])
        if shipLength > shipHits:
            return True
    return False

def main():
    current_fleet = randomly_place_all_ships()
    shotsTaken = []

    game_over = False
    shots = 0
    
    while not game_over:

        loc_str = input("Enter row and column to shoot (separted by space), or enter 'q' to quit: ").split()
        if loc_str == ["q"]:
            break 
        try:   
            current_row = int(loc_str[0])
            current_column = int(loc_str[1])
            shots += 1
            shotsTaken.append((current_row,current_column))

            if check_if_hits(current_row, current_column, current_fleet):
                print("You have a hit!")
                (current_fleet, ship_hit) = hit(current_row, current_column, current_fleet)
                if is_sunk(ship_hit):
                    print("You sank a " + ship_type(ship_hit) + "!")
            else:
                print("You missed!")

            if not are_unsunk_ships_left(current_fleet): game_over = True
        except:
            print("Must enter row and column in a valid format.")
    if game_over == True:
        print("Game over! You required", shots, "shots.")

if __name__ == '__main__':
    main()