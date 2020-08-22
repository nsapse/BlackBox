class Square():
    """
    Square - a class representing an individual cell on the board. All that is needed to
    instantiate an instance of square is a set of row and column coordinates.

    Although a square does not need to know anything other than its placement when intiated
    it will interact with rays and the board frequently and as a result it will be able to
    deduct from its coordinates whether or not it is an "edge" where rays can be fired. If a
    ray is fired from it then it will know where that ray begins or terminates at it
    although it will be reliant on the ray to provide that information to it. Keeping track of this information is likely unnecessary
    for the project but will be helpful in allowing for the code to be expanded on later to create a
    GUI.

    A square also know whether or not it contains an atom, which it is told by the Board during
    its instantiation.


    """
    def __init__(self, row, column):
        """
        __init__ initiates an instance of the Square Class

        :param row: an integer representing a row
        :type row: int
        :param column: an integer representing a column
        :type column: int
        """
        self._row = row
        self._column = column
        self._selected = False

        # Whether the square is an "edge" from which a ray can be launched
        self._edge = self.is_edge()

        #  Whether or not an atom is placed on the square
        self._atom = False

        # Whether or not a ray has originated from the square
        # False if no - points towards Ray object if yes
        self._originating_ray = False

        # Whether or not a ray has terminated on the square. Defaults to False
        # Contains tuple of origin of the terminating ray if one exists.
        self._terminating_ray = False

    def get_position(self):
        """
        get_position - returns the position (row and column) of the square

        :return: [row, column]
        :rtype: list[int, int]
        """
        return [self._row, self._column]
    
    def get_originating_ray(self):
        """get_originating_ray - returns the ray (if any) which originated from this location"""
        return self._originating_ray

    def set_originating_ray(self, ray):
        """set_originating_ray - sets the set_originating_ray property"""

        self._originating_ray = ray
        
    def get_terminating_ray(self):
        """
        get_terminating_ray - returns the origin of any ray terminating at the square
        :return: a tuple repsenting the origin of a terminating ray
        :rtype: tuple(int, int)
        """
        return self._terminating_ray

    def set_terminating_ray(self, location):
        """
        set_terminating_ray - Records that a ray terminates at the square

        :param location: tuple containing the location parameters
        :type location: tuple(int, int)
        """
        self._terminating_ray = location

    def is_edge(self):
        """
        is_edge - returns whether or not the square is an "edge" of the board from
        which a ray can be shot

        :return: Bool
        """
        if self._row == 0 or self._row == 9 or self._column == 0 or self._column == 9:
            # check that the edge is not actually a corner square
            if not self.is_corner():
                # If not a corner and in a border row return True
                return True

        return False
    
    def is_corner(self):
        # supplemental check  to make sure that origin square is not a corner square
        if self._row == 0 and self._column == 0:
            return True

        if self._row == 0 and self._column == 9:
            return True

        if self._row == 9 and self._column == 0:
            return True

        if self._row == 9 and self._column == 9:
            return True

    def set_atom(self, status):
        """
        set_atom - sets the status of a square regarding containing an atom

        :param status: Bool
        """
        self._atom = status

    def is_atom(self):
        """
        is_atom - returns a Bool indicating whether or not a square contains an atom

        :return: Bool
        """
        return self._atom
    
    def is_selected(self):
        """
        is_selected - returns whether or not a square is currently selected

        :return: Bool
        """
        return self._selected

    def toggle_selected(self):
        """
        toggle_selected - toggles the current value of a square's _selected property
        """

        self._selected = not self._selected
