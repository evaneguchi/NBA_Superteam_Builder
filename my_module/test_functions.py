"""Test for my functions.

Note: because these are 'empty' functions (return None), here we just test
  that the functions execute, and return None, as expected.
"""


##
##
from functions import top_5, top_5_balanced, create_team, create_opponent, play_game, final_path
from classes import Team, SuperTeam

def test_top_5():
    """Function does testing on top_5 function"""
    assert top_5('PTS', 'LAL') == ({'Anthony Davis': 26.1, 'LeBron James': 25.3,\
                                    'Kyle Kuzma': 12.8, 'Dion Waiters': 10.766666666666666,\
                                    'Kentavious Caldwell-Pope': 9.3}, [26.1, 25.3, 12.8,\
                                    10.766666666666666, 9.3], 'LAL')
    assert callable(top_5)

def test_top_5_balanced():
    """Function does testing on top_5_balanced function"""
    assert top_5_balanced('AST') == ({'LeBron James': [10.2, 'PG'], 'James Harden':\
                                     [7.5, 'SG'], 'Nikola Jokić': [7.0, 'C'], \
                                    'Draymond Green': [6.2, 'PF'], 'Jimmy Butler':\
                                    [6.0, 'SF']}, [25.3, 34.3, 19.9, 8.0, 19.9])
    assert callable(top_5_balanced)

def test_create_team():
    """Function does testing on create_team function"""
    assert isinstance(create_team('Balanced', 'Points', ''), str)
    assert create_team('Balanced', 'Assists', '') == "\nGreat! You are responsible for the team: Superteam.\nThe players that had the best Assists and who are on your team are: ['LeBron James', 'James Harden', 'Nikola Jokić', 'Draymond Green', 'Jimmy Butler']"
    assert callable(create_team)

def test_create_opponent():
    """Function does testing on create_opponent function"""
    assert isinstance(create_opponent('Los Angeles Lakers'), str)
    assert create_opponent('Los Angeles Lakers') == "\nThe Los Angeles Lakers's "+\
        "players with the best Assists are: ['LeBron James', 'Rajon Rondo',"+\
            " 'Anthony Davis', 'Alex Caruso', 'Dion Waiters']"
    assert callable(create_opponent)

def test_play_game():
    """Function does testing on play_game function"""
    assert callable(play_game)

def test_final_path():
    """Function does testing on final_path function"""
    assert isinstance(final_path('Exit'), str)
    assert final_path('Exit') == '\nOkay, thanks for making your team! Bye!'
    assert callable(final_path)
