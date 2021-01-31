import unittest
import battleship


class CellTest(unittest.TestCase):
    """ Test Cell class"""
    def setUp(self) -> None:
        rand_col = battleship.Board.get_random_col()
        rand_row = battleship.Board.get_random_row()
        self.cell = battleship.Cell(rand_col, rand_row)

    def test_cell_neighbors(self):
        """ Above, below, before, after"""

        # Upper corner cell
        cell = battleship.Cell('A', 1)
        self.assertIsNone(cell.above)
        self.assertIsNone(cell.before)
        self.assertEqual(cell.below, ('A', 2))
        self.assertEqual(cell.after, ('B', 1))

        # Lower corner cell
        cell = battleship.Cell('H', 8)
        self.assertEqual(cell.above, ('H', 7))
        self.assertEqual(cell.before, ('G', 8))
        self.assertIsNone(cell.below)
        self.assertIsNone(cell.after)

        # Somewhere in the middle
        cell = battleship.Cell('G', 7)
        self.assertEqual(cell.above, ('G', 6))
        self.assertEqual(cell.before, ('F', 7))
        self.assertEqual(cell.below, ('G', 8))
        self.assertEqual(cell.after, ('H', 7))

        self.assertRaises(Exception, battleship.Cell, 'D', 49)


class BoardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.board = battleship.Board()
        print(self.board)

    def test_board_initialize(self):
        self.assertEqual(self.board.VERTICAL, 1)
        self.assertEqual(self.board.HORIZONTAL, 2)
        self.assertEqual(self.board.columns, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
        self.assertEqual(self.board.rows, [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(self.board.middle_rows, [2, 3, 4, 5, 6, 7])
        self.assertEqual(self.board.middle_columns, ['B', 'C', 'D', 'E', 'F', 'G'])

    def test_get_random_middle_cell(self):
        for i in range(0, 100000):
            # Row 1 and 8 cannot be used for middle of ship in vertical place
            middle_row_vertical = self.board.get_random_middle_row(self.board.VERTICAL)
            self.assertIn(middle_row_vertical, self.board.middle_rows)

            # We should be able to get above and below cells for middle rows in vertical placement
            random_col = self.board.get_random_col()
            self.assertIn(random_col, self.board.columns)
            middle_row_vertical_cell = battleship.Cell(random_col, middle_row_vertical)
            self.assertIsNotNone(middle_row_vertical_cell.above)
            self.assertIsNotNone(middle_row_vertical_cell.below)

            # For horizontal placement middle row can be anything, but middle column cannot be 'A' nor 'H'
            random_row = self.board.get_random_middle_row(self.board.HORIZONTAL)
            self.assertIn(random_row, self.board.rows)

            middle_col_horizontal = self.board.get_random_middle_col(self.board.HORIZONTAL)
            self.assertIn(middle_col_horizontal, self.board.middle_columns)
            middle_col_horizontal_cell = battleship.Cell(middle_col_horizontal, random_row)
            self.assertIsNotNone(middle_col_horizontal_cell.before)
            self.assertIsNotNone(middle_col_horizontal_cell.after)

    def test_get_cell(self):
        self.assertRaises(Exception, self.board.get_cell, 'U', 10)
        for col in self.board.columns:
            for row in self.board.rows:
                cell = self.board.get_cell(col, row)
                self.assertEqual(cell.row, row)
                self.assertEqual(cell.col, col)

    def test_get_random_cell(self):
        for i in range(0, 10000):
            cell = self.board.get_random_cell()
            # Assert cell belongs to the board
            self.assertIsNotNone(self.board.get_cell(cell.col, cell.row))


class ShipTest(unittest.TestCase):
    def setUp(self) -> None:
        self.ships = [battleship.Ship() for i in range(1, 10)]
        self.vertical = battleship.Board.VERTICAL
        self.horizontal = battleship.Board.HORIZONTAL

    def test_ship_initialization(self):
        for ship in self.ships:
            self.assertIsNotNone(ship.front)
            self.assertIsNotNone(ship.middle)
            self.assertIsNotNone(ship.rear)
            self.assertIn(ship.type, [self.vertical, self.horizontal])
            self.assertFalse(ship.sunk)

    def test_ship_placement(self):
        for ship in self.ships:
            if ship.type == self.vertical:
                # Same column
                self.assertEqual(ship.front.col, ship.middle.col)
                self.assertEqual(ship.rear.col, ship.middle.col)
            if ship.type == self.horizontal:
                # Same row
                self.assertEqual(ship.front.row, ship.middle.row)
                self.assertEqual(ship.rear.row, ship.middle.row)


class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.player = battleship.Player()

    def test_player(self):
        self.assertIsNone(self.player.name)
        self.assertIsNone(self.player.last_hit_cell)
        self.assertIsNotNone(self.player.board)
        self.player.name = 'Player 1'
        self.assertEqual(self.player.name, 'Player 1')


class GameTest(unittest.TestCase):
    def setUp(self) -> None:
        self.game = battleship.Game(player_1_name='John', player_2_name='Jack')

        self.player_1 = self.game.player_1
        self.player_2 = self.game.player_2

        self.board_1 = self.player_1.board
        self.board_2 = self.player_2.board

        self.ship_1 = self.board_1.ship
        self.ship_2 = self.board_2.ship

    def test_game(self):
        self.assertFalse(self.game.is_over)
        self.assertEqual(self.game.status, 'In Progress')

    def test_players(self):
        self.assertEqual(self.game.player_1.name, 'John')
        self.assertEqual(self.game.player_2.name, 'Jack')

    def test_boards(self):
        self.assertIsNotNone(self.game.player_1.board)
        self.assertIsNotNone(self.game.player_2.board)
        self.assertNotEqual(self.game.player_1.board, self.game.player_2.board)

    def test_ships(self):
        self.assertFalse(self.game.player_1.board.ship.sunk)
        self.assertFalse(self.game.player_2.board.ship.sunk)

    def test_play_round(self):
        # Place ships on round 1
        self.game.play_round()
        self.assertEqual(self.game.player_1.last_hit_cell, None)
        self.assertEqual(self.game.player_2.last_hit_cell, None)

        # Players hit each other's boards
        self.game.play_round()
        self.assertIsNotNone(self.game.player_1.last_hit_cell)
        self.assertIsNotNone(self.game.player_2.last_hit_cell)

        while not self.game.is_over:
            self.game.play_round()

        self.assertRaises(Exception, self.game.play_round)
        self.assertGreater(self.game.round, 4)


if __name__ == '__main__':
    unittest.main()
