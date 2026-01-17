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
                       
        score = 0.0
        #Dictionary mit entsprechenden werten für die Figuren
        existance_score = {
            King: 99999,
            Pawn: 1,
            Knight: 3,
            Bishop: 3,
            Rook: 5,
            Queen: 9
        }
        
        #addiere auf den score den value von
        #type(self) schaut welcher type das piece hat, bei einem König wäre es King
        #das wird zu seinem Key und der Value ist dann 99999
        score += existance_score[type(self)]
        
        #Zentrum gibt zusatzpunkte
        middle = [3, 4]
        #für alle move die man durch get_valid_cells() zurück bekommt
        for move in self.get_valid_cells():
            #für jedes mal wenn man ein anderes piece schlagen kann füge 0.25 hinzu
            if self.can_hit_on_cell(move): # Checks wheter this piece can hit other pieces
                score += 0.25
            
            #und ob man das zentrum angreifen kann
            #wenn das tupel move in index 0 und 1 die mitte hat (also 3 und 4)
            if move[0] in middle and move[1] in middle: # Checks if piece controls the middle part 
                #füge 0.4 hinzu
                score += 0.4

            #und füge 0.25 für jeden move den man überhaupt machen kann hinzu
            score += 0.25
        
        return score

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

        # Erstelle eine leere liste
        valid_cells = []

        # hol dir alle zellen wo ein piece hingehen kann
        reachable_cells = self.get_reachable_cells()

        # speichere die initial position von dem piece um das board später wiederherzustellen
        initial_position = self.cell 
        
        # gehe durch jeden möglichen move
        for potential_move in reachable_cells:
            #speichere die figure auf der cell wo wir hinwollen,
            #um es später wieder dahin zu machen 
            target_cell_content = self.board.get_cell(potential_move)
            # setzt das piece auf den potenziellen move um zu schauen 
            # ob der eigene König im schach liegt
            self.board.set_cell(potential_move, self)
            
            # Wenn der eigene König nicht im Schach liegt
            # dann ist der move valide
            if not self.board.is_king_check_cached(self.white):
                # füge den move der liste hinzu
                valid_cells.append(potential_move)

            # das brett wieder in sein ursprungszustand versetzen
            self.board.set_cell(initial_position, self)
            self.board.set_cell(potential_move, target_cell_content)
        
        # returned alle moves wo der eigene könig nicht im schach ist 1
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

        #Die Index auf dem Board sind [0-7] und [0-7]
        #Wenn Die Figur Weiß ist, ist die "Home Row" [1] und bei Schwarz [6] (board.py, Klasse BoardBase, Methode Reset, ca Zeile 180)
        
        #Und beim Bauern ist die Einzige erlaubte Richtung, vorwärts
        #Für Weiß also +1 und schwarz -1

        # [
        # [_,_,_,_,_,_,_,_]
        # [w,w,w,w,w,w,w,w] nach unten 
        # [_,_,_,_,_,_,_,_]
        # [_,_,_,_,_,_,_,_]
        # [_,_,_,_,_,_,_,_]
        # [_,_,_,_,_,_,_,_]
        # [b,b,b,b,b,b,b,b] nach oben
        # [_,_,_,_,_,_,_,_]
        # ]
        

        #wir erstellen eine leere liste wo wir gleich die felder hinzufügen werden
        reachable_cells = []

        if self.is_white():
            direction = 1
            home_row = 1
        else:#also wenns schwarz ist 
            direction = -1  
            home_row = 6


        #wir nehmen den SPEZIFISCHEN bauern mit Self und schauen uns seine Position an mit .cell
        #und speichern diese position in row und col (DIE WIR NICHT VERÄNDERN IN ZUKUNFT, WICHTIG!!!)
        row, col = self.cell


        #ein schritt ist nach vorne ist, die reihe zu nehmen wo der ist und seine richtung addieren
        #die spalte bleibt weil er ja nur nach vorne geht 
        one_step = (row + direction, col)

        #wenn die neue zelle wo wir hinwollen leer und gültig ist
        if self.board.cell_is_valid_and_empty(one_step):
            #füge diese zelle zur liste reachable_cells hinzu
            reachable_cells.append(one_step)

            #da wir ein schritt nach vorne bereits gecheckt haben 
            #und wir immernoch in diesem if block sind

            #machen wir einmal einen doppelschritt
            #also einfach die richtung was vorne ist für den Bauern mal 2, col bleibt gleich
            two_steps = (row + direction * 2, col)
            
            #wenn die row von dem bauen seine Home Row ist und die zelle in 2 schritten frei und gültig ist
            if row == home_row and self.board.cell_is_valid_and_empty(two_steps):
                #füge diese zelle "two_steps" der liste hinzu
                reachable_cells.append(two_steps)

        #jetzt erstellen wir eine liste mit 1 und -1 (für rechts und links)
        for value in [1, -1]:
            #der angriff ist, eins nach vorne und nach + value (also beim ersten durchlauf +1 beim zweiten -1)
            attack = (row + direction, col + value)

            #wenn unser piece das wir gerade bewegen (deshalb auch self als erstes argument)
            #auf der zelle attack angreifen kann
            if self.board.piece_can_hit_on_cell(self, attack):
                #dann füge die zelle attack der liste hinzu
                reachable_cells.append(attack)

        #jetzt zum schluss gebe die liste zurück
        return reachable_cells


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
        #1. Der Rook kann sich nur Horizontal und Vertikal bewegen 
        #2. mit einer liste aus 4 tupeln (1,0) usw kann man das implementieren
        #3. und dann mit dem tupel in die richtung gehen und überprüfen
        #   - wenn die zelle leer und valide ist, wiederhole noch ein schritt
        #   - wenn die zelle nicht leer ist, überprüfe ob es ein gegner ist
        #       -wenn ja, füge die zelle noch hinzu
        #       -wenn nein, dann fügen wir es NICHT hinzu 

        #leere liste erstellen
        reachable_cells = []

        #wir nehmen den SPEZIFISCHEN Turm mit Self und schauen uns seine Position an mit .cell
        #und speichern diese position in row und col (DIE WIR NICHT VERÄNDERN IN DER ZUKUNFT, 
        # WICHTIG!!! NICHT VERGESSEN IN DER PRÜFUNG)
        row, col = self.cell

        #die liste seiner richtunge erstellen
        #wir verändern immernur einen index, weil nur horizontal oder nur vertikal
        direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]


        #wir unpacken das tupel mit j und k 
        #zb das erste tupel ist (1,0) also j wird 1 und k wird 0
        for j, k in direction:

            #wir fügen die richtung zu der position wo der turm gerade ist hinzu 
            #und speichern diese neue zelle als new_cell
            new_cell = (row + j, col + k) 
            
            #während die new_cell valide und leer ist
            while self.board.cell_is_valid_and_empty(new_cell):
                #füge die new_cell der liste hinzu
                reachable_cells.append(new_cell)

                #jetzt unpacken wir die neue position
                #und fügen wir die richtung hinzu damit der noch ein schritt geht
                new_row, new_col = new_cell
                new_cell = (new_row + j, new_col + k)

            #Das wird dann solange wiederholt bis die new_cell nicht mehr leer oder valide ist
            #aber wir checken nochmal ob es sich um einen gegner bei der nächsten zelle handelt
             
            #wenn die neue zelle einen gegner hat 
            # (als argument geben wir erstmal den turm mit den wir bewegen wollen 
            # und die zelle wo wir hinwollen)
            if self.board.piece_can_hit_on_cell(self, new_cell):
                #dann füge das noch der liste hinzu
                reachable_cells.append(new_cell)


        #zum schluss geben wir die liste zurück
        return reachable_cells


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

        #Der Springer hat nur 8 mögliche bewegungen 
        #gehe durch alle 8 moves und guck ob das feld leer ist oder ein gegner auf dem feld steht

        #leere liste erstellen
        reachable_cells = []
        

        #wir nehmen den SPEZIFISCHEN Turm mit Self und schauen uns seine Position an mit .cell
        #und speichern diese position in row und col (DIE WIR NICHT VERÄNDERN IN DER ZUKUNFT, 
        # WICHTIG!!! NICHT VERGESSEN IN DER PRÜFUNG)
        row, col = self.cell
        
        #weil der springer sich wie ein L bewegt sind das seine 8 möglichen züge
        possible_moves = [(2, 1), (2, -1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (1,-2), (-1,-2)]


        #wir unpacken das tupel mit y und x (für die jeweiligen achsen wie beim koordinaten system) 
        for y, x in possible_moves:
            #wir speichern die neue position in "new_cell"
            new_cell = row + y, col + x
            
            #wir nutzen die funktion "piece_can_enter_cell" weil es perfekt passt
            
            #wenn ist die neue zelle leer oder da ist ein gegner drauf
            #(wir geben als argument den springer mit, durch self, und die neue zelle wo der hinwill)
            if self.board.piece_can_enter_cell(self, new_cell):
                #dann füge die "new_cell" der liste hinzu 
                reachable_cells.append(new_cell)        
       
       #gebe die liste zurück
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


        # GLEICHE LOGIK WIE DER TURM, eigentlich auch gleiche kommentare 


        #Der Läufer läuft diagonal, also einer der 4 richtungen unten bei direction
        #implementieren kann man das mit einer liste von tupeln wo beide richtungen angepasst werden 
        #jetzt gehe mehrmals in eine richtung und checke
        #       -ob die zelle leer und valide ist, wenn ja gehe noch einen schritt
        #       -wenn die zelle nicht leer ist überprüfe ob es ein gegner ist
        #           wenn ja füge das noch hinzu, 
        #           wenn nein dann nicht 

         
        #erstelle eine leere liste
        reachable_cells = []

        #wir nehmen den SPEZIFISCHEN Läufer mit Self und schauen uns seine Position an mit .cell
        #und speichern diese position in row und col (DIE WIR NICHT VERÄNDERN IN DER ZUKUNFT, 
        # WICHTIG!!! NICHT VERGESSEN IN DER PRÜFUNG)
        row, col = self.cell

        # die liste mit seinen richtungen
        direction = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        #wir unpacken das tupel mit j und k 
        for j, k in direction:

            #wir fügen die richtung zu der position wo der läufer im moment ist hinzu 
            #und speichern diese neue zelle als new_cell
            new_cell = (row + j, col + k)
            
            #während die new_cell valide und leer ist
            while self.board.cell_is_valid_and_empty(new_cell):
                #füge die new_cell der liste hinzu
                reachable_cells.append(new_cell)

                #jetzt unpacken wir die neue position
                #und fügen wir die richtung hinzu damit der noch ein schritt geht
                (new_row, new_col) = new_cell
                new_cell = (new_row + j, new_col + k)
            
            #Das wird dann solange wiederholt bis die new_cell nicht mehr leer oder valide ist
            #aber wir checken nochmal ob es sich um einen gegner bei der nächsten zelle handelt
            
            
            #wenn die neue zelle einen gegner hat 
            # (als argument geben wir erstmal den läufer den wir bewegen wollen 
            # und die zelle wo wir hinwollen)
            if self.board.piece_can_hit_on_cell(self, new_cell):
                
                #dann füge das noch der liste hinzu
                reachable_cells.append(new_cell)
        
        #zum schluss geben wir die liste zurück
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


        #Es ist der exakt gleiche code wie turm und läufer
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
        row, col = self.cell

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