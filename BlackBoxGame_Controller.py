import Board
import Ray


class BlackBoxGame():
    """
    BlackBoxGame - a container class representing the game rules and logic for the game Black Box.

    BlackBoxGame holds the over-arching meta-information regarding a game of black box. This includes
    the score, the number of atoms on the board, and the location of these atoms. Because of this it must be
    able to interact with the Board itself (its own class) as well as the Ray class.

    BlackBoxGame is responsible for passing the board the information necessary to instantiate itself (the
    locations of atoms) and then for interrogating it as to what lies at different locations. Once it has
    this information from the board it passes it to the Ray object so that the Ray can process it and act
    accordingly.

    """
    def __init__(self, atoms):
        """
        __init__ - initializes an instance of the BlackBoxGame class
        :param atoms: the location of atoms to be placed on the board
        :type atoms: list[tuples]
        """
        self._board = Board.Board(atoms)
        self._score = 25
        self._atoms = self._board.get_atoms()
        self._guesses = []

    def get_board(self):
        """
        get_board - returns copy of the game's _board object """
        return self._board

    def get_score(self):
        """
        get_score - returns the current score
        :return:score
        :rtype:int
        """
        return self._score

    def set_score(self, change):
        """
        set_score - increments the score by change - can be negative
        :param change: the amount to change the score by
        :type change: int

        """
        self._score = self._score + change

    def move_ray(self, ray):
        """
        move_ray - this is the primary function which is responsible for recursively moving a ray. Although it 
        primarily look after the action of the Ray.Ray class it lives in the Game instance itself.

        THIS IS HOW WE DETERMINE THE EXIT POINT OF ALL RAYS - HORIZONTAL, VERTICAL, OR WITH DETOURS

        :param: ray - the ray object whose trajectory and interactions with the board are being determined
        :param type: Object(Ray.Ray)

        :return: None - side effect - set's ray's terminus 
        :return type: None
        """

        # look to the next spot in the ray's trajectory
        next_coordinates = ray.get_next_location()
        next_location = self._board.get_board_square(next_coordinates)

        # check for a collisition - return if it occurs
        if ray.check_for_collision(next_location):
            return

        # if we didn't collide as we moved we need to look to check our
        # diagonals for atoms
        ccw_diag_coordinates, cw_diag_coordinates = ray.get_diagonals()

        ccw_diagonal = self._board.get_board_square(ccw_diag_coordinates)
        cw_diagonal = self._board.get_board_square(cw_diag_coordinates)

        if ccw_diagonal.is_atom() or cw_diagonal.is_atom():

            # If we're on our first move and the immediately diagonals contain an atom we have a reflection
            if ray.get_current_location() == ray.get_origin_location():

                terminal_square = self._board.get_board_square(
                    ray.get_current_location())

                # let's the ray know it's finished and the square that it's an endpoint
                # self.end_ray(ray, terminal_square)
                return ray.record_edge_collision(terminal_square)

            # otherwise they cause a bend in the path
            else:
                # we have to calculate our trajectory based on the pull
                # of the atoms in our path
                ray.recalculate_trajectory(ccw_diagonal, cw_diagonal)

                # get the coordinates of the next location in our new trajectory
                next_coordinates = ray.get_next_location()

                # determine the next coordinate will result in a collision - return if it would
                if ray.check_for_collision(
                        self._board.get_board_square(next_coordinates)):
                    return

        # move the ray to the next step forward in its current trajectory
        ray.set_current_location(next_coordinates)

        #  finally, recursively call our current function from the next step in its path.
        self.move_ray(ray)

    def shoot_ray(self, origin_row, origin_column):
        """
        shoot_ray - shoots a ray from a given row and column if possible
        :param origin_row:
        :type origin_row:
        :param origin_column:
        :type origin_column:
        :return: Terminus Location (if it exists) or None
        :rtype: tuple(int, int) or None
        """

        # get the the square object at row x column
        origin = self._board.get_board_square((origin_row, origin_column))

        # check that it is a valid "edge" to send a ray from
        origin_check = origin.is_edge()

        # if it's not then return false
        if origin_check == False:
            return False

        # if we pass the origin check create shoot a new Ray.Ray object from row x column
        new_ray = Ray.Ray(origin_row, origin_column)

        # let the square we shot from know its an orign square
        origin.set_originating_ray(new_ray)
        # Deduct 1 from the score since we now have on exit point
        self.set_score(-1)

        # while the ray object has a direction (will be set to none when it reaches an endpoint)
        # send it to the helper function that will move it
        while new_ray.get_direction() != None:
            self.move_ray(new_ray)

    # if we hit an exit point (other than through reflection) deduct the point for that
        terminus = new_ray.get_terminal_location()
        # check the the terminal point is an edge (hitting an atom returns none as terminus)

        if terminus != None:
            # check that the terminus is not a reflection, which shouldn't be counted twice
            terminal_square = self._board.get_board_square(terminus)
            terminal_square.set_terminating_ray(new_ray)
            if terminus != (origin_row, origin_column):
                self.set_score(-1)

        return terminus

    def guess_atom(self, row, column):
        """
        guess_atoms - a function allowing a player to input guesses as to the locations
        of atoms on the board

        :param row: the row coordinate of the potential atom
        :type row: int
        :param column: the column coordinate of the potential atom
        :type column: int
        :return: True or False, indicating whether an atom exists at that coordinate
        :rtype: Bool
        """
        if [row, column] in self._atoms:
            # if an tom was properly guessed remove it from the atom's array
            # and return True, append the guess to the guesses array, and
            #remove it from the available atoms to guess from.
            self._guesses.append([row, column])
            self._atoms.remove([row, column])
            return True

        # otherwise deduct five points and return false
        self.set_score(-5)

        # add the guess to the guesses array
        self._guesses.append([row, column])
        return False

    def atoms_left(self):
        """
        atoms_left - returns the number of unguessed atoms still left
        :return: the number of remaining atoms
        :rtype: int
        """
        return len(self._atoms)
