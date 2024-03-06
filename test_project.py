import unittest
from unittest.mock import patch
from project import multi_game

class TestMultiGame(unittest.TestCase):
    def test_multi_game(self):
        # Test case 1: No questions in the file
        with patch('builtins.input', side_effect=['exit']):
            with patch('sys.exit') as mock_exit:
                multi_game()
                mock_exit.assert_called_once()

        # Test case 2: User answers all questions correctly
        with patch('builtins.input', side_effect=['1', '1', '2', '2', '3', '3', 'exit']):
            with patch('sys.exit') as mock_exit:
                multi_game()
                mock_exit.assert_called_once()

        # Test case 3: User answers some questions incorrectly
        with patch('builtins.input', side_effect=['1', '2', '3', 'exit']):
            with patch('sys.exit') as mock_exit:
                multi_game()
                mock_exit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
