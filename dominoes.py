#! python3
"""Domino Game."""

import re
import random

import numpy as np


class DominoGame:
    """A class that represents a domino game."""

    def __init__(self):
        """Initialize a game with a full domino set."""
        domino_set = DominoSet()

        self.computer_set = domino_set.get_part(7)
        self.player_set = domino_set.get_part(7)
        self.stock_set = domino_set
        self.snake = Snake()
        self.status = self.get_starting_player()

    def __str__(self):
        """Print game status."""
        string = "=" * 70 + "\n" \
            f"Stock size: {self.stock_set.get_size()}\n" \
            f"Computer dominoes: {self.computer_set.get_size()}\n\n" \
            f"{self.snake.__str__()}\n\n" \
            "Your pieces:\n" \
            f"{self.player_set.get_dominoes_str()}\n\n" \
            f"{self.get_status_msg()}"
        return string

    def get_starting_player(self):
        """Determine the starting piece and the first player."""
        max_computer_domino = self.computer_set.get_largest_domino()
        max_player_domino = self.player_set.get_largest_domino()

        if max_computer_domino is None and max_player_domino is not None:
            # If only player has a double domino
            DominoGame.move_domino(max_player_domino, self.player_set,
                                   self.snake)
            return "computer"
        elif max_player_domino is None and max_computer_domino is not None:
            # If only player has a double domino
            DominoGame.move_domino(max_computer_domino, self.computer_set, self.snake)
            return "player"
        elif max_computer_domino.numbers == max_computer_domino.numbers:
            # Start over if both players have the same comparison result
            self.__init__()
        else:
            if max_player_domino.numbers[0] > max_computer_domino.numbers[0]:
                DominoGame.move_domino(max_player_domino, self.player_set,
                                       self.snake)
                return "computer"
            elif max_computer_domino.numbers[0] > max_player_domino.numbers[0]:
                DominoGame.move_domino(max_computer_domino, self.computer_set,
                                       self.snake)
                return "player"

    def get_status_msg(self):
        """Get message representing next player status."""
        if self.status == "computer":
            msg = "Status: Computer is about to make a move." \
                  " Press Enter to continue..."
        else:
            msg = "Status: It's your turn to make a move. Enter your command."

        return msg

    @staticmethod
    def move_domino(domino, source, target, side="R", snake=False):
        """Takes a domino from a source set and places it in a target set."""
        target.add_domino(domino, side)             # add domino to target

        domino_id = source.dominoes.index(domino)   # get domino index
        del source.dominoes[domino_id]              # del the piece from source

    def can_add_to_snake(self, move):
        """Check that the domino piece can be added to the snake."""
        if move > 0:
            snake_side_num = self.snake.get_side_number("R")
        elif move < 0:
            snake_side_num = self.snake.get_side_number("L")
        else:
            return True

        domino = self.get_current_player_set().dominoes[abs(move) - 1]

        if snake_side_num in domino.numbers:
            return True

        if self.status == "player":
            # If such move can't be executed by a player
            print("Illegal move. Please try again.")
        return False

    def is_command_valid(self, command):
        """Check if the player move command is valid."""
        if len(command) > 2:
            print("Invalid input. Please try again.")
            return False
        try:
            move = int(command)
            if abs(move) > self.player_set.get_size():
                # If user takes a non-present domino piece (out of range)
                print("Invalid input. Please enter an existing index.")
                return False
            if move != 0:
                return self.can_add_to_snake(move)
        except ValueError:
            print(
                f"Could not process the move described by command: '{command}'."
                " Please try again.")
            return False

        return True

    def get_player_command(self):
        """Get player move from human (input) or computer (random)."""
        # print(self.get_status_msg())

        # Get human or computer input
        if self.status == "player":
            # Get human input until a valid command is entered
            DO_GET_INPUT = True
            while DO_GET_INPUT:
                command = input()
                if self.is_command_valid(command):
                    DO_GET_INPUT = False
        else:
            input()         # get arbitrary input
            command = "0"   # initialize command with default value
            self.get_domino_scores()
            sorted_set = sorted(self.computer_set.dominoes,
                                key=lambda x: x.score,
                                reverse=True)
            for i, domino in enumerate(sorted_set, 1):
                if self.can_add_to_snake(i):
                    command = str(i)
                    break
                elif self.can_add_to_snake(-i):
                    command = str(-i)
                    break

        return command

    def get_current_player_set(self):
        """Return a domino set of a current player."""
        if self.status == "player":
            return self.player_set
        elif self.status == "computer":
            return self.computer_set

    def get_domino_scores(self):
        """Calculate domino scores based on their rarity."""
        # Count the number of 0's, 1's, etc. in hand and snake
        current_player_set = self.get_current_player_set()
        hand_numbers = current_player_set.get_domino_values()
        snake_numbers = self.snake.get_domino_values()
        total_numbers = np.array([hand_numbers + snake_numbers])

        counts = {}
        for i in range(7):
            counts[i] = np.sum(total_numbers == i)

        for domino in current_player_set.dominoes:
            domino.score = counts[domino.numbers[0]] + counts[domino.numbers[1]]

    def do_play_game(self):
        """Determine whether the end-game conditions are met."""
        # 1. One of the players runs out of dominoes - winner
        if not self.player_set.dominoes or not self.computer_set.dominoes:
            return False, "win"

        # 2. The numbers on the ends of the snake are equal and appear 8 times
        first_domino = self.snake.get_domino_values()[0]
        last_domino = self.snake.get_domino_values()[-1]

        # Check that last domino consists of any number from the first one
        end_num = False
        for num in first_domino:
            if num in last_domino:
                end_num = num
                break

        if end_num:
            counter = 2
            for piece in self.snake.get_domino_values()[1:-1]:
                if end_num in piece:
                    counter += 1
            if counter == 8:
                return False, "draw"

        return True, None

    def make_move(self):
        """Make a move in the game based on a sign and integer number input.

        Take an action in the game by placing a domino on the left or right side
        of the snake or taking an extra piece from the stock and skip a turn.
        """
        move = self.get_player_command()
        current_set = self.get_current_player_set()

        if "0" in move:
            # Get a domino piece from stock or skip turn if stock is empty
            try:
                current_set.dominoes.append(self.stock_set.dominoes.pop())
            except IndexError:
                pass
        else:
            if move[0] == "-":
                side = "L"
                move = move[1]  # set domino number to the first position
            else:
                side = "R"

            # Get domino to move based on it's index in the domino set list
            domino_num = int(move) - 1
            domino_to_move = current_set.dominoes[domino_num]

            # Move the domino piece from current player set to the snake set
            DominoGame.move_domino(domino_to_move, current_set, self.snake,
                                   side, snake=True)

        # Set next player status
        self.status = "player" if self.status == "computer" else "computer"

    def play(self):
        """Play the game."""
        DO_PLAY_FLAG = True
        while DO_PLAY_FLAG:
            print(self)

            self.make_move()

            DO_PLAY_FLAG, result = self.do_play_game()

        if result == "draw":
            print("Status: The game is over. It's a draw!")
        else:
            if self.status == "computer":
                print("Status: The game is over. You won!")
            else:
                print("Status: The game is over. The computer won!")


