#! python3
"""Unit test script for testing class regarding domino game."""
import random
import unittest

from dominoes import Domino
from dominoes import DominoSet


class TestDomino(unittest.TestCase):
    """A class for testing 'Domino' class.

    answer - outcome from using a method.
    output - expected result.
    """

    def test_switch_numbers(self):
        """Test switch numbers method."""
        answer = Domino([1, 0]).numbers

        piece = Domino([0, 1])
        piece.switch_numbers()
        output = piece.numbers

        self.assertEqual(output, answer)

    def test_is_valid01(self):
        """Test is_valid method with different number of elements."""
        self.assertFalse(Domino.is_valid([]))           # empty list
        self.assertFalse(Domino.is_valid([0]))          # one-element list
        self.assertTrue(Domino.is_valid([0, 1]))        # one-element list
        self.assertFalse(Domino.is_valid([0, 1, 2]))    # three-element list

    def test_is_valid02(self):
        """Test is_valid method with different element types."""
        self.assertTrue(Domino.is_valid([0, 1]))            # both int
        self.assertFalse(Domino.is_valid(['zero', 1]))      # 1nd str
        self.assertFalse(Domino.is_valid([0, 'one']))       # 2nd str
        self.assertFalse(Domino.is_valid(['zero', 'one']))  # both str
        self.assertFalse(Domino.is_valid([['zero'], [1]]))  # both list
        self.assertFalse(Domino.is_valid([[0], [1]]))       # both list

    def test_is_valid03(self):
        """Test is_valid method with different element values."""
        # Correct inputs
        self.assertTrue(Domino.is_valid([0, 0]))
        self.assertTrue(Domino.is_valid([1, 0]))
        self.assertTrue(Domino.is_valid([1, 1]))
        self.assertTrue(Domino.is_valid([1, 5]))
        self.assertTrue(Domino.is_valid([1, 6]))

        # Incorrect inputs
        self.assertFalse(Domino.is_valid([-1, -1]))
        self.assertFalse(Domino.is_valid([-1, 0]))
        self.assertFalse(Domino.is_valid([0, -1]))
        self.assertFalse(Domino.is_valid([7, 7]))
        self.assertFalse(Domino.is_valid([7, 0]))
        self.assertFalse(Domino.is_valid([0, 7]))

    def test_is_double(self):
        """Test is_double method."""
        piece_1 = Domino([0, 1])
        piece_2 = Domino([0, 0])
        piece_3 = Domino([1, 0])
        piece_4 = Domino([1, 1])

        self.assertFalse(piece_1.is_double())
        self.assertTrue(piece_2.is_double())
        self.assertFalse(piece_3.is_double())
        self.assertTrue(piece_4.is_double())


class TestDominoSet(unittest.TestCase):
    """Class for testing DominoSet class."""

    def setUp(self):
        random.seed(42)
        self.domino_set = DominoSet()   # initialize a full domino set

    def test_init(self):
        """Test __init__ method with arbitrary Domino list."""
        self.assertRaises(Exception, DominoSet, [Domino([0, 0]), 2])

    def test_get_double_dominoes01(self):
        """Test get_double_dominoes method with full set."""
        domino_set = DominoSet()

        result = [domino.numbers for domino in domino_set.get_double_dominoes()]
        answer = [[i, i] for i in range(6+1)]
        self.assertEqual(result, answer)

    def test_get_double_dominoes02(self):
        """Test get_double_dominoes method with no double dominoes in set."""
        domino_set = DominoSet(domino_list=[])

        result = [domino.numbers for domino in domino_set.get_double_dominoes()]
        answer = []
        self.assertEqual(result, answer)

        domino_set = DominoSet(domino_list=[[0, 1], [5, 6]])

        result = [domino.numbers for domino in domino_set.get_double_dominoes()]
        self.assertEqual(result, answer)

    def test_get_largest_domino(self):
        """Test get_largest_domino method with full set."""
        domino_set = DominoSet()

        result = domino_set.get_largest_domino().numbers
        answer = [6, 6]
        self.assertEqual(result, answer)

        answer = [6, 5]
        self.assertNotEqual(result, answer)


if __name__ == "__main__":
    unittest.main(verbosity=2)
