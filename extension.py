'''version of battleships which includes visualisation'''

from random import randint,choice
import pygame
import copy
from InputBox import *
from Button import *
from tkinter import *
from tkinter import messagebox
from screen import Screen
from GameLogic import Game

def main():
    """In this extension, I have moved and adapted the mandatory functions to be methods in the Game class in the GameLogic.py file. 
    I have also created the Screen class in screen.py, which draws and updates the pygame screen."""
    
    pygame.init()
    pygame.display.set_caption('Battleships')

    game = Game() # creating a game class to handle the logic, also initialises the fleet
    screen = Screen() # creating a screen class which handles drawing and updating the screen

    running = True

    while running == True:

        #this for loop handles events
        for event in pygame.event.get():

            if event.type == pygame.QUIT: #in the case of quiting, stops the game loop
                running = False

            for box in screen.input_boxes: # handling events related to drawing the input boxes
                box.handle_event(event) 

            if event.type == pygame.MOUSEBUTTONDOWN:
            	if screen.submitButton.isOver(pygame.mouse.get_pos()): # when the submit button is pressed

                    try:
                        column = int(screen.input_boxes[0].get_text()) # getting the row and column information from the input boxes
                        row = int(screen.input_boxes[1].get_text()) 
                        game.handle_shot(row,column)  # this performs the necessary logic after a shot is taken

                    except: # when the input in the input boxes is not two integers
                        Tk().wm_withdraw() #to hide the main window
                        messagebox.showinfo('Error','Please enter a valid row and column number') 

                    screen.input_boxes[0].reset_text() # input box text is reset after 'submit' button is pressed 
                    screen.input_boxes[1].reset_text()



        #checking for the end of the game
        if not game.are_unsunk_ships_left():
            Tk().wm_withdraw()
            messagebox.showinfo('Congratulations',f'Well done on finishing the game, you required {len(game.shotsTaken)} shots.') 
            running = False

        # redrawing the screen   
        screen.update_screen(game.shotsTaken, game.current_fleet)

if __name__ == '__main__':
    main()