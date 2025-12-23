import numpy as np

class Piece:
    """
    Base class for pieces on the board. 
    
    A piece holds a reference to the board, its color and its currently located cell.
    In this class, you need to implement two methods, the "evaluate()" method and the "get_valid_cells()" method.
    """
    def __init__(self, board, white):
        """
        Constructor for a piece based on provided parameters

        :param board: Reference to the board this piece is placed on
        :type board: :ref:class:`board`
        """
        self.board = board
        self.white = white
        self.cell = None



    def is_white(self):
        """
        Returns whether this piece is white

        :return: True if the piece white, False otherwise
        """
        return self.white

    def can_enter_cell(self, cell):
        """
        Shortcut method to see if a cell on the board can be entered.
        Simply calls :py:meth:`piece_can_enter_cell <board.Board.piece_can_enter_cell>` from the current board class.

        :param cell: The cell to check for. Must be a unpackable (row, col) type.
        :return: True if the provided cell can enter, False otherwise
        """
        return self.board.piece_can_enter_cell(self, cell)

    def can_hit_on_cell(self, cell):
        """
        Shortcut method to see if this piece can hit another piece on a cell.
        Simply calls :py:meth:`piece_can_hit_on_cell <board.Board.piece_can_hit_on_cell>` from the current board class.

        :param cell: The cell to check for. Must be a unpackable (row, col) type.
        :return: True if the piece can hit on the provided cell, False otherwise
        """
        return self.board.piece_can_hit_on_cell(self, cell)

    def evaluate(self):
        """
        **TODO** Implement a meaningful numerical evaluation of this piece on the board.
        This evaluation happens independent of the color as later, values for white pieces will be added and values for black pieces will be substracted. 
        
        **HINT** Making this method *independent* of the pieces color is crucial to get a *symmetric* evaluation metric in the end.
         
        - The pure existance of this piece alone is worth some points. This will create an effect where the player with more pieces on the board will, in sum, get the most points assigned. 
        - Think of other criteria that would make this piece more valuable, e.g. movability or whether this piece can hit other pieces. Value them accordingly.
        
        :return: Return numerical score between -infinity and +infinity. Greater values indicate better evaluation result (more favorable).
        """
        # TODO: Implement
        
        #SOURCES:
        # https://www.chessprogramming.org/Point_Value
        # https://www.chessprogramming.org/Evaluation_of_Pieces
        # https://www.chessprogramming.org/Point_Value#Basic_values, Larry Kaufmann 2012
        # https://www.chessprogramming.org/Piece-Square_Tables for position
        # https://www.chessprogramming.org/Material
        # https://www.chessprogramming.org/Simplified_Evaluation_Function


        #PLAN

        #Get the Material worth from: 
        # 1. Get The existence of the piece, the instance of it and add points (would recommend larger numbers for finer evaluation
        # 2. Get the position of it, 
        # 3. evaluate further with more methods from chessprograming.com

        #Implement the following:
        #Bonus for the bishop pair (bishops complement each other, controlling squares of different color)
        # Penalty for the rook pair (Larry Kaufman called it "principle of redundancy")
        # Penalty for the knight pair (as two knights are less successful against the rook than any other pair of minor pieces)
        # decreasing the value of the rook pawns and increasing the value of the central pawns (though this can be done in the piece-square tables as well)
        # Trade down bonus that encourages the winning side to trade pieces but no pawns [3]
        # Penalty for having no pawns, as it makes it more difficult to win the endgame
        # Bad trade penalty as proposed by Robert Hyatt, that is penalizing the material imbalances that are disadvantageous like having three pawns for a piece or a rook for two minors.
        # Elephantiasis effect as suggested by Harm Geert Muller (meaning that stronger pieces lose part of their value in presence of weaker pieces)
        #I think Multiple if statements would be the best, because i have to implement a lot of different rules for every single one of them
        

        # TODO 
        # Adjust the positional values accordingly to white and black
        pawn_pos = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5,  5],
        [0,  0,  0, 20, 20,  0,  0,  0],
        [5, -5,-10,  0,  0,-10, -5,  5],
        [5, 10, 10,-20,-20, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]]

        rook_pos = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [0,  0,  0,  5,  5,  0,  0,  0]]

        knight_pos = [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]]

        bishop_pos = [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]]

        queen_pos = [
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [-5,  0,  5,  5,  5,  5,  0, -5],
        [0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]]

        king_pos_middle_game = [
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [20, 20,  0,  0,  0,  0, 20, 20],
        [20, 30, 10,  0,  0, 10, 30, 20]]

        king_pos_end_game = [
        [-50,-40,-30,-20,-20,-30,-40,-50],
        [-30,-20,-10,  0,  0,-10,-20,-30],
        [-30,-10, 20, 30, 30, 20,-10,-30],
        [-30,-10, 30, 40, 40, 30,-10,-30],
        [-30,-10, 30, 40, 40, 30,-10,-30],
        [-30,-10, 20, 30, 30, 20,-10,-30],
        [-30,-30,  0,  0,  0,  0,-30,-30],
        [-50,-30,-30,-30,-30,-30,-30,-50]]

        

        if isinstance(self, Pawn):
            self_value = 100
            row , col = self.cell
            cell_value = pawn_pos[row][col]

        elif isinstance(self, Rook):
            self_value = 525
            row , col = self.cell
            cell_value = rook_pos[row][col]

        elif isinstance(self, Knight):
            self_value = 350
            row , col = self.cell
            cell_value = knight_pos[row][col]
    
        elif isinstance(self, Bishop):
            self_value = 350
            row , col = self.cell
            cell_value = bishop_pos[row][col]

        elif isinstance(self, Queen):
            self_value = 1000
            row , col = self.cell
            cell_value = queen_pos[row][col]

        elif isinstance(self, King):
            self_value = 20000#got the value of 20000 from:
            row , col = self.cell
            cell_value = king_pos_middle_game[row][col]

        return self_value 

            


    def get_valid_cells(self):
        """
        **TODO** Return a list of **valid** cells this piece can move into. 
        
        A cell is valid if 
          a) it is **reachable**. That is what the :py:meth:`get_reachable_cells` method is for and
          b) after a move into this cell the own king is not (or no longer) in check.

        **HINT**: Use the :py:meth:`get_reachable_cells` method of this piece to receive a list of reachable cells.
        Iterate through all of them and temporarily place the piece on this cell. Then check whether your own King (same color)
        is in check. Use the :py:meth:`is_king_check_cached` method to test for checks. If there is no check after this move, add
        this cell to the list of valid cells. After every move, restore the original board configuration. 
        
        To temporarily move a piece into a new cell, first store its old position (self.cell) in a local variable. 
        The target cell might have another piece already placed on it. 
        Use :py:meth:`get_cell <board.BoardBase.get_cell>` to retrieve that piece (or None if there was none) and store it as well. 
        Then call :py:meth:`set_cell <board.BoardBase.set_cell>` to place this piece on the target cell and test for any checks given. 
        After this, restore the original configuration by placing this piece back into its old position (call :py:meth:`set_cell <board.BoardBase.set_cell>` again)
        and place the previous piece also back into its cell. 
        
        :return: Return True 
        """
        # TODO: Implement

        #GOAL:
        #IF i understood correctly
        # 1. We have to take all the possible positions a pice can do within the next move
        # 2. place that piece on every one of those positions 
        # 2.1. (we might could optimize and cut off branches with the same direction E.g. the rook isn't allowed to move to the right at all)
        # 3. See if the King is checked if Piece is on that position
        # 4. based on 3. either add it to the list or don't
        # 5. restore board to it's original state
        #PLAN
        # 1. Create an empty list which we will return in the end
        # 2. get all reachable cells
        # 3. safe the initial position of the piece
        # 4. before you loop over all possible positions, safe the piece which stands on the goal_cell and it's position (indirectly the goal cell)
        # 5. loop, add or not, reset again then return


        valid_cells = []

        #We get all reachable cells as a list
        reachable_cells = self.get_reachable_cells()

        #We safe the initial position of the piece we wanna move
        initial_position = self.cell

        #possible_position will be a tuple, we iterate over a list with tuples
        for possible_position in reachable_cells:

            #safe the piece that is on the cell we wanna go to
            local_piece = self.board.get_cell(possible_position)
            #set OUR piece on that cell
            self.board.set_cell(possible_position, self)

            #check if king is in check, but we inverese it
            #so only if king is NOT in check we append that position to the list
            if not self.board.is_king_check_cached(self.white):
                valid_cells.append(possible_position)

            #After the if, which will ALWAYS happen, we FIRST set out piece back to it's original place
            self.board.set_cell(initial_position, self)
            #THEN SECOND we place the old piece on the position we checked
            self.board.set_cell(possible_position, local_piece)

        return valid_cells
                   

class Pawn(Piece):  # Bauer
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanik for `pawns <https://de.wikipedia.org/wiki/Bauer_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Pawns can move only forward (towards the opposing army). Depening of whether this piece is black of white, this means pawn
        can move only to higher or lower rows. Normally a pawn can only move one cell forward as long as the target cell is not occupied by any other piece. 
        If the pawn is still on its starting row, it can also dash forward and move two pieces at once (as long as the path to that cell is not blocked).
        Pawns can only hit diagonally, meaning they can hit other pieces only the are one cell forward left or one cell forward right from them. 

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the pawn movability mechanics. 

        **NOTE**: For all you deep chess experts: Hitting `en passant <https://de.wikipedia.org/wiki/En_passant>`_ does not need to be implemented.
        
        :return: A list of reachable cells this pawn could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move

        #The indices of the Board are [0-7] [0-7] if it's White the pawn's Home row will be [1] and for black [6]
        #so the only direction which is allowed is into the respective other direction of it's own color (black is -1 , white is +1) of the first index (in that case row)

        reachable_cells = []

        #By implementing a set direction we don't need to repeat ourselves for black and white, would generally recommend to differentiate at start
        #https://stackoverflow.com/questions/14461905/python-if-else-short-hand
        #this was combined with tuple unpacking 
        #https://www.w3schools.com/python/python_tuples_unpack.asp
        #"direction" and "home_row" are (1, 1) if it's white, else (the only other case is black) it's (-1, 6) 

        direction, home_row = (1, 1) if self.white else (-1, 6)

        (row, col) = self.cell

        one_step = (row + direction, col)
        #row + direction because 5 + 1 = 6 and 5 + (-1) is 4 so it's fine
        if self.board.cell_is_valid_and_empty(one_step):
            reachable_cells.append(one_step)

            #Now we Check if Dash(2 cells at once) is even possible
            #The cell right infront is free because we checked it earlier, now we check if the second cell is also free and if the pawn is in his homerow 
            two_steps = (row + direction * 2, col)
            if row == home_row and self.board.cell_is_valid_and_empty(two_steps):
                reachable_cells.append(two_steps)

        for value in [1, -1]:
            attack = (row + direction, col + value)
            #You need self as the first argument because that's the piece you want to move
            if self.board.piece_can_hit_on_cell(self, attack):
                reachable_cells.append(attack)

        return reachable_cells


# We can also do it like that but we would unnecessarily repeat our selves (and for other pieces with more possibilities we can't copy paste the code 10 or more times)
            #  #Now we SEPERATELY check if pawn can attack his diagonal fields
            # #The multiple if's are on purpose!!!
            # if self.board.piece_can_hit_on_cell(self, (row + direction, col -1)):
            #     reachable_cells.append((row + direction, col -1))
            # if self.board.piece_can_hit_on_cell(self, (row + direction, col +1)):
            #     reachable_cells.append((row + direction, col +1))
        

        # A bit easier to understand implementation of the same code
        # reachable_cells = []

        # #To know where the pawn will be able to move we first need it's current position
        # (row, col) = self.cell
        

        # #1. Check Color, because self.white is a Boolean we can use it as a condition and if's not True it will be False so we just need an else
        # if self.white:
        #     #2. Now we check if the cell right infront of the Pawn is free and if so we append that cell as a possible one
        #     if self.board.cell_is_valid_and_empty((row - 1, col)):
        #         reachable_cells.append((row - 1, col))

        #         #Now we Check if Dash(2 cells at once) is even possible
        #         #The cell right infront is free because we checked it earlier, now we check if the second cell is also free and if the pawn is in his homerow 
        #         if row == 6 and self.board.cell_is_valid_and_empty((row - 2, col)):
        #             reachable_cells.append((row - 2, col))

        #     #If white we SEPERATELY check if can attack his diagonal fields
        #     #The multiple if's are on purpose
        #     if self.board.piece_can_hit_on_cell(self, (row - 1, col -1)):
        #         reachable_cells.append((row - 1, col -1))
        #     if self.board.piece_can_hit_on_cell(self, (row - 1, col +1)):
        #         reachable_cells.append((row - 1, col +1))
        
        # #Same as for White one but instead of Homerow 6 it's 1 and his "Forward" is + 1 while white's was -1
        # else:
        #     #See if Cell infront is free and add to list
        #     if self.board.cell_is_valid_and_empty((row + 1, col)):
        #         reachable_cells.append((row + 1, col))
                
        #         #Check if it's the Homerow, if so and Free -> add to list
        #         if row == 1 and self.board.cell_is_valid_and_empty((row + 2, col)):
        #             reachable_cells.append((row + 2, col))

        #     # Again Check Seperately if pawn can hit diagonally
        #     if self.board.piece_can_hit_on_cell(self, (row + 1, col -1)):
        #         reachable_cells.append((row + 1, col -1))
        #     if self.board.piece_can_hit_on_cell(self, (row + 1, col +1)):
        #         reachable_cells.append((row + 1, col +1))

        # return reachable_cells

