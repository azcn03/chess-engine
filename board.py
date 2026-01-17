from operator import is_
import os
import numpy as np
from uuid import uuid4
from pieces import Pawn, Rook, Bishop, Queen, King, Knight
from util import (
    map_piece_to_character,
    InvalidColumnException,
    InvalidRowException,
)


class BoardBase:
    """
    Base Class for the Chess Board.
    You are free to look around the members of this class and their implementation, however you will not need to change
    anything in this class for any of the tasks.
    """

    def __init__(self):
        """Constructor.
        Start with empty cells
        """
        self.cells = [[None for _ in range(8)] for _ in range(8)]
        self.check_cache = {}

    def __str__(self):
        """
        Returns a nice printable (on console) representation for the current board configuration.
        This is an extended form, meant for readability on console output.
        """
        return "\n".join(
            [
                " ".join([map_piece_to_character(cell) for cell in row])
                for row in reversed(self.cells)
            ]
        )

    def hash(self):
        """
        Returns a unique hash (string) representation for the current board configuration.
        This is short form, not meant for readability.
        """
        return "".join(
            [
                "".join([map_piece_to_character(cell) for cell in row])
                for row in reversed(self.cells)
            ]
        )
    
    def save_to_disk(self, fname = None):
        """
        Saves current board configuration to disk.

        :param name: Filename to use. If None is provided, a unique one will be generated
        """
        if fname is None:
            fname = str(uuid4())

        if '.' not in fname:
            fname += ".board"

        with open(fname, "wt") as f:
            f.write(str(self))

    def clear_board(self):
        """
        Clears to board, deleting all pieces currently placed on it
        """
        self.cells = [[None for _ in range(8)] for _ in range(8)]


    def load_from_memory(self, configString):
        """
        Read previously stored configuration from a memory string

        :param name: Filename to use. 
        """       
        self.cells = [[None for _ in range(8)] for _ in range(8)]

        for row, line in enumerate(configString.split("\n")):
              line = line.strip()
              for col, pieceCode in enumerate(line.split(' ')):
                if pieceCode == '.':
                    continue
                
                if pieceCode.isupper():
                    white = True
                else:
                    white = False

                pieceCode = pieceCode.upper()

                if pieceCode == "P":
                    piece = Pawn(self, white)
                if pieceCode == "K":
                    piece = King(self, white)
                if pieceCode == "Q":
                    piece = Queen(self, white)
                if pieceCode == "N":
                    piece = Knight(self, white)
                if pieceCode == "B":
                    piece = Bishop(self, white)
                if pieceCode == "R":
                    piece = Rook(self, white)

                self.set_cell(np.array([7-row, col]), piece)

    def load_from_disk(self, fname):
        """
        Read previously stored configuration from disk

        :param name: Filename to use. 
        """       

        with open(fname, "rt") as f:
            self.load_from_memory(f.read())
            

    def is_king_check_cached(self, white):
        """
        Calls is_king_check for board configurations not yet known. Caches the result for later look-up.
        """
        # Calculate hash and see if current position is in the cache
        hash = self.hash() + ("-w" if white else "-b")
        if hash in self.check_cache:
            return self.check_cache[hash]

        # No, so evaluate it
        value = self.is_king_check(white)

        # Cache it for later
        self.check_cache[hash] = value
        return value

    def get_cell(self, cell):
        """
        Retrieves the piece placed on the given cell or "None" if cell is invalid
        """
        # If the cell is not valid, there cannot be a piece on it
        if not self.is_valid_cell(cell):
            return None

        # Unpack coordinates
        row, col = cell

        # Return the piece on the cell
        return self.cells[row][col]

    def set_cell(self, cell, piece):
        """
        Places a piece on a given cell.
        """
        # Unpack coordinates
        row, col = cell

        # Check if they are valid, raise an Exception if not
        if row < 0 or row >= 8:
            raise InvalidRowException((row, col))

        if col < 0 or col >= 8:
            raise InvalidColumnException((row, col))

        # If there is a piece to place, there is maintenance stuff to do
        if piece is not None:
            # If the piece has a cell (so it was placed on the board already), set that cell to None
            if piece.cell is not None:
                self.set_cell(piece.cell, None)

            # Update the pieces cell
            piece.cell = np.array([row, col])

        # Update the cell on the board
        self.cells[row][col] = piece

    def reset(self):
        """
        Resets the board to its default (start) configuration
        """
        # Start with all empty cells
        self.cells = [[None for _ in range(8)] for _ in range(8)]

        # Pawns
        for fcol in range(8):
            self.set_cell(np.array([1, fcol]), Pawn(self, True))
            self.set_cell(np.array([6, fcol]), Pawn(self, False))

        # Rooks
        self.set_cell(np.array([0, 0]), Rook(self, True))
        self.set_cell(np.array([0, 7]), Rook(self, True))
        self.set_cell(np.array([7, 0]), Rook(self, False))
        self.set_cell(np.array([7, 7]), Rook(self, False))

        # Knights
        self.set_cell(np.array([0, 1]), Knight(self, True))
        self.set_cell(np.array([0, 6]), Knight(self, True))
        self.set_cell(np.array([7, 1]), Knight(self, False))
        self.set_cell(np.array([7, 6]), Knight(self, False))

        # Bishops
        self.set_cell(np.array([0, 2]), Bishop(self, True))
        self.set_cell(np.array([0, 5]), Bishop(self, True))
        self.set_cell(np.array([7, 2]), Bishop(self, False))
        self.set_cell(np.array([7, 5]), Bishop(self, False))

        # Queen
        self.set_cell(np.array([0, 3]), Queen(self, True))
        self.set_cell(np.array([7, 3]), Queen(self, False))

        # King
        self.set_cell(np.array([0, 4]), King(self, True))
        self.set_cell(np.array([7, 4]), King(self, False))

        #self.save_to_disk()


class Board(BoardBase):
    """
    Your implementation of the chess board. You will need to find implementations for all of these methods. 

    **HINT**: Read the documentation carefully. Also look at the parent class (BoardBase) for further reference and example implementations. 
    """

    def __init__(self):
        """
        Constructor, currently does nothing but calling the super constructor. 

        """
        super().__init__()

    def iterate_cells_with_pieces(self, white):
        """
        **TODO**: Write a generator (using the yield keyword) that allows to iterate
        over all cells with a piece of given color.

        **HINT**: You need a double-nested loop,
        the first one iterates over all the rows, the second one iterates over each cell in the current row.
        If the cell has a piece (so it is not None) and the piece has the correct color, *yield* it

        :param white: True if WHITE pieces are to be iterated, False otherwise
        :type white: Boolean
        """
        # TODO: Implement

        #im konstruktor von boardBase erstellen wir die Zellen mit
        # cells = [[None for _ in range(8)] for _ in range(8)]
        # man Könnte es dynamisch machen mit len() oder man kann einfach range(8) machen


        # range(8) nutzen weil es einfacher ist zu verstehen
        for row in range(8):
            for col in range(8):

                #ich erstelle eine variable um den inhalt von der Zelle zu speichern
                #wir geben row und col als argumente mit
                piece = self.get_cell((row, col)) 

                #jetzt überprüfen wir einfach ob das piece das wir erhalten haben nicht None ist
                #und wegen dem AND schaut der sich die zweite bedingung nur an wenn die erste True ist
                #und nur dann schauen wir ob das piece was wir bekommen haben die gleiche farbe hat wie der paramter in der funktion 
                if piece is not None and piece.white == white:
                    #wenn es so ist yielde das piece 
                    yield piece

        

    def find_king(self, white):
        """
        **TODO**: Find the king piece of given color and return that piece

        **HINT**: You can use the iterate_cells_with_pieces() Method to find all
        pieces of a given color

        :param white: True if WHITE pieces are to be iterated, False otherwise
        :type white: Boolean

        :return: The :py:class:'King': object of the given color or None if there is no King on the board.
        """
        # TODO: Implement

        #PLAN
        # 1. nutze die iterate_cells_with_pieces() methode um alle teile der gegebenen farbe zu bekommen 
        # 2. checke ob das piece von der klasse King ist
 
        for piece in self.iterate_cells_with_pieces(white):
            # isinstance gibt true oder false zurück, ob die gegebene Instanze von der Klasse King ist
            if isinstance(piece, King):
                #dann returne das Piece
                return piece
            
        #und falls er kein König findet gibt er None zurück
        #ja wir wissen das wenn eine Funktion nichts Returned, None als Rückgabewert hat
        #aber ums besser zu verstehen
        return None


    def is_king_check(self, white):
        """
        **TODO**: Evaluate if the king of given color is currently in check.
        A check is given if any opposing piece can beat the king in its next move.

        **HINT**: You can use the find_king() Method to find the king of the given color.
        Then use the iterate_cells_with_pieces Method to find all pieces of *opposing color* (negate the "white"-parameter)
        For each opposing piece, call the "get_reachable_cells()" method to get a list of all reachable cells.
        Iterate over each reachable cell and check if the kings cell is reachable. If yes, shortcut and return True right away.
        """
        # TODO: Implement

        # Finds the king of a given color (white=True or False)
        position_king = self.find_king(white)

        # Unpack the tuple of the kings cell
        king_row, king_col = position_king.cell

        # Iterates over the board and returns every piece of the opposing color
        for piece in self.iterate_cells_with_pieces(not white):
            # Iterates over every reachable cell of the piece
            for reachable_cell in piece.get_reachable_cells():
                # Unpacks the pieces position (cell)
                piece_row, piece_col = reachable_cell
                # Checks if the opposing piece can hit the king
                if piece_row == king_row and piece_col == king_col:
                    # If so return False, because it shouldn't be possible
                    return True 
        # If the king isn't in check, return False
        return False
            


    def evaluate(self):
        """
        **TODO**: Evaluate the current board configuration into a numerical number.
        The higher the number, to more favorable for WHITE (note: This is always from whites perspective!) the current configuration is.


        **HINT**: Start with a score of zero.
        Use the iterate_cells_with_pieces Method to find all WHITE pieces and call their respective "evaluate" Method. Sum those scores up.
        Then use the iterate_cells_with_pieces Method to find all BLACK pieces, call their respective "evaluate" Method and substract that from the score.
        """
        # TODO: Implement
        
        # Starting Score
        score = 0.0

        # Iterates over the board and returns every white piece
        for piece in self.iterate_cells_with_pieces(True):
            # Adds the value for every white piece
            score += piece.evaluate()
        
        for piece in self.iterate_cells_with_pieces(False):
            # Subtracts the value for every black piece
            score -= piece.evaluate()

        return score

    def is_valid_cell(self, cell):
        """
        **TODO**: Check if the given cell coordinates are valid. A cell coordinate is valid if both
        row and coloumn are between 0 and 7 inclusively.

        **HINT**:
        Cell is a tuple (row, col) of row and column. Unpack the tuple and check both row and col for
        being within the allowed range (0 to 7 inclusively).
        Don´t forget to handle the special case of "cell" being None. Return False in that case
        """
        # TODO: Implement

        #https://stackoverflow.com/questions/9494404/use-of-true-false-and-none-as-return-values-in-python-functions
        
        #Wenn die Zelle None ist, gebe False zurück 
        #sobald man in einer funktion return aufruft beendet es die funktion 
        if cell is None:
            return False
        
        #wir unpacken cell in row und col
        row, col = cell 

        
        #https://stackoverflow.com/questions/13628791/determine-whether-integer-is-between-two-other-integers
        #Wenn 0 kleiner oder gleich row ist UND row kleiner oder gleich 7
        #UND 0 kleiner oder gleich col UND col kleiner oder gleich 7 ist gebe True zurück

        #Es ist lesbarer deshalb so gemacht
        if 0 <= row <= 7 and 0 <= col <= 7:
            return True
        
        #Wenn die Bedinung oben nicht ausgelöst wurde sind wir jetzt hier
        #das heißt in jedem anderen Fall geben wir False zurück
        return False


    def cell_is_valid_and_empty(self, cell):
        """
        **TODO**: Check if the given cell is empty, meaning there is no piece placed on it.

        **HINT**:
        You can use the "is_valid_cell()" Method to verify the cell is valid in the first place.
        If so, use "get_cell()" to retrieve the piece placed on it and return True if there is None
        """
        # TODO: Implement

        #"get_cell()" returns the element of the given coordinates
        #In the Constructor of the Class BoardBase every cell is initialized with the Value None, so an "Empty" cell has the Value None
        #That's why we check if it is "None"

        #wir brauchen self. weil wir so auf die funktionen von der gleichen klasse zugreifen können
        #wir nutzen hier auch das logische AND, also checkt er bedingung 1 und wenn das False ist
        #bricht er direkt ab weil die gesamt bedingung garnicht mehr wahr werden kann

        # Wenn die Cell eine Valide cell ist UND die cell None ist 
        #(was in diesem schachbrett bedeutet das keine Figur drauf ist) 
        #dann gebe true zurück
        if self.is_valid_cell(cell) and self.get_cell(cell) is None:
            return True
            
        #in jedem anderen fall gebe False zurück
        return False

    def piece_can_enter_cell(self, piece, cell):
        """
        Either Empty or Enemy (with valid cell)

        **TODO**: Check if the given piece can enter the given cell.
        Note: You don´t need to check movement rules for the individual piece here. You only need to answer the question
        whether the piece can be placed on the given cell or not.

        A piece can be placed on a cell if the cell is valid and either empty or an opposing piece is placed here.
        A cell cannot be entered if a piece of the same color is already in that cell.

        **HINT**:
        You can use the "is_valid_cell()" Method to verify the cell is valid in the first place.
        If so, use "get_cell()" to retrieve the piece placed on it. If there is None, this cell can be entered
        If, however, there is another piece, it must be of opposing color. Check the other pieces "white" attribute and compare against
        the given piece "white" attribute.
        """
        # TODO: Implement

        #Wenn die Cell valide ist 
        if self.is_valid_cell(cell):
                
            #und wenn die cell none ist (also es ist leer)
            #oder die zelle wo wir hinwollen hat eine andere farbe 
            #als die farbe von dem piece das wir mitgeben
            if self.get_cell(cell) is None or self.get_cell(cell).is_white() != piece.is_white():
                #dann gebe wahr zurück
                return True
            
        #in jedem anderen fall gebe false zurück
        return False


    def piece_can_hit_on_cell(self, piece, cell):
        """
        Enemy is on the cell

        **TODO**: Check if the given piece can *hit* at the given cell.
        Note: You don´t need to check movement rules for the individual piece here. You only need to answer the question
        whether the piece can be placed on the given cell or not and hit an opposing piece.

        A piece can hit on a cell if the cell is valid and an opposing piece is placed here.
        A cell cannot be hit if the cell is empty or a piece of the same color is already in that cell.

        **HINT**:
        You can use the "is_valid_cell()" Method to verify the cell is valid in the first place.
        If so, use "get_cell()" to retrieve the piece placed on it. If there is None, this cell cannot be hit.
        If, however, there is another piece, it must be of opposing color. Check the other pieces "white" attribute and compare against
        the given piece "white" attribute.
        """
        # TODO: Implement
        
        #wenn die cell valide ist
        if self.is_valid_cell(cell):
            #und die cell None (also leer)
            if self.get_cell(cell) is None:
                #gebe false zurück
                return False
            
            #oder wenn die cell eine andere farbe hat als das piece das wir haben
            if self.get_cell(cell).is_white() != piece.is_white():
                #dann gebe true zurück
                return True
            
        #in allen anderen fällen gebe false zurück
        return False
