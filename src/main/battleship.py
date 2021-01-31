import random
from tools import colored, colored_background


class Cell:
    """ A single cell on the board. For example: A1, column A at row 1, can be hit or not, part of ship or not"""
    def __init__(self, col: str, row: int, hit: bool = False, part: str = None):
        # Column choices: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        if col not in Board.columns:
            raise Exception('Col {} must be in allowed columns list {}'.format(col, Board.columns))
        self._col = col

        # Row choices: [1, 2, 3, 4, 5, 6, 7, 8]
        if row not in Board.rows:
            raise Exception('Row {} must be in allowed rows list {}'.format(row, Board.rows))
        self._row = row

        # True When sell has been hit, False by default
        self._hit = hit

        # Part of ship it houses if any. Choices: Front, Middle, Rear
        if part and part not in Ship.SHIP_PARTS:
            raise Exception('Part {} is not in allowed ship parts list {}'.format(part, Ship.SHIP_PARTS))
        self._part = part

        # Coordinates of neighboring cells, tuple (col, row)
        self._above = self.default_above()
        self._below = self.default_below()
        self._before = self.default_before()
        self._after = self.default_after()

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, col):
        self._col = col

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, row):
        self._row = row

    @property
    def above(self):
        return self._above

    @property
    def below(self):
        return self._below

    @property
    def before(self):
        return self._before

    @property
    def after(self):
        return self._after

    @property
    def hit(self):
        return self._hit

    @hit.setter
    def hit(self, hit):
        self._hit = hit

    @property
    def part(self):
        return self._part

    @part.setter
    def part(self, part):
        self._part = part

    def default_above(self):
        """ Cell is above current cell, must be on the same column"""
        above_row = self.row - 1
        if above_row in Board.rows:
            return self.col, above_row

    def default_below(self):
        """ Cell is below current cell, must be on the same column"""
        below_row = self.row + 1
        if below_row in Board.rows:
            return self.col, below_row

    def default_before(self):
        """ Cell is before current cell, must be on the same row"""
        before_col_index = Board.columns.index(self.col) - 1
        if 0 <= before_col_index <= 7:
            return Board.columns[before_col_index], self.row

    def default_after(self):
        """ Cell is after current cell, must be on the same row"""
        after_col_index = Board.columns.index(self.col) + 1
        if 0 <= after_col_index <= 7:
            return Board.columns[after_col_index], self.row

    def __repr__(self):
        part = 'n'
        if self.part == 'Front':
            part = 'f'
        elif self.part == 'Middle':
            part = 'm'
        elif self.part == 'Rear':
            part = 'r'
        if self.part:
            return colored(
                colored_background(
                    '{}{}[{}{}]'.format(
                        self.col, self.row, part,
                        colored('x', 'red') if self.hit else colored('o', 'green')), 'orange'), 'blue')
        return '{}{}[{}{}]'.format(
            self.col, self.row, part, colored('x', 'red') if self.hit else colored('o', 'green'))

    def __str__(self):
        return self.__repr__()


class Ship:
    """ A ship is combination of 3 cells that can be vertically or horizontally placed, respectively of type 1 or 2 """
    SHIP_PARTS = ['Front', 'Middle', 'Rear']

    def __init__(self):
        self._type = random.choice(Board.SHIP_PLACEMENTS)
        self._middle = self.find_middle_cell()
        self._front = self.find_front_cell(self.middle)
        self._rear = self.find_rear_cell(self.middle)
        self._sunk = False

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type_value):
        self._type = type_value

    @property
    def sunk(self):
        return self._sunk

    @sunk.setter
    def sunk(self, sunk):
        self._sunk = sunk

    @property
    def front(self):
        return self._front

    @front.setter
    def front(self, front):
        self._front = front

    @property
    def middle(self):
        return self._middle

    @middle.setter
    def middle(self, middle):
        self._middle = middle

    @property
    def rear(self):
        return self._rear

    @rear.setter
    def rear(self, rear):
        self._rear = rear

    def sink(self):
        """ A ship sinks when all of its parts have been hit"""
        if self.front.hit and self.middle.hit and self.rear.hit:
            self.sunk = True

    def is_vertical(self):
        return self.type == Board.VERTICAL

    def is_horizontal(self):
        return self.type == Board.HORIZONTAL

    def find_middle_cell(self):
        return Cell(Board.get_random_middle_col(self.type), Board.get_random_middle_row(self.type), part='Middle')

    def find_front_cell(self, middle: Cell):
        if self.is_vertical():
            # above cell
            return Cell(middle.above[0], middle.above[1], part='Front')
        if self.is_horizontal():
            # before cell
            return Cell(middle.before[0], middle.before[1], part='Front')

    def find_rear_cell(self, middle):
        if self.is_vertical():
            # below cell
            return Cell(middle.below[0], middle.below[1], part='Rear')
        if self.is_horizontal():
            # after cell
            return Cell(middle.after[0], middle.after[1], part='Rear')

    def __repr__(self):
        if self.type == Board.HORIZONTAL:
            return '{}{}{}'.format(self.front, self.middle, self.rear)
        if self.type == Board.VERTICAL:
            return '{}\n{}\n{}'.format(self.front, self.middle, self.rear)


class Board:

    # All columns available
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    # Columns eligible to house middle of the ship assuming horizontal placement
    middle_columns = ['B', 'C', 'D', 'E', 'F', 'G']

    # All rows available
    rows = [1, 2, 3, 4, 5, 6, 7, 8]

    # Rows eligible to house middle of the ship assuming vertical placement
    middle_rows = [2, 3, 4, 5, 6, 7]

    # Vertical ship placement
    VERTICAL = 1

    # Horizontal ship placement
    HORIZONTAL = 2

    SHIP_PLACEMENTS = [VERTICAL, HORIZONTAL]

    def __init__(self):
        self._ship = Ship()
        self._cells = self.initialize_board()

    @property
    def ship(self):
        return self._ship

    @property
    def cells(self):
        return self._cells

    def initialize_board(self):
        # Create cells for the entire board and track them in a dictionary
        board_cells = {}
        for row in self.rows:
            row_cells = []  # all cells on one row, one for each column
            for col in self.columns:
                row_cells.append(Cell(col, row))
            board_cells[row] = row_cells

        return board_cells

    def place_ship(self):
        # Place all parts of the ship on the board
        self.replace_cell_on_the_board(self.ship.front)
        self.replace_cell_on_the_board(self.ship.middle)
        self.replace_cell_on_the_board(self.ship.rear)

    @classmethod
    def get_random_col(cls):
        return random.choice(cls.columns)

    @classmethod
    def get_random_row(cls):
        return random.choice(cls.rows)

    @classmethod
    def get_random_middle_row(cls, placement_type):
        """
        :param placement_type: Ship placement type. Either vertical (1) or horizontal (2)
        :return: row number
        """

        # For vertical placement,Row 1 and 8 are not eligible
        if placement_type == cls.VERTICAL:
            return random.choice(cls.middle_rows)

        if placement_type == cls.HORIZONTAL:
            return cls.get_random_row()

    @classmethod
    def get_random_middle_col(cls, placement_type):
        """
        :param placement_type: Ship placement type. Either vertical (1) or horizontal (2)
        :return: col alphabet
        """

        if placement_type == cls.VERTICAL:
            return cls.get_random_col()
        # For horizontal placement, Col A and H are not eligible
        if placement_type == cls.HORIZONTAL:
            return random.choice(cls.middle_columns)

    def replace_cell_on_the_board(self, new_cell: Cell):
        # Find row to place new cell
        board_row = self.cells[new_cell.row]

        # Find index of column
        board_col_index = Board.columns.index(new_cell.col)

        # Put new cell at index
        board_row[board_col_index] = new_cell

    def get_cell(self, col, row):
        if col in self.columns and row in self.rows:
            board_row = self.cells[row]
            col_index = self.columns.index(col)
            return board_row[col_index]
        else:
            raise Exception('Cell at col {} and row {} does not exist'.format(col, row))

    def get_random_cell(self):
        return self.get_cell(self.get_random_col(), self.get_random_row())

    def __repr__(self):
        board_print = ''
        for row, row_cells in self.cells.items():
            row_print = ''
            for cell in row_cells:
                row_print = '{}{} '.format(row_print, cell)

            board_print = '{}\n{}'.format(board_print, row_print)

        return board_print


class Player:
    """ Each player has own board and own ship"""
    def __init__(self, name=None):
        self._name = name
        self._board = Board()
        self._last_hit_cell = None  # Last cell to be hit on player's own board

    @property
    def last_hit_cell(self):
        return self._last_hit_cell

    @last_hit_cell.setter
    def last_hit_cell(self, cell: Cell):
        self._last_hit_cell = cell

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        self._board = board

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Game:
    def __init__(self, player_1_name: str = 'Player 1', player_2_name:  str = 'Player 2'):
        self._round = 0  # Current round
        self._player_1 = Player(name=player_1_name)
        self._player_2 = Player(name=player_2_name)
        self._is_over = False  # Game is over when one player's ship is sunk
        self._winner = None
        self._loser = None
        self._status = 'Complete' if self.is_over else 'In Progress'
        self._shoots_first = random.choice([self.player_1, self.player_2])
        self._shoots_second = self.player_2 if self._shoots_first == self.player_1 else self.player_1

    @property
    def round(self):
        return self._round

    @round.setter
    def round(self, round_value):
        self._round = round_value

    @property
    def player_1(self):
        return self._player_1

    @player_1.setter
    def player_1(self, player_1):
        self._player_1 = player_1

    @property
    def player_2(self):
        return self._player_2

    @player_2.setter
    def player_2(self, player_2):
        self._player_2 = player_2

    @property
    def is_over(self):
        return self._is_over

    @is_over.setter
    def is_over(self, is_over):
        self._is_over = is_over

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, winner):
        self._winner = winner

    @property
    def loser(self):
        return self._loser

    @loser.setter
    def loser(self, loser):
        self._loser = loser

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    def play_round(self):
        # Round one each player place their ship
        if self.is_over:
            raise Exception('Game is already over. Winner: {}'.format(self.winner))

        if self.round == 0:
            self._shoots_first.board.place_ship()
            self._shoots_second.board.place_ship()
        else:
            self.shoot(self._shoots_second)
            self.shoot(self._shoots_first)

        if self.player_1.board.ship.sunk:
            self.is_over = True
            self.loser = self.player_1
            self.winner = self.player_2
            self.status = 'Complete'

        elif self.player_2.board.ship.sunk:
            self.is_over = True
            self.loser = self.player_2
            self.winner = self.player_1
            self.status = 'Complete'

        self.round += 1
        
        if self.is_over:
            print('----------------------------\n')
            print('Last round board status\n')
            print('----------------------------')
            print(self)

    @staticmethod
    def shoot(opponent: Player):
        """
        :param opponent: Player with board getting shot at
        :return:
        """
        random_cell = opponent.board.get_random_cell()
        random_cell.hit = True
        opponent.last_hit_cell = random_cell
        opponent.board.ship.sink()

    def __repr__(self):

        title = '\n{} vs {}: Round {}, {}, Winner: {}'.format(self._shoots_first, self._shoots_second, self.round, self.status, self.winner)
        l1 = '---------------------------------------------------------------------------------------------------'
        l2 = '==================================================================================================='
        return '{}\n{}\'s Board{}\n{}\n{}\'s Board{}\n{}\n{}\n{}\n\n'.format(
            title,
            self._shoots_first.name,
            self._shoots_first.board,
            l1,
            self._shoots_second.name,
            self._shoots_second.board,
            '{} hit {}'.format(self._shoots_first.name, self._shoots_second.last_hit_cell),
            '{} hit {}'.format(self._shoots_second.name, self._shoots_first.last_hit_cell),
            l2)

    def __str__(self):
        return self.__repr__()


if __name__ == '__main__':
    # Run unittests
    # python -m unittest battleship_tests.py


    player_1_name = input("Enter Player 1 name: ")
    player_2_name = input("Enter Player 2 name: ")

    if not player_1_name:
        player_1_name = 'Player 1'

    if not player_2_name:
        player_2_name = 'Player 2'



    new_game = Game(player_1_name, player_2_name)

    while not new_game.is_over:
        new_game.play_round()

    print ('You sunk my battleship')