class DominoSet:
    """A class that represents a domino set."""

    def __init__(self, domino_list=None):
        """Initialize a domino set.

        Initializes a DominoSet instance with 'dominoes' attribute that stores
        a list of Domino objects. Pairs of integers stored in a form of a list
        or a tuple are also valid.
        A full set will be created by default. This behavior may be changed by
        passing 'domino_list' argument.

        Args:
            domino_list: a list with Domino objects to create a DominoSet
                (default None);

        Raises:
            Exception: when any element in the 'domino_list' is not valid;
        """
        self.dominoes = []

        if domino_list is None:
            # Initialize with a full domino set
            for i in range(6 + 1):
                self.dominoes += [Domino([i, j]) for j in range(i, 6 + 1)]
        else:
            if domino_list:
                # Initialize with an arbitrary set
                for element in domino_list:
                    if isinstance(element, Domino):
                        self.dominoes.append(element)
                    elif isinstance(element, (tuple, list)):
                        self.dominoes.append(Domino(element))
                    else:
                        msg = "Wrong argument was passed to the function."
                        raise Exception(msg)

    def __str__(self):
        """Print a domino set as a list of dominoes."""
        return str(self.get_domino_values())

    def add_domino(self, domino, side="R"):
        """Add a domino piece to a DominoSet instance.

        Args:
            domino(Domino): domino object that will be added to the snake;
            side(str): 'L' if domino should be added on the left, 'R' otherwise;

        Raises:
            TypeError: when 'domino' argument is not a Domino class instance;
            ValueError: when 'side' argument value is neither 'L' nor 'R';
        """
        if not isinstance(domino, Domino):
            msg = "Argument passed to the function was not a Domino object."
            raise TypeError(msg)

        if side not in ("L", "R"):
            msg = "Wrong 'side' argument value. Valid options are 'L' or 'R'."
            raise ValueError(msg)

        if side == "R":
            self.dominoes.append(domino)
        elif side == "L":
            self.dominoes.insert(0, domino)

    def get_part(self, quantity, remove_original=True):
        """Get a part of random domino pieces from the domino set."""
        if not isinstance(remove_original, bool):
            raise TypeError("Wrong type of the 'remove_original' argument.")

        part = random.sample(self.dominoes, quantity)

        if remove_original:
            for piece in part:
                self.dominoes.remove(piece)

        return DominoSet(domino_list=part)

    def get_double_dominoes(self):
        """Get a list of double dominoes in the domino set."""
        return [domino for domino in self.dominoes if domino.is_double()]

    def get_largest_domino(self):
        """Find the largest double domino in the domino set."""
        doubles = self.get_double_dominoes()
        if not doubles:
            return None
        else:
            max_domino = doubles[0]
            for domino in doubles:
                if domino.numbers[0] > max_domino.numbers[0]:
                    max_domino = domino

            return max_domino

    def get_domino_values(self):
        """Get numbers of domino pieces as a list."""
        return [domino.numbers for domino in self.dominoes]

    def get_dominoes_str(self):
        """Get a string representing player's domino set."""
        pieces_str_list = [f'{i}:{piece}' for i, piece in
                           enumerate(self.dominoes, 1)]

        return "\n".join(pieces_str_list)

    def get_size(self):
        """Get the number of dominoes remaining in the stock."""
        return len(self.dominoes)

    def get_side_number(self, side):
        """Get the first or the last number from the domino set."""
        if side == "R":
            side_num = self.dominoes[-1].numbers[-1]
        else:
            side_num = self.dominoes[0].numbers[0]

        return side_num


class Snake(DominoSet):
    """A DominoSet subclass that represents a snake."""

    def __init__(self):
        super().__init__(domino_list=[])

    def __str__(self):
        """Replaces get_snake_str"""
        string = ""
        if len(self.dominoes) > 6:
            for domino in self.dominoes[:3]:
                string += str(domino.numbers)
            string += "..."
            for domino in self.dominoes[-3:]:
                string += str(domino.numbers)
        else:
            for domino in self.dominoes:
                string += str(domino.numbers)

        return string

    def add_domino(self, domino, side):
        """Add a domino piece to a Snake instance.

        The function checks if the domino piece needs to be switched and appends
        it to a list that stores snake pieces.
        """
        if self.dominoes:
            side_number = self.get_side_number(side)
            if side == "R" and domino.numbers[0] != side_number:
                domino.switch_numbers()
            if side == "L" and domino.numbers[1] != side_number:
                domino.switch_numbers()

        super().add_domino(domino, side)


class Domino:
    """A class that represents a single domino piece."""

    def __init__(self, numbers):
        """Initialize a domino piece using a list of integers."""
        if self.is_valid(numbers):
            self.numbers = numbers
        else:
            msg = f'Error when initializing a domino piece. Could not ' \
                  f'initialize a domino piece with argument {numbers}. '
            raise ValueError(msg)

    def __repr__(self):
        return f'Domino({self.numbers})'

    def __str__(self):
        """Print domino numbers as a collection of lists."""
        return f'{self.numbers}'

    def switch_numbers(self):
        """Switch domino orientation."""
        numbers = self.numbers[::-1]
        self.numbers = numbers

    def is_double(self):
        """Check that the domino is 'double' - both numbers are equal."""
        return True if self.numbers[0] == self.numbers[1] else False

    @staticmethod
    def is_valid(numbers):
        """Check that the domino piece is valid.

        A domino piece is valid when the following conditions are fulfilled:
        - the 'numbers' list consists of two elements only,
        - these elements are of integer type,
        - both elements values are between or equal 0 and 6 range.

        Arguments:
            numbers(list): a list of numbers that define a domino piece.

        Returns:
            bool: True if 'numbers' list satisfies the defined conditions.
        """
        if len(numbers) != 2:
            return False
        else:
            # Check that the list elements are of int type
            is_integer = all(map(lambda x: isinstance(x, int), numbers))
            if not is_integer:
                return False

            # Check that the list elements are in valid range
            is_in_range = all(map(lambda x: 0 <= x <= 6, numbers))
            if not is_in_range:
                return False

        return True


if __name__ == "__main__":
    # Initialize a seed
    random.seed(42)

    # Initialize a Domino Game
    game = DominoGame()
    game.play()