class Rook(Piece):  # Turm
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for `rooks <https://de.wikipedia.org/wiki/Turm_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Rooks can move only horizontally or vertically. They can move an arbitrary amount of cells until blocked by an own piece
        or an opposing piece (which they could hit and then being stopped).

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this rook could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move

        #PLAN:
        #1. Rook can move horizontally and vertically so 4 directions
        #2. I will implement this with a list of those 4 directions E.g. (1, 0)
        #3. 
        #3. Now go one step in the given direction and check for
        #       -if cell is empty and valid then repeat and add one step
        #       -if the cell isn't empty check if it's an opponent then add that step and stop that direction because you can't go through an opponent 


        #Implementation 

        reachable_cells = []

        (row, col) = self.cell

        # Here is the list of his Directions 
        direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        #Unpack the tuple's from the list in j and k
        for j, k in direction:
            #add the current position they are in to the possible direction once
            new_cell = (row + j, col + k) #3 and 3 then it will become 4 and 3 for E.g. with the first tuple from the list (1, 0)
            
            #while it's empty move forward
            while self.board.cell_is_valid_and_empty(new_cell):
                reachable_cells.append(new_cell)
                #unpack tuple so we know where on the board we are
                (new_row, new_col) = new_cell
                #add the direction we are going toward again E.g. (1, 1) and save in new cell
                new_cell = (new_row + j, new_col + k)
            
            #if we are here the next cell wasn't empty, so we check if it's an opponent
            #if so add that cell once to the list, then return to the start of the for loop and do all that again with E.g.(1, -1)
            if self.board.is_valid_cell(new_cell) and self.board.piece_can_hit_on_cell(self, new_cell):
                reachable_cells.append(new_cell)

        return reachable_cells


        #More beginner way
        # #The indices of the Board are [0-7] [0-7], 
        # #the Rook's are allowed to move in every axis (+1/-1) multiple times as long as cell is valid and empty
        # #if own color there then stop one cell before that
        # #if oponent color there include that cell (sounds a bit like list slicing, might try it with that)

        # #Need to optimize code, DRY concept and readability, this basically just a mockup
        # reachable_cells = []

        # directions = [1, -1] 

        # (row, col) = self.cell
        
        # for direction in directions:
        #     steps = 1
        #     #for positive direction
        #     if direction > 0:
        #         #take current position and add 1 in row see if its possible
        #         while self.board.cell_is_valid_and_empty((row + steps, col)):
        #             reachable_cells.append((row + steps, col))
        #             steps += 1
        #         if(self.board.piece_can_hit_on_cell(self, (row + steps, col))):
        #             reachable_cells.append((row + steps, col))

        #     else:
        #         steps *= -1
        #         while self.board.cell_is_valid_and_empty((row + steps, col)):
        #             reachable_cells.append((row + steps, col))
        #             steps -= 1
        #         if(self.board.piece_can_hit_on_cell(self, (row + steps, col))):
        #             reachable_cells.append((row + steps, col))

        # for direction in directions:
        #     steps = 1
        #     if direction > 0:
        #         while self.board.cell_is_valid_and_empty((row, steps + col)):
        #             reachable_cells.append((row, steps + col))
        #             steps += 1
        #         if(self.board.piece_can_hit_on_cell(self, (row, steps + col))):
        #             reachable_cells.append((row, steps + col))
        #     else:
        #         steps *= -1
        #         while self.board.cell_is_valid_and_empty((row, steps + col)):
        #             reachable_cells.append((row, steps + col))
        #             steps -= 1
        #         if(self.board.piece_can_hit_on_cell(self, (row, steps + col))):
        #             reachable_cells.append((row, steps + col))

        # return reachable_cells


class Knight(Piece):  # Springer
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for `knights <https://de.wikipedia.org/wiki/Springer_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Knights can move in a special pattern. They can move two rows up or down and then one column left or right. Alternatively, they can
        move one row up or down and then two columns left or right. They are not blocked by pieces in between. 

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this knight could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move

        # PLAN:
        #1. Knight only has 8 possible moves, i will create a list of those 8 moves
        #2. Go trough every move and see if either the cell they wanna go to is empty OR an opposing piece is there (that the cells are valid is already assumed)
        #3. Return the list of those moves

        reachable_cells = []
        (row, col) = self.cell
        
        #Because the Knight moves in 2 in one directions 1 in the other those are the 8 possibilities
        possible_moves = [(2, 1), (2, -1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (1,-2), (-1,-2)]

        for j, k in possible_moves:
            #We save the new Position in "new_cell"
            new_cell = (row + j, col + k)
            #We use the method "piece_can_enter_cell", because it perfectly catches the case of
            #Either the new Cell has to be empty or an opposing piece has to be there
            if self.board.piece_can_enter_cell(self, new_cell):
                reachable_cells.append(new_cell)        
       
        return reachable_cells

    
class Bishop(Piece):  # Läufer
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for `bishop <https://de.wikipedia.org/wiki/L%C3%A4ufer_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Bishops can move diagonally an arbitrary amount of cells until blocked.

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this bishop could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move

        #PLAN:
        #1. Bishop can move diagonally in 4 directions, which is one of the moves of the list below "direction" but multiple times
        #2. I will implement this in a list with tuples and increase both elements with one after every turn 
        #3. Now go one step diagonally and check for
        #       -if cell is empty and valid then repeat and add one step
        #       -if the cell isn't empty check if it's an opponent then add that step and stop that direction because you can't go through an opponent 

        #Implementation 
        reachable_cells = []
        (row, col) = self.cell

        # Here is the list of his Directions
        direction = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        #Unpack the tuple's from the list in j and k
        for j, k in direction:
            #add the current position they are in to the possible direction once
            new_cell = (row + j, col + k) #3 and 3 then it will become 4 and 4 for E.g. with the first tuple from the list (1, 1)
            
            #while it's empty move forward
            while self.board.cell_is_valid_and_empty(new_cell):
                reachable_cells.append(new_cell)
                #unpack tuple so we know where on the board we are
                (new_row, new_col) = new_cell
                #add the direction we are going toward again E.g. (1, 1) and save in new cell
                new_cell = (new_row + j, new_col + k)
            
            #if we are here the next cell wasn't empty, so we check if it's an opponent
            #if so add that cell once to the list, then return to the start of the for loop and do all that again with E.g.(1, -1)
            if self.board.piece_can_hit_on_cell(self, new_cell):
                reachable_cells.append(new_cell)
        
        return reachable_cells


class Queen(Piece):  # Königin
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for the `queen <https://de.wikipedia.org/wiki/Dame_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Queens can move horizontally, vertically and diagonally an arbitrary amount of cells until blocked. They combine the movability
        of rooks and bishops. 

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this queen could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move

        #PLAN:
        #1. Queen Basically is a rook and bishop at the same time, just adjust the directios
        #2. I will implement this in a list with tuples and increase both elements with one after every turn 
        #3. Now go one step into direction and check for
        #       -if cell is empty and valid then repeat and add one step
        #       -if the cell isn't empty check if it's an opponent then add that step and stop that direction because you can't go through an opponent 

        #Implementation 
        reachable_cells = []
        (row, col) = self.cell

        # Here is the list of his Directions
        direction = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]


        #Unpack the tuple's from the list in j and k
        for j, k in direction:
            #add the current position they are in to the possible direction once
            new_cell = (row + j, col + k) #3 and 3 then it will become 4 and 4 for E.g. with the first tuple from the list (1, 1)
            
            #while it's empty move forward
            while self.board.cell_is_valid_and_empty(new_cell):
                reachable_cells.append(new_cell)
                #unpack tuple so we know where on the board we are
                (new_row, new_col) = new_cell
                #add the direction we are going toward again E.g. (1, 1) and save in new cell
                new_cell = (new_row + j, new_col + k)
            
            #if we are here the next cell wasn't empty, so we check if it's an opponent
            #if so add that cell once to the list, then return to the start of the for loop and do all that again with E.g.(1, -1)
            if self.board.piece_can_hit_on_cell(self, new_cell):
                reachable_cells.append(new_cell)
        
        return reachable_cells


class King(Piece):  # König
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for the `king <https://de.wikipedia.org/wiki/K%C3%B6nig_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Kings can move horizontally, vertically and diagonally but only one piece at a time.

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this king could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move
        #PLAN:
        #1. King is Basically a rook and bishop at the same time, but can just move once in every direction
        #2. I will implement this in a list with tuples and could add the knight logic
        #3. Now go one step into direction and check for
        #       -if cell is empty and valid then repeat and add one step
        #       -if the cell isn't empty check if it's an opponent then add that step and stop that direction because you can't go through an opponent 

        #Implementation 
        reachable_cells = []
        (row, col) = self.cell

        # Here is the list of his Directions
        possible_moves = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]

        # unpack the tuple
        for j, k in possible_moves:
            #We save the new Position in "new_cell"
            new_cell = (row + j, col + k)
            #We use the method "piece_can_enter_cell", because it perfectly catches the case of
            #Either the new Cell has to be empty or an opposing piece has to be there
            if self.board.piece_can_enter_cell(self, new_cell):
                reachable_cells.append(new_cell)        
        return reachable_cells