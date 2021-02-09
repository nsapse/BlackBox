# required external libraries
import pygame, sys, math

# import of primary class
import BlackBoxGame_Controller as BlackBoxGame

def main(atoms):
    pygame.init()

    # instantiate an instance of the game controller which will create a board
    new_game = BlackBoxGame.BlackBoxGame(atoms)

    # pull the board from the game instance 
    new_board = new_game.get_board()
    # Setup Drawing of Board
    size = width, height = 1200, 1300
    white = 255, 255, 255
    black = 0, 0, 0
    grey = 160, 160, 160
    square_width = (width / 11)
    square_height = (height / 12)
    margin = 10
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Black Box")

    # dictionary to track the current board
    board_tracker = {}

    # the main loop 
    while True:
        pygame.display.flip() 

        # insert a delay so changes are viewable by humans
        pygame.time.delay(100)

        
        # draw the board
        for row in  new_board.get_board():
            for square in row:
                # get the square's position on the board
                x_position, y_position = square.get_position()

                # calculate the coordinates where the square will be drawn
                x_draw =  (margin + square_width) * x_position + margin
                y_draw =  (margin + square_width) * y_position + margin

                # save a copy of each game square as a dictionary in the 
                # board tracker containing pygame Rect objects mapped to its 
                # coordinates so that the board detect actions within where it
                # is drawn
                rect_dimension = (x_draw, y_draw, square_width, square_height)
                board_tracker[int(x_position), int(y_position)] = pygame.Rect(rect_dimension)

                # draw the square's color according to its position and status
                if square.is_edge():
                    # if the square is the origin or terminus of a ray represent that
                     if square.get_originating_ray() == False and square.get_terminating_ray() == False:
                         pygame.draw.rect(screen, grey, rect_dimension)
                     else:
                         if square.get_originating_ray() != False:
                             ray = square.get_originating_ray()
                             color = ray.get_color()
                             pygame.draw.rect(screen, color, rect_dimension)
                         if square.get_terminating_ray() != False:
                             # draw in same color or mark with characters of originating ray? 
                             ray = square.get_terminating_ray()
                             color = ray.get_color()
                             pygame.draw.rect(screen, color, rect_dimension)

              
                else:
                    if not square.is_edge():
                        if square.is_selected():
                            pygame.draw.rect(screen, black, rect_dimension)
                        else:
                            pygame.draw.rect(screen, white, rect_dimension)


        # let the player know their score (if playing actively) or whether they have won or lost
        if new_game.get_score() <= 0:
            game_over()
            
        # if you guess the location of all the atoms you won
        if new_game.atoms_left() == 0:
            you_win()

        else:
            # draw the score
            score_text = f"Score: {str(new_game.get_score())}"

        pygame.draw.rect(screen, black, (15, 1200, 400, 4000))
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        text_surface = font.render(score_text, True, white)
        screen.blit(text_surface, dest=(12, 1200)) 

        # updates the screem so the redrawn squares are visible
        pygame.display.update()

        # instantiate the actual game loop
        for event in pygame.event.get():

            # quits python execution if the user quits 
            if event.type == pygame.QUIT:
                sys.exit()

            # otherwise check the squares to see if they have been clicked
            if event.type == pygame.MOUSEBUTTONUP:

                # loops through the dictionary of game tiles we've 
                # created and takes the coordinates of each (the keys)
                # and the actual objects (the values) to work with each
                for coordinates, square_object in board_tracker.items():

                    # check if the mouse event took place within the boundaries of a game tile
                    if square_object.collidepoint(pygame.mouse.get_pos()):
                        row = coordinates[0]
                        column = coordinates[1]

                        # pull a game tile object to check the properties of and act on accordingly
                        active_game_tile = new_board.get_board_square((row, column))

                        # secondary not-corner check necessary
                        if not active_game_tile.is_edge() and not active_game_tile.is_corner():

                            # A click on a non-edge square constitutes a guess
                            guess = new_game.guess_atom(row, column)

                            if guess:
                                active_game_tile.toggle_selected()

                            pygame.display.update()

                        if active_game_tile.is_edge():
                            # a click on an edge square constitutes shooting a ray
                            new_game.shoot_ray(row, column)


def game_over():
    pygame.init()

    # Setup Drawing of Board
    size = width, height = 1200, 1300
    white = 255, 255, 255
    black = 0, 0, 0
    grey = 160, 160, 160
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Game Over")
    
    display_text = "Game Over"
    pygame.draw.rect(screen, black, (0,0, width, height))
    font = pygame.font.Font(pygame.font.get_default_font(), 64)
    text_surface = font.render(display_text, True, white)
    screen.blit(text_surface, dest=(height/2,width/2)) 

def you_win():
    pygame.init()

    # Setup Drawing of Board
    size = width, height = 1200, 1300
    white = 255, 255, 255
    black = 0, 0, 0
    grey = 160, 160, 160
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("You Win!")

    display_text = "You Win!"
    pygame.draw.rect(screen, black, (0,0, width, height))
    font = pygame.font.Font(pygame.font.get_default_font(), 64)
    text_surface = font.render(display_text, True, white)
    screen.blit(text_surface, dest=(height/2,width/2)) 

if __name__ == "__main__": #TODO - Implement Random Atom Generation
    atoms = int(input("Enter the number of atoms to be placed on the board: "))
    main(atoms)
