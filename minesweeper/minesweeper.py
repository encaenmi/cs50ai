import itertools
import random

from pygame.constants import KMOD_NONE


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # if the number of cells in sentence equals the count, return all
        # unsure if there are other cases to handle here
        if self.count != 0 and len(self.cells) == self.count:
            return self.cells
        

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if there are no more cells in the count, all are safe
        # unsure if there are other cases to handle here
        if self.count == 0:
            return self.cells


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # if you know a cell is a mine, you should take it out?
        # and create a new sentence such as {(cell), 1}? or just take it out and decrease the count?
        if cell in self.cells:
            #print(f"Cell {cell} marked as mine. Count is now {self.count - 1}")
            self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # if cell is in this sentence's list, remove from list
        if cell in self.cells:
            #print(f"Cell {cell} marked as safe.")
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        if cell not in self.mines:
            self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        if cell not in self.safes:
            self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # accept a cell and its count, update count
        # update self.mines, self.safes, self.moves_made and self.knowledge
        # it will always get safe cells, as mines end the game
        # so you're creating or updating a sentence every time you call this function

        # update self.moves_made and self.safes
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # identify neighbors, excluding cells beyond borders, own cell, and safe cells
        neighbors = set()

        for i in range(max(0, cell[0] - 1), min(self.height, cell[0] + 2)):
            for j in range(max(0, cell[1] - 1), min(self.width, cell[1] + 2)):
                current_cell = (i, j)
                if current_cell != cell and current_cell not in self.safes:
                    neighbors.add(current_cell)

        # add list of previously unrevealed potentially safe neighbors to knowledge
        self.knowledge.append(Sentence(neighbors, count))

        """
        ways in which you can infer knowledge after adding a new sentence:
        1. go through sentences in knowledge and remove known safes
        2. go through sentences in knowledge, remove known mines, and decrease count
        3. go through sentences in knowledge, find those w count = 0, mark cells as safes (check_safes_and_mines -> known_safes)
        4. go through sentences in knowledge, find those w count = len(cells), mark cells as mines (check_safes_and_mines -> known_mines)
        5. infer new sentences using set operations (set_inference)
        6. perhaps recursively loop through these until there's nothing else to do?
        """
        
        self.check_safes_and_mines()
        self.set_inference()
        self.check_safes_and_mines()

        # testing empty removal
        self.cleanup()
        
        # debugging
        """
        print("Cells marked as safe:")
        for c in self.safes:
            if c not in self.moves_made:
                print(c)
        print("Cells marked as mines:")
        for c in self.mines:
            print(c)
        
        print(f"Number of cells marked as safe: {len(self.safes)}")
        print(f"Number of cells marked as mines: {len(self.mines)}")

        for sentence in self.knowledge:
            print(f"{sentence.cells}, {sentence.count}")
        """


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        try: 
            eligible = []

            for i in self.safes:
                eligible.append(i)

            for j in self.moves_made:
                eligible.remove(j)

            # choose randomly among available moves
            chosen_one = random.randint(0,len(eligible)-1)

            return eligible[chosen_one]

        except:
            return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        try:
            # make list of full range, while discarding mines and moves
            eligible = []
            for i in range(0, self.height):
                for j in range(0, self.width):
                    if (i, j) not in self.moves_made and (i, j) not in self.mines:
                        eligible.append((i, j))

            chosen_one = random.randint(0,len(eligible)-1)

            return eligible[chosen_one]

        except:
            return None
        

    # use sentences' known_mines and known_safes functions to update knowledge
    def check_safes_and_mines(self):
        mines_to_add = []
        safes_to_add = []
        for sentence in self.knowledge:
            if sentence.known_mines():
                for mine in sentence.known_mines():
                    if mine not in self.safes and mine not in self.mines:
                        #self.mines.add(mine)
                        mines_to_add.append(mine)
            if sentence.known_safes():
                for safe in sentence.known_safes():
                    if safe not in self.safes:
                        #self.safes.add(safe)
                        safes_to_add.append(safe)
        
        for m in mines_to_add:
            self.mark_mine(m)
        for s in safes_to_add:
            self.mark_safe(s)

    def set_inference(self):
        # then infer all new sentences you can infer
        # any time we have two sentences set1 = count1
        # and set2 = count2, where set1 is a subset of set2
        # we can construct the new sentence set2 - set1 = count2 - count1
        sentencesToAdd = []
        sentencesToRemove = []

        for set1 in self.knowledge:
            if set1.cells != set():
                for set2 in self.knowledge:
                    if set1.cells != set2.cells and set2.cells != set():
                        if set1.cells.issubset(set2.cells):

                            newSentence = Sentence(set2.cells.difference(set1.cells), set2.count - set1.count)

                            if newSentence not in sentencesToAdd:
                                sentencesToAdd.append(newSentence)
                            if set2 not in sentencesToRemove:
                                sentencesToRemove.append(set2)
                            
                        elif set2.cells.issubset(set1.cells):

                            newSentence = Sentence(set1.cells.difference(set2.cells), set1.count - set2.count)
                            
                            if newSentence not in sentencesToAdd:
                                sentencesToAdd.append(newSentence)
                            if set1 not in sentencesToRemove:
                                sentencesToRemove.append(set1)

        
        for sentenceToRemove in sentencesToRemove:
            for sentence in self.knowledge:
                if sentence == sentenceToRemove:
                    #print(f"removing sentence {sentence.cells} = {sentence.count}")
                    self.knowledge.remove(sentence)
        
        for sentenceToAdd in sentencesToAdd:
            #print(f"adding sentence {sentenceToAdd.cells} = {sentenceToAdd.count}")
            self.knowledge.append(sentenceToAdd)

    def cleanup(self):
        for sentence in self.knowledge:
            if sentence.cells == set():
                self.knowledge.remove(sentence)