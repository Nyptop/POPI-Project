import pytest
from battleships import *




def test_is_sunk1():
    """testing is_sunk on a cruiser"""
    s = (2, 3, False, 3, {(2,3), (3,3), (4,3)})
    assert is_sunk(s) == True

def test_is_sunk2():
    """testing that is_sunk can also return False in the correct way"""
    s = (2, 3, False, 3, {(2,3), (3,3)})
    assert is_sunk(s) == False
    

def test_is_sunk3():
    """testing is_sunk on a submarine"""
    s = (7, 7, True, 1, {(7,7)})
    assert is_sunk(s) == True
    

def test_is_sunk4():
    """testing is_sunk when there are no hits on the ship"""
    s = (7, 7, True, 2, {})
    assert is_sunk(s) == False
    

def test_is_sunk5():
    """testing is_sunk on a battleship"""
    s = (1, 1, True, 4, {(1,1), (1,2), (1,3),(1,4)})
    assert is_sunk(s) == True




def test_ship_type1():
    """testing ship_type on a cruiser that has been sunk"""
    s = (2, 3, False, 3, {(2,3), (3,3), (4,3)})
    assert ship_type(s) == "cruiser"

def test_ship_type2():
    """testing ship_type on a cruiser with no hits"""
    s = (5, 6, False, 3, {})
    assert ship_type(s) == "cruiser"

def test_ship_type3():
    """testing ship_type on a battleship"""
    s = (4, 4, True, 4, {(4,4), (4,6)})
    assert ship_type(s) == "battleship"

def test_ship_type4():
    """testing ship type on a submarine"""
    s = (3, 6, True, 1, {})
    assert ship_type(s) == "submarine"

def test_ship_type5():
    """finally, testing ship type on a destroyer, so all possible return values of ship_type have been tested"""
    s = (7, 4, True, 2, {(7,5)})
    assert ship_type(s) == "destroyer"





def test_is_open_sea1():
    """testing one up and one left from ship head"""
    row = 1
    column = 2
    s = (2, 3, False, 3, {(2,3), (3,3), (4,3)})
    fleet = [s]
    assert is_open_sea(row,column,fleet) == True
    
def test_is_open_sea2():
    """testing inside the ship"""
    row = 3
    column = 3
    s = (2, 3, False, 3, {(2,3), (3,3), (4,3)})
    fleet = [s]
    assert is_open_sea(row,column,fleet) == False

def test_is_open_sea3():
    """testing just beyond the end of the ship"""
    row = 5
    column = 3
    s = (2, 3, False, 3, {(2,3), (3,3), (4,3)})
    fleet = [s]
    assert is_open_sea(row,column,fleet) == True

def test_is_open_sea4():
    """testing with a full fleet"""
    row = 5
    column = 6
    fleet = [(8, 2, True, 3, set()), (1, 4, False, 2, set()), (5, 2, False, 2, set()), (1, 9, False, 2, set()), (8, 6, False, 1, set()), (6, 8, False, 1, set()), (3, 2, True, 1, set()), (1, 2, False, 1, set()), (6, 4, True, 3, {(6, 6), (6, 4), (6, 5)}), (0, 7, False, 4, {(3, 7)})]
    assert is_open_sea(row,column,fleet) == True

def test_is_open_sea5():
    """testing to make sure is_open_sea correctly returns false given a full fleet"""
    row = 6
    column = 6
    fleet = [(8, 2, True, 3, set()), (1, 4, False, 2, set()), (5, 2, False, 2, set()), (1, 9, False, 2, set()), (8, 6, False, 1, set()), (6, 8, False, 1, set()), (3, 2, True, 1, set()), (1, 2, False, 1, set()), (6, 4, True, 3, {(6, 6), (6, 4), (6, 5)}), (0, 7, False, 4, {(3, 7)})]
    assert is_open_sea(row,column,fleet) == False




def test_ok_to_place_ship_at1():
    """simple test with a submarine"""
    row = 7
    column = 7
    horizontal = False
    length = 1
    fleet = [(9, 3, True, 4, set()), (4, 0, True, 3, set()), (6, 2, True, 3, set()), (0, 4, False, 2, set()), (6, 9, False, 2, set()), (1, 7, False, 2, set()), (4, 6, False, 1, set()), (9, 1, True, 1, set()), (4, 8, False, 1, set())]
    assert ok_to_place_ship_at(row,column,horizontal,length,fleet) == True

def test_ok_to_place_ship_at2():
    """more difficult test with a battleship"""
    row = 9
    column = 3
    horizontal = True
    length = 4
    fleet = [(4, 0, True, 3, set()), (6, 2, True, 3, set()), (0, 4, False, 2, set()), (6, 9, False, 2, set()), (1, 7, False, 2, set()), (4, 6, False, 1, set()), (7, 7, False, 1, set()), (9, 1, True, 1, set()), (4, 8, False, 1, set())]
    assert ok_to_place_ship_at(row,column,horizontal,length,fleet) == True

def test_ok_to_place_ship_at3():
    """testing that it can correctly return false when the tail of a battleship overlaps another"""
    row = 9
    column = 3
    horizontal = True
    length = 4
    fleet = [(4, 0, True, 3, set()), (6, 2, True, 3, set()), (0, 4, False, 2, set()), (6, 9, False, 2, set()), (1, 7, False, 2, set()), (4, 6, False, 1, set()), (7, 7, False, 1, set()), (9, 6, True, 1, set()), (4, 8, False, 1, set())]
    assert ok_to_place_ship_at(row,column,horizontal,length,fleet) == False

def test_ok_to_place_ship_at4():
    """testing that it can correctly return false even when there is open sea if the ship is only one diagonal step away from another
    I'm doing this by placing a battleship whose tail is one diagonal step from a submarine at (8,7)"""
    row = 9
    column = 3
    horizontal = True
    length = 4
    fleet = [(4, 0, True, 3, set()), (6, 2, True, 3, set()), (0, 4, False, 2, set()), (6, 9, False, 2, set()), (1, 7, False, 2, set()), (4, 6, False, 1, set()), (7, 7, False, 1, set()), (8, 7, True, 1, set()), (4, 8, False, 1, set())]
    assert ok_to_place_ship_at(row,column,horizontal,length,fleet) == False

def test_ok_to_place_ship_at5():
    """another test to see whether ok_to_place_ship_at returns false when a proposed ship is a single diagonal step away from an existing one
    this time, with the tails of a battleship and a cruiser """
    row = 4
    column = 1
    horizontal = True
    length = 4
    fleet = [(1, 5, False, 3, set())]
    #tail of cruiser is at (3,5), tail of battleship at (4,4)
    assert ok_to_place_ship_at(row,column,horizontal,length,fleet) == False

def test_ok_to_place_ship_at6():
    """testing ok_to_place_ship_at returns false when proposed ship has block one horizontal step from an existing ship's block"""
    row = 5
    column = 2
    horizontal = True
    length = 4
    fleet = [(4, 6, False, 3, set())]
    assert ok_to_place_ship_at(row,column,horizontal,length,fleet) == False

def test_ok_to_place_ship_at7():
    """testing ok_to_place_ship_at returns false when proposed ship has block one vertical step from an existing ship's block"""
    row = 5
    column = 2
    horizontal = True
    length = 4
    fleet = [(2, 3, False, 3, set())]
    assert ok_to_place_ship_at(row,column,horizontal,length,fleet) == False

def test_ok_to_place_ship_at8():
    """testing that this function correctly returns false when a horizontal ship goes off the end of the board""" 
    row = 5
    column = 7
    horizontal = True
    length = 4
    fleet = []
    assert ok_to_place_ship_at(row,column,horizontal,length,fleet) == False

def test_ok_to_place_ship_at9():
    """testing that this function correctly returns true when a horizontal ship is close, but not over, the edge of the board"""
    row = 5
    column = 6
    horizontal = True
    length = 4
    fleet = []
    assert ok_to_place_ship_at(row,column,horizontal,length,fleet) == True

def test_ok_to_place_ship_at10():
    """testing that this function correctly returns false when a vertical ship goes off the end of the board""" 
    row = 7
    column = 7
    horizontal = False
    length = 4
    fleet = []
    assert ok_to_place_ship_at(row,column,horizontal,length,fleet) == False

def test_ok_to_place_ship_at11():
    """testing that this function correctly returns true when a vertical ship is close, but not over, the edge of the board"""
    row = 6
    column = 6
    horizontal = False
    length = 4
    fleet = []
    assert ok_to_place_ship_at(row,column,horizontal,length,fleet) == True




def test_place_ship_at1():
    """testing the very first placement of a battleship in an empty fleet"""
    row = 3
    column = 8
    horizontal = False
    length = 4
    fleet = []
    emptySet = set()
    newFleet = fleet + [(row,column,horizontal,length,emptySet)]
    assert place_ship_at(row,column,horizontal,length,fleet)==newFleet

def test_place_ship_at2():
    """a test of a typical case for this function (placing destroyer after battleship and cruisers have been placed)"""
    row = 9
    column = 1
    horizontal = True
    length = 2
    fleet = [(3, 3, False, 4, set()), (0, 4, True, 3, set()), (5, 0, False, 3, set()), (2, 6, True, 2, set())]
    emptySet = set()
    newFleet = fleet + [(row,column,horizontal,length,emptySet)]
    assert place_ship_at(row,column,horizontal,length,fleet)==newFleet

def test_place_ship_at3():
    """a further test of a typical use of this function (placing another cruiser after battleship and cruiser already placed)"""
    row = 9
    column = 4
    horizontal = True
    length = 3
    fleet = [(4, 7, False, 4, set()), (2, 5, True, 3, set())]
    emptySet = set()
    newFleet = fleet + [(row,column,horizontal,length,emptySet)]
    assert place_ship_at(row,column,horizontal,length,fleet)==newFleet

def test_place_ship_at4():
    """a further test of a typical use of this function (placing a submarine after all larger ships have been placed)"""
    row = 1
    column = 1
    horizontal = True
    length = 1
    fleet = [(0, 5, False, 4, set()), (6, 8, False, 3, set()), (6, 1, True, 3, set()), (2, 9, False, 2, set()), (3, 3, False, 2, set()), (0, 3, False, 2, set())]
    emptySet = set()
    newFleet = fleet + [(row,column,horizontal,length,emptySet)]
    assert place_ship_at(row,column,horizontal,length,fleet)==newFleet

def test_place_ship_at5():
    """testing the placement of the very last ship"""
    row = 8
    column = 0
    horizontal = True
    length = 1
    fleet = [(4, 5, True, 4, set()), (3, 0, True, 3, set()), (6, 4, False, 3, set()), (1, 7, True, 2, set()), (6, 7, True, 2, set()), (1, 3, True, 2, set()), (1, 1, True, 1, set()), (8, 8, True, 1, set()), (5, 1, True, 1, set())]
    emptySet = set()
    newFleet = fleet + [(row,column,horizontal,length,emptySet)]
    assert place_ship_at(row,column,horizontal,length,fleet)==newFleet
    




def test_check_if_hits1():
    """testing a positive hit with a full fleet in mid-game"""
    row = 0
    column = 8
    fleet = [(8, 3, True, 4, set()), (6, 1, True, 3, set()), (0, 6, False, 2, set()), (0, 3, False, 1, set()), (4, 8, True, 1, set()), (6, 8, True, 1, set()), (3, 1, False, 1, {(3, 1)}), (4, 6, False, 2, {(4, 6)}), (2, 3, False, 2, {(3, 3)}), (0, 8, False, 3, {(1, 8)})]
    assert check_if_hits(row,column,fleet)==True

def test_check_if_hits2():
    """testing the very first hit in a game"""
    row = 4
    column = 1
    fleet = [(4, 4, False, 4, set()), (0, 4, False, 3, set()), (6, 9, False, 3, set()), (2, 9, False, 2, set()), (4, 0, True, 2, set()), (2, 6, True, 2, set()), (7, 1, True, 1, set()), (1, 2, True, 1, set()), (7, 7, True, 1, set()), (0, 9, False, 1, set())]
    assert check_if_hits(row,column,fleet)==True

def test_check_if_hits3():
    """testing that this function still returns True even when a coordinate has been hit before
    even though though it would not be rational for a user to make such a move, they might still accidently play this move, so it is important to test"""
    row = 2
    column = 1
    fleet = [(0, 1, True, 2, {(0, 1), (0, 2)}), (0, 4, True, 1, {(0, 4)}), (2, 1, True, 2, {(2, 1), (2, 2)}), (0, 6, False, 3, {(1, 6), (2, 6), (0, 6)}), (3, 4, True, 1, {(3, 4)}), (6, 1, True, 1, {(6, 1)}), (6, 4, True, 3, {(6, 6), (6, 4), (6, 5)}), (5, 8, False, 2, {(6, 8), (5, 8)}), (8, 0, True, 1, {(8, 0)}), (9, 2, True, 4, {(9, 2), (9, 3)})]
    assert check_if_hits(row,column,fleet)==True

def test_check_if_hits5():
    """testing that a near miss returns False"""
    row = 0
    column = 2
    fleet = [(8, 3, True, 4, set()), (6, 1, True, 3, set()), (0, 6, False, 2, set()), (0, 3, False, 1, set()), (4, 8, True, 1, set()), (6, 8, True, 1, set()), (3, 1, False, 1, {(3, 1)}), (4, 6, False, 2, {(4, 6)}), (2, 3, False, 2, {(3, 3)}), (0, 8, False, 3, {(1, 8)})]
    assert check_if_hits(row,column,fleet)==False

def test_check_if_hits6():
    """testing that another near miss returns False"""
    row = 5
    column = 8
    fleet = [(8, 3, True, 4, set()), (6, 1, True, 3, set()), (0, 6, False, 2, set()), (0, 3, False, 1, set()), (4, 8, True, 1, set()), (6, 8, True, 1, set()), (3, 1, False, 1, {(3, 1)}), (4, 6, False, 2, {(4, 6)}), (2, 3, False, 2, {(3, 3)}), (0, 8, False, 3, {(1, 8)})]
    assert check_if_hits(row,column,fleet)==False




def test_hit1():
    """testing a typical scenario for hit mid-game"""
    hitRow = 3
    hitCol = 8
    fleet = [(5, 1, False, 3, set()), (6, 3, True, 2, set()), (7, 7, False, 2, set()), (8, 5, False, 1, set()), (4, 3, True, 1, set()), (1, 1, True, 3, {(1, 1), (1, 2), (1, 3)}), (1, 5, True, 1, {(1, 5)}), (1, 7, True, 2, {(1, 7), (1, 8)}), (3, 0, True, 1, {(3, 0)}), (3, 5, True, 4, {(3, 7), (3, 5), (3, 6)})]
    assert hit(hitRow,hitCol,fleet) == ([(5, 1, False, 3, set()), (6, 3, True, 2, set()), (7, 7, False, 2, set()), (8, 5, False, 1, set()), (4, 3, True, 1, set()), (1, 1, True, 3, {(1, 1), (1, 2), (1, 3)}), (1, 5, True, 1, {(1, 5)}), (1, 7, True, 2, {(1, 7), (1, 8)}), (3, 0, True, 1, {(3, 0)}), (3, 5, True, 4, {(3, 7), (3, 8), (3, 5), (3, 6)})],(3, 5, True, 4, {(3, 7), (3, 8), (3, 5), (3, 6)}))

def test_hit2():
    """testing a second typical scenario for hit mid-game"""
    hitRow = 8
    hitCol = 2
    fleet = [(5, 8, False, 4, {(6, 8), (7, 8), (5, 8)}), (6, 2, False, 3, {(6, 2), (7, 2)}), (3, 6, True, 3, {(3, 7), (3, 8), (3, 6)}), (0, 8, True, 2, {(0, 8), (0, 9)}), (8, 5, True, 2, set()), (0, 2, True, 2, {(0, 2), (0, 3)}), (5, 0, True, 1, {(5, 0)}), (2, 1, True, 1, {(2, 1)}), (6, 5, True, 1, {(6, 5)}), (0, 5, False, 1, {(0, 5)})]
    assert hit(hitRow,hitCol,fleet) == ([(5, 8, False, 4, {(6, 8), (7, 8), (5, 8)}), (6, 2, False, 3, {(8, 2), (6, 2), (7, 2)}), (3, 6, True, 3, {(3, 7), (3, 8), (3, 6)}), (0, 8, True, 2, {(0, 8), (0, 9)}), (8, 5, True, 2, set()), (0, 2, True, 2, {(0, 2), (0, 3)}), (5, 0, True, 1, {(5, 0)}), (2, 1, True, 1, {(2, 1)}), (6, 5, True, 1, {(6, 5)}), (0, 5, False, 1, {(0, 5)})],(6, 2, False, 3, {(8, 2), (6, 2), (7, 2)}))

def test_hit3():
    """testing the very last hit to finish the game"""
    hitRow = 9
    hitCol = 4
    fleet = [(2, 5, True, 4, {(2, 5), (2, 6), (2, 7), (2, 8)}), (7, 3, True, 3, {(7, 4), (7, 5), (7, 3)}), (6, 0, False, 3, {(7, 0), (8, 0), (6, 0)}), (4, 2, False, 2, {(4, 2), (5, 2)}), (6, 7, True, 2, {(6, 7), (6, 8)}), (2, 2, True, 2, {(2, 3), (2, 2)}), (0, 1, False, 1, {(0, 1)}), (0, 3, False, 1, {(0, 3)}), (0, 9, True, 1, {(0, 9)}), (9, 4, False, 1, set())]
    assert hit(hitRow,hitCol,fleet) == ([(2, 5, True, 4, {(2, 5), (2, 6), (2, 7), (2, 8)}), (7, 3, True, 3, {(7, 4), (7, 5), (7, 3)}), (6, 0, False, 3, {(7, 0), (8, 0), (6, 0)}), (4, 2, False, 2, {(4, 2), (5, 2)}), (6, 7, True, 2, {(6, 7), (6, 8)}), (2, 2, True, 2, {(2, 3), (2, 2)}), (0, 1, False, 1, {(0, 1)}), (0, 3, False, 1, {(0, 3)}), (0, 9, True, 1, {(0, 9)}), (9, 4, False, 1, {(9,4)})],(9, 4, False, 1, {(9,4)}))

def test_hit4():
    """testing the very first hit of the game"""
    hitRow = 0
    hitCol = 0
    fleet = [(3, 5, False, 4, set()), (1, 7, True, 3, set()), (9, 4, True, 3, set()), (6, 0, True, 2, set()), (4, 9, False, 2, set()), (0, 0, False, 2, set()), (1, 5, True, 1, set()), (7, 7, True, 1, set()), (3, 7, True, 1, set()), (3, 0, False, 1, set())]
    assert hit(hitRow,hitCol,fleet) == ([(3, 5, False, 4, set()), (1, 7, True, 3, set()), (9, 4, True, 3, set()), (6, 0, True, 2, set()), (4, 9, False, 2, set()), (0, 0, False, 2, {(0, 0)}), (1, 5, True, 1, set()), (7, 7, True, 1, set()), (3, 7, True, 1, set()), (3, 0, False, 1, set())],(0, 0, False, 2, {(0, 0)}))

def test_hit5():
    """testing hit function on a coordinate which has already been hit"""
    hitRow = 0
    hitCol = 4
    fleet = [(3, 7, False, 3, set()), (8, 4, True, 3, set()), (1, 1, True, 2, set()), (4, 5, False, 2, set()), (9, 1, True, 2, set()), (7, 8, False, 1, set()), (4, 1, False, 1, set()), (6, 1, True, 1, set()), (5, 3, False, 1, set()), (0, 4, True, 4, {(0, 4)})]
    assert hit(hitRow,hitCol,fleet) == ([(3, 7, False, 3, set()), (8, 4, True, 3, set()), (1, 1, True, 2, set()), (4, 5, False, 2, set()), (9, 1, True, 2, set()), (7, 8, False, 1, set()), (4, 1, False, 1, set()), (6, 1, True, 1, set()), (5, 3, False, 1, set()), (0, 4, True, 4, {(0, 4)})],(0, 4, True, 4, {(0, 4)}))




def test_are_unsunk_ships_left1():
    """testing with one coordinate left to hit"""
    fleet = [(8, 8, False, 1, set()), (0, 7, False, 1, {(0, 7)}), (1, 2, True, 4, {(1, 2), (1, 3), (1, 4), (1, 5)}), (0, 9, False, 3, {(2, 9), (0, 9), (1, 9)}), (4, 1, True, 1, {(4, 1)}), (4, 6, True, 2, {(4, 6), (4, 7)}), (3, 4, False, 3, {(4, 4), (5, 4), (3, 4)}), (6, 6, True, 2, {(6, 6), (6, 7)}), (8, 3, False, 1, {(8, 3)}), (8, 5, True, 2, {(8, 5), (8, 6)})]
    assert are_unsunk_ships_left(fleet)==True

def test_are_unsunk_ships_left2():
    """testing with a completed game"""
    fleet = [(8, 8, False, 1, {8,8}), (0, 7, False, 1, {(0, 7)}), (1, 2, True, 4, {(1, 2), (1, 3), (1, 4), (1, 5)}), (0, 9, False, 3, {(2, 9), (0, 9), (1, 9)}), (4, 1, True, 1, {(4, 1)}), (4, 6, True, 2, {(4, 6), (4, 7)}), (3, 4, False, 3, {(4, 4), (5, 4), (3, 4)}), (6, 6, True, 2, {(6, 6), (6, 7)}), (8, 3, False, 1, {(8, 3)}), (8, 5, True, 2, {(8, 5), (8, 6)})]
    assert are_unsunk_ships_left(fleet)==False

def test_are_unsunk_ships_left3():
    """testing the game in its starting state"""
    fleet = [(0, 4, True, 4, set()), (3, 7, False, 3, set()), (8, 4, True, 3, set()), (1, 1, True, 2, set()), (4, 5, False, 2, set()), (9, 1, True, 2, set()), (7, 8, False, 1, set()), (4, 1, False, 1, set()), (6, 1, True, 1, set()), (5, 3, False, 1, set())]
    assert are_unsunk_ships_left(fleet)==True

def test_are_unsunk_ships_left4():
    """testing a typical mid game scenario"""
    fleet = [(5, 1, False, 3, set()), (6, 3, True, 2, set()), (7, 7, False, 2, set()), (8, 5, False, 1, set()), (4, 3, True, 1, set()), (1, 1, True, 3, {(1, 1), (1, 2), (1, 3)}), (1, 5, True, 1, {(1, 5)}), (1, 7, True, 2, {(1, 7), (1, 8)}), (3, 0, True, 1, {(3, 0)}), (3, 5, True, 4, {(3, 7), (3, 5), (3, 6)})]
    assert are_unsunk_ships_left(fleet)==True

def test_are_unsunk_ships_left5():
    """testing a different scenario where all ships are sunk"""
    fleet = [(0, 4, False, 2, {(0, 4), (1, 4)}), (1, 6, True, 1, {(1, 6)}), (0, 0, False, 3, {(1, 0), (2, 0), (0, 0)}), (0, 8, False, 3, {(0, 8), (1, 8), (2, 8)}), (5, 5, True, 2, {(5, 5), (5, 6)}), (3, 2, False, 4, {(3, 2), (6, 2), (4, 2), (5, 2)}), (7, 8, False, 1, {(7, 8)}), (8, 1, True, 1, {(8, 1)}), (9, 3, True, 1, {(9, 3)}), (9, 6, True, 2, {(9, 6),(9,7)})]
    assert are_unsunk_ships_left(fleet)==False
    
