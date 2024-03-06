import csv
import pytest
from project import delete_history, format_data, game_selector, history, print_history, remove_duplicates

def test_history():
    games_history = [
        [
            {'question': 'What is the capital of France?', 'user_answer': 'Paris', 'correct_answer': 'Paris', 'correct': True},
            {'question': 'What is the capital of Germany?', 'user_answer': 'Berlin', 'correct_answer': 'Berlin', 'correct': True}
        ],
        [
            {'question': 'What is the capital of Italy?', 'user_answer': 'Rome', 'correct_answer': 'Rome', 'correct': True},
            {'question': 'What is the capital of Spain?', 'user_answer': 'Madrid', 'correct_answer': 'Madrid', 'correct': True}
        ]
    ]

    history(games_history)

    with open('history.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    assert len(rows) == 4
    assert rows[0]['question'] == 'What is the capital of France?'
    assert rows[0]['user_answer'] == 'Paris'
    assert rows[0]['correct_answer'] == 'Paris'
    assert rows[0]['correct'] == 'True'
    assert rows[1]['question'] == 'What is the capital of Germany?'
    assert rows[1]['user_answer'] == 'Berlin'
    assert rows[1]['correct_answer'] == 'Berlin'
    assert rows[1]['correct'] == 'True'
    assert rows[2]['question'] == 'What is the capital of Italy?'
    assert rows[2]['user_answer'] == 'Rome'
    assert rows[2]['correct_answer'] == 'Rome'
    assert rows[2]['correct'] == 'True'
    assert rows[3]['question'] == 'What is the capital of Spain?'
    assert rows[3]['user_answer'] == 'Madrid'
    assert rows[3]['correct_answer'] == 'Madrid'
    assert rows[3]['correct'] == 'True'
    
import os
import pytest
from project import multi_choice_game

def test_multi_choice_game_file_exists(mocker):
    mocker.patch('os.path.isfile', return_value=True)
    mocker.patch('project.multi_game')

    multi_choice_game()

    os.path.isfile.assert_called_once_with("multi_choice.csv")
    assert not os.path.isfile.called
    project.multi_game.assert_called_once()

def test_multi_choice_game_file_not_exists(mocker):
    mocker.patch('os.path.isfile', return_value=False)
    mocker.patch('project.write_mf')
    mocker.patch('project.multi_game')

    multi_choice_game()

    os.path.isfile.assert_called_once_with("multi_choice.csv")
    project.write_mf.assert_called_once_with("multi_choice.csv")
    project.multi_game.assert_called_once()