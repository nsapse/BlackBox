import random

class Ray():
    """
    Ray - a class representing a ray shot from an edge of a board in the game
    Blackbox

    A ray is responsible for knowing its location and current direction and calculating its trajectory

    communicate with square objects (which are passed to it) and with the game itself (which passes the ray
    information based on the parts of the board it is currently interacting with).

    """
    def __init__(self, origin_row, origin_column):
        """
        __init__ - initializes a Ray object

        :param origin_row: The row from which it originates
        :type origin_row: int
        :param origin_column: The column from which it originates
        :type origin_column: int
        """

        # Set the ray's point of origination
        self._origin_row = origin_row
        self._origin_column = origin_column

        # Ray calculates its initial direction based on its origin point on the board
        self._direction = self.calculate_initial_direction()

        # The ray's current location - Begins at origin, updated on movement iterations
        self._current_row = origin_row
        self._current_column = origin_column

        # The ray's terminus
        self._terminal_row = None
        self._terminal_column = None

        # Whether the terminus of the ray is an atom
        self._atom_terminus = False

        # a color for display on the game board
        self._ray_color = self.generate_color()

    def generate_color(self):
        """generate_color - generates a random color for the ray

        @return: A three digit RGB value
        """
        color_one = random.randint(0,255)
        color_two = random.randint(0,255)
        color_three = random.randint(0,255)

        return int(color_one), int(color_two),  int(color_three)

    def get_color(self):
        """
        get_color - returns self._ray_color
        """

        return self._ray_color

    def get_direction(self):
        """
        get_direction - returns the current direction of the Ray

        :return: A String Representing the Direction
        :rtype: String
        """
        return self._direction

    def set_direction(self, direction):
        """
        set_direction - sets the direction of a ray

        :param direction: "UP", "DOWN", "LEFT" or "RIGHT"
        :type direction: String
        """
        self._direction = direction

    def get_origin_location(self):
        """
        get_origin_location - returns the origin location of a ray

        :return: (origin_row, origin_column)
        :rtype: tuple(int, int)
        """
        return(self._origin_row, self._origin_column)

    def set_current_location(self, location):
        """
        set_current_location - sets the current location of

        :param location: tuple containing the current row and column
        :type location: tuple(int, int)
        """
        self._current_row, self._current_column = location

    def get_current_location(self):
        """
        get_current_location - returns tupe of the current location

        :return: (current_row, current_column)
        :rtype: tuple(int, int)
        """
        return (self._current_row, self._current_column)

    def get_terminal_location(self):
        """
        get_terminal_location - returns the terminal location of a ray

        :return: (row, column) or None
        :rtype: tuple(int, int) or None
        """
        # return None if no terminus has been set or if the terminus is a direct collision with an atom
        if self._terminal_row == None or self._terminal_column == None or self._atom_terminus == True:
            return None
        return (self._terminal_row, self._terminal_column)

    def set_terminal_location(self, location):
        """
        set_terminal_location - set's a node's terminal location

        :param location: tuple of (row, column)
        :type location: tuple(int, int)
        """
        self._terminal_row, self._terminal_column = location

    def reverse(self):
        """
        reverse - reverses the current direction of a ray

        :return: None
        """
        if self._direction == "UP":
            self._direction = "DOWN"
            return

        if self._direction == "DOWN":
            self._direction = "UP"
            return

        if self._direction == "LEFT":
            self._direction = "RIGHT"
            return

        if self._direction == "RIGHT":
            self._direction = "LEFT"
            return

    def calculate_initial_direction(self):
        """
        calculate_initial_direction - returns the initial direction that
        a ray will move based on which edge of the board it is originating
        from

        :return: "UP", "DOWN", "LEFT", "RIGHT"
        :rtype: String
        """
        if self._origin_row == 0:
            return "DOWN"

        if self._origin_row == 9:
            return "UP"

        if self._origin_column== 0:
            return "RIGHT"

        if self._origin_column== 9:
            return "LEFT"

    def get_next_location(self):
        """
        get_next_location - calculates the next point on a ray's trajectory
        based on its current direction.

        :return: tuple containing next point
        :rtype: tuple(int, int)
        """
        if self._direction == "UP":
            return (self._current_row - 1, self._current_column)

        if self._direction == "DOWN":
            return (self._current_row + 1, self._current_column)

        if self._direction == "LEFT":
            return (self._current_row, self._current_column - 1)

        if self._direction == "RIGHT":
            return (self._current_row, self._current_column + 1)


    def record_atom_collision(self, atom_object):
        """
        record_atom_collision - records the collision between a ray and an atom

        :param atom_object: the atom being collided with
        :type atom_object: Object(Square)
        """

        # sets the ray's terminus to the atom (although it is not a proper terminus)
        # for the purposes of data collection
        self.set_terminal_location(atom_object.get_position())

        # set the ray's _atom_terminus to True since we have collided with an atom

        self._atom_terminus = True

        # since the ray has collided it is no longer moving - set motion to None
        self.set_direction(None)

    def record_edge_collision(self, edge_object):
        """
        record_edge_collision - records the collision between a ray and an edge

        :param edge_object: the edge being collided with
        :type edge_object: Object(Square)
        """
        # let the ray know it has hit its terminus
        self.set_terminal_location(edge_object.get_position())

        #  Let the next square know it is the terminus of the current ray
        edge_object.set_terminating_ray(self.get_origin_location())

        # Set the ray's direction to None since it is no longer moving

        self._direction = None

        # return the location of the terminus to the previous function call
        return edge_object.get_position()

    def get_diagonals(self):
        """
        get_diagonals - returns the coordinates of the squares diagonal to
        the current position of the ray (i.e. adjacent to the next position
        in the ray's calculated trajectory).

        :return: (Counter-Clockwise Diagonal Coordinates, Clockwise-Diagonal Coordinates)
        :rtype: tuple(tuple(int, int), tuple(int, int))
        """
        next_location = self.get_next_location()

        if self._direction == "UP" or self._direction =="DOWN":
            ccw_diagonal = (next_location[0], next_location[1] - 1)
            cw_diagonal = (next_location[0], next_location[1] + 1)

        if self._direction == "LEFT" or self._direction == "RIGHT":
            ccw_diagonal = (next_location[0] - 1, next_location[1])
            cw_diagonal = (next_location[0] + 1, next_location[1])

        return (ccw_diagonal, cw_diagonal)

    def recalculate_trajectory(self, ccw_diagonal, cw_diagonal):
        """
        recalculate trajectory - looks at the squares diagonally adjacent
        to the ray's current location and changes the ray's direction based on
        the presence and effect of atoms in those locations.

        :param ccw_diagonal: the square counter clockwise to the current trajectory
        :type ccw_diagonal: Object(Square)
        :param cw_diagonal: the square clockwise from the current trajectory
        :type cw_diagonal: Object(Square)
        """
        #  if both are atoms we're reversed in direction
        if cw_diagonal.is_atom() and ccw_diagonal.is_atom():
            self.reverse()
            return

        if ccw_diagonal.is_atom():
            if self._direction == "UP" or self._direction == "DOWN":
                self._direction = "RIGHT"
                return

            if self._direction == "LEFT" or self._direction == "RIGHT":
                self._direction = "DOWN"
                return

        if cw_diagonal.is_atom():
            if self._direction == "UP" or self._direction == "DOWN":
                self._direction = "LEFT"
                return

            if self._direction == "LEFT" or self._direction == "RIGHT":
                self._direction = "UP"
                return


    def check_for_collision(self, square):
        """
        check_for_collision - checks to see if a ray's movement to a given
        square would result in a collision with either an atom or an edge

        :param square: the square being moved to
        :type square: Object(Square)
        :return: A boolean representing whether a collision will occur
        :rtype: Bool
        """
        # if the next location is the location of an atom we strike it and record the collision
        if square.is_atom():
            self.record_atom_collision(square)
            return True

        # if the next location is another edge we've hit our terminus
        if square.is_edge():
            # return the location of the collision and return its coordinates
            self.record_edge_collision(square)
            return True
