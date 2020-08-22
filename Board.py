import random
from Square import Square

class Board():
    """
    Board - A Class representing a grid of "Square" objects used to
    play BlackBox.

    The Board's primary responsibility is to act as a container for the individual
    square cells which live inside it and make up the game. It instantiates them
    telling each of them at the time they are born whether or not they contain
    atoms.

    Because the board contains crucial game information it must interact with the
    overarching BlackBoxGame class by providing it squares or the entire board as it
    requests them.
    """
    def __init__(self, number_of_atoms):
        """
        __init__ - initalizes an instance of the board
        :param atoms:   a list of the locations on the board where
                        "atoms will be placed
        :type atoms:    List[tuples]
        """
        if number_of_atoms < 1:
            print("Please enter one or more atoms")
            return None
        self._atoms = number_of_atoms
        self._atom_positions = self.position_atoms()
        # logic around atoms and square types
        self._board = self.build_board(self._atom_positions)

    def position_atoms(self):
        """position_atoms - generate random positions for 
        the number of atoms provided

        @param number_of_atoms: The number of atoms to be placed on the board
        @type number_of_atoms: int

        @return: Array of Atom Positions
        @rtype : List[(tuples)]
        """
        atoms = []
        for i in range(self._atoms):
            x = random.randint(1,8)
            y = random.randint(1,8)
            atoms.append([x,y])
        return atoms
    
    def build_board(self, atom_positions):
        """
        build_board - assembles an instance of the board object with
        atoms at the locations passed in atom_positions

        :param atom_positions: a list of the places where atoms will be placed
        :type atom_positions: List[tuples]
        :return: board - the assembled board [nested array of Square objects] with atoms in place
        :rtype:  List[List[]]
        """
        board = []

        # nested loops to create nested arrays
        for row in range(10):
            board.append([])
            for column in range(10):
                #
                square = Square(row,column)
                board[row].append(square)
                if [row,column] in atom_positions:
                    square.set_atom(True)

        return board

    def get_board(self):
        """
        get_board - returns the board object

        :return: _board - two dimensional array populated with Square Objects
        :rtype: List[List[Object(Square)]]
        """
        return self._board

    def get_board_square(self, square_coordinates):
        """
        get_board_square - returns an individual square object from the board

        :param square_coordinates: a tuple holding the row and columnm (in that order) of the square
        :type square_coordinates: tuple(ints)
        :return: the square object at that location
        :rtype: Object(Square)
        """
        row = square_coordinates[0]
        column = square_coordinates[1]

        return self._board[row][column]

    def get_atoms(self):
        return self._atom_positions
        
