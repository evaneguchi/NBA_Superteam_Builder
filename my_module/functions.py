"""A collection of function for doing my project."""

import tkinter as tk
import pandas as pd
import random as rd

df = pd.read_csv('nbaplayers.csv')

TEAM = None
CHOSEN_STAT = None
OPPONENT = None

class Team():
    """Class that stores top 5 players names, stats and average points per team

    Parameters
    ----------
    players : dict
        Dictionary with keys of names of players as strings and values as average stats per game
    point : list
        List of average points per game as floats
    team : string
        String of team
    """
    def __init__(self, players, point, team):
        self.players = players
        self.point = point
        self.team = team


    def points(self):
        """Generates an estimated total amount of points the Team would score in a game

        Parameters
        ----------
        self.points : list
            Class attribute of average points per game for each player

        Return
        ------
        total : int
            Total amount of estimated points scored
        """
        total = 0

        #Iterate over each player's average points per game
        for plyr_pt in self.point:
            #Create an upper bound for points
            upper = plyr_pt+15
            #Create a lower bound for points that doesn't go negative
            if plyr_pt-15 < 0:
                lower = 0
            else:
                lower = plyr_pt-15
            #Create a random point total that a player could score in a game
            total += rd.triangular(lower, upper, plyr_pt)

        #Change point total to a whole integer
        return int(total)

    def stat(self):
        """Calculates an estimated total amount of the specific stat focused \
            on the Team would acquire in a game

        Parameters
        ----------
        self.players : dict
            Class attribute of average stat per game for each player in a dict

        Return
        ------
        total : int
            Total amount of estimateed stat acquired
        """
        total = 0

        #Check if players dictionary includes position or not
        if isinstance(list(self.players.values())[0], list):
            #Iterate over player's average stats per game
            for plyr_st in self.players.values():
                #Create an upper bound for stat
                upper = plyr_st[0]+3
                #Create a lower bound for stat that doesn't go negative
                if plyr_st[0]-3 < 0:
                    lower = 0
                else:
                    lower = plyr_st[0]-3
                #Create a random stat total that a player could acquire in a game
                total += rd.triangular(lower, upper, plyr_st[0])
        else:
            #Iterate over player's average stats per game as the 0th element
            for plyr_st in self.players.values():
                #Create an upper bound for stat
                upper = plyr_st+3
                #Create a lower bound for stat that doesn't go negative
                if plyr_st-3 < 0:
                    lower = 0
                else:
                    lower = plyr_st-3
                #Create a random stat total that a player could acquire in a game
                total += rd.triangular(lower, upper, plyr_st)

        #Change stat total to a whole integer
        return int(total)


class SuperTeam(Team):
    """Class that stores top 5 players across NBA and inherits attributes from
    Team

    Paramaters
    ----------
    players : dict
        Dictionary with keys of names of players as strings and values as average stats per game
    points : list
        List of average points per game as floats
    team : string, Optional
        String of teamname, default = 'Superteam'
    """
    def __init__(self, players, point, team='Superteam'):
        super().__init__(players, point, team)


def top_5(stat, team=None):
    """Return top 5 players' name, average stat, and points per game for a given stat

    Parameters
    ----------
    stat : string
        The type of stat going to be compared
    team : string, Optional
        Name of team if only one team is desired, default=None

    Return
    ------
    players : dict
        Dictionary with key of players and values of their average stats per game
    points : list
        List of players' average points per game
    """
    players = {}
    points = []

    if team is None:
        #Group and sort players together who were on multiple teams and have
        #different statlines for each team
        top = df.groupby('Player').mean().sort_values(stat, ascending=False)
        for index in range(0, 5):
            #Edits name of player to take out the player's tag
            name = top.index[index].split('\\')[0]
            #Get average stat of player
            spg = top[stat][index]
            #Get average points of player
            ppg = top['PTS'][index]
            #Append player's stats to the players dictionary
            players[name] = spg
            #Append player's points to the points list
            points.append(ppg)
        return players, points
    team_players = []
    #Get all players that have been on the specific team
    for tm_plyr in df.where(df['Tm'] == team).dropna().reset_index(drop=True)['Player']:
        team_players.append(tm_plyr)
    #Sort players based on stat
    sorted_players = df.groupby('Player').mean().sort_values(stat, ascending=False)
    counter = 0
    #While loop that iterates through sorted players until 5 players are added.
    while len(points) < 5:
        #Checks if player is on the desired team
        if sorted_players.index[counter] in team_players:
            #Edits name of player to take out the player's tag
            name = sorted_players.index[counter].split('\\')[0]
            #Get average stat of player
            spg = sorted_players[stat][counter]
            #Get average points of player
            ppg = sorted_players['PTS'][counter]
            #Append player's stats to the players dictionary
            players[name] = spg
            #Append player's points to the points list
            points.append(ppg)
        counter += 1
    return players, points, team


def top_5_balanced(stat):
    """Return top 5 players' name, average stat, and points per game for a given stat.
    Also makes sure one of each position is on the team (No duplicates).

    Parameters
    ----------
    stat : string
        The type fo stat going to be compared

    Return
    ------
    players : dict
        Dictionary of players with values of their average stats per game and position
    points : list
        List of players' average points per game
    """
    players = {}
    points = []
    taken_pos = []
    #Group and sort players together who were on multiple teams and have
    #different statlines for each team
    top = df.groupby('Player').mean().sort_values(stat, ascending=False)

    counter = 0
    #While loop that iterates through top until 5 players are added to players
    while len(points) < 5:
        #Gets position of player
        pos = df[df['Player'].str.contains(top.index[counter].split('\\')[0],\
                                           na=False)]['Pos'].iloc[0].split('-')[0]
        #If position is not taken, player is added to team
        if pos not in taken_pos:
            #Edits name of player to take out player's tag
            name = top.index[counter].split('\\')[0]
            #Get average stat of player
            spg = top[stat][counter]
            #Get average points of player
            ppg = top['PTS'][counter]
            #Append player's stats and position to the players dictionary
            players[name] = [spg, pos]
            #Append player's points to the points list
            points.append(ppg)
            #Records position to not be taken again
            taken_pos.append(pos)
            counter += 1
        else:
            counter += 1
    return players, points


def create_team(bal, stat, name):
    """Run top_5 or top_5_balanced functions to create Superteam with given info
    Preparation for Tkinter GUI

    Parameters
    ----------
    bal : string
        String input from TKinter selection to determine usage of top_5 or top_5_balanced
    stat : string
        String input from TKinter selection to determine which stat to filter with
    name : string
        String input from TKinter entry to make team name
    """
    #Import global variables to be assigned and saved for later use
    global TEAM
    global CHOSEN_STAT
    #Record desired stat to use later
    CHOSEN_STAT = stat
    #Create dictionary to translate stat
    desired_stat = {'Points': 'PTS',
                    'Assists': 'AST',
                    'Rebounds': 'TRB',
                    'Steals': 'STL',
                    'Blocks': 'BLK'}
    #Determine whether or not to assign Superteam a name
    if name == '':
        #If 'Balanced' was chosen, top_5_balanced should be run
        if bal in 'Balanced (One of Each Position)':
            #Determine which stat to use to filter
            balanced = top_5_balanced(desired_stat[stat])
            TEAM = SuperTeam(balanced[0], balanced[1])
        #If 'Unbalanced' was chosen, top_5 should be run
        elif bal in 'Unbalanced (Strictly Top Players)':
            #Determine which stat to use to filter
            unbalanced = top_5(desired_stat[stat])
            TEAM = SuperTeam(unbalanced[0], unbalanced[1])
    else:
        #If 'Balanced' was chosen, top_5_balanced should be run
        if bal in 'Balanced (One of Each Position)':
            #Determine which stat to use to filter
            balanced = top_5_balanced(desired_stat[stat])
            TEAM = SuperTeam(balanced[0], balanced[1], name)
        #If 'Unbalanced' was chosen, top_5 should be run
        elif bal in 'Unbalanced (Strictly Top Players)':
            #determine which stat to use to filter
            unbalanced = top_5(desired_stat[stat])
            TEAM = SuperTeam(unbalanced[0], unbalanced[1], name)
    #Return confirmation messages for user
    return '\nGreat! You are responsible for the team: ' + TEAM.team + '.\nThe players'+\
        ' that had the best ' + stat + ' and who are on your team are: '\
          + str(list(TEAM.players.keys()))


def create_opponent(team):
    """Function to run top_5 with given information.
    Preparation for TKinter GUI

    Parameters
    ----------
    team : string
        String of desired team to filter through
    chosen_stat : string
        Global string of stat to filter with
    """
    #Import global variables to assign and save for later use
    global OPPONENT
    global CHOSEN_STAT
    #Create dictionary to convert user friendly string to dataframe string
    nba_dict = {'Atlanta Hawks': 'ATL',
                'Boston Celtics': 'BOS',
                'Brooklyn Nets': 'BRK',
                'Charlotte Hornets': 'CHO',
                'Chicago Bulls': 'CHI',
                'Cleveland Cavaliers': 'CLE',
                'Dallas Mavericks': 'DAL',
                'Denver Nuggets': 'DEN',
                'Detroit Pistons': 'DET',
                'Golden State Warriors': 'GSW',
                'Houston Rockets': 'HOU',
                'Indiana Pacers': 'IND',
                'Los Angeles Clippers': 'LAC',
                'Los Angeles Lakers': 'LAL',
                'Memphis Grizzlies': 'MEM',
                'Miami Heat': 'MIA',
                'Milwaukee Bucks': 'MIL',
                'Minnesota Timberwolves': 'MIN',
                'New Orleans Pelicans': 'NOP',
                'New York Knicks': 'NYK',
                'Oklahoma City Thunder': 'OKC',
                'Orlando Magic': 'ORL',
                'Philadelphia 76ers': 'PHI',
                'Phoenix Suns': 'PHO',
                'Portland Trail Blazers': 'POR',
                'Sacramento Kings': 'SAC',
                'San Antonio Spurs': 'SAS',
                'Toronto Raptors': 'TOR',
                'Utah Jazz': 'UTA',
                'Washington Wizards': 'WAS'}
    #Create dictionary to convert user friendly string to dataframe string
    stat_dict = {'Points': 'PTS',
                 'Assists': 'AST',
                 'Rebounds': 'TRB',
                 'Steals': 'STL',
                 'Blocks': 'BLK'}
    #Create new team with top_5 function
    new_team = top_5(stat_dict[CHOSEN_STAT], nba_dict[team])
    #Create new Team class with attributes of new_team
    OPPONENT = Team(new_team[0], new_team[1], new_team[2])
    return "\nThe " + team + "'s players with the best " + CHOSEN_STAT + " are: "\
        + str(list(OPPONENT.players.keys()))


def play_game():
    """Simulate game between Superteam and chosen NBA team

    Parameters
    ----------
    team : class
        Superteam class
    opponent : class
        Team class

    Return
    ------
    Printed messages of simulated scores and who won
    """
    #Generate simulation of each team scoring points
    team_pts = TEAM.points()
    oppo_pts = OPPONENT.points()
    #Printed statements that don't need to print out a second line for Points
    if CHOSEN_STAT == 'Points':
        #What to print if Superteam wins
        if team_pts > oppo_pts:
            print('')
            print('With a final score of ' + str(team_pts) + ' to ' + str(oppo_pts)\
                  + ', ' + TEAM.team + ' beat ' + OPPONENT.team + ' by ' +\
                      str(team_pts-oppo_pts) + ' points.')
        #What to print if Team wins
        elif oppo_pts > team_pts:
            print('')
            print('With a final score of ' + str(oppo_pts) + ' to ' + str(team_pts)\
                  + ', ' + OPPONENT.team + ' beat ' + TEAM.team + ' by ' +\
                      str(oppo_pts-team_pts) + ' points.')
        #What to print if there's a tie
        else:
            print('')
            print('The game ended in a tie with a score of ' + str(team_pts) +\
                  ' to ' + str(oppo_pts) + '.')
    #Printed statements that need to print out a second line to show how many
    #of the specified stat each team generated
    else:
        #Generate simulation of each team's amount of the chosen stat
        team_stats = TEAM.stat()
        oppo_stats = OPPONENT.stat()
        #What to print if Superteam wins
        if team_pts > oppo_pts:
            print('')
            print('With a final score of ' + str(team_pts) + ' to ' + str(oppo_pts)\
                  + ', ' + TEAM.team + ' beat ' + OPPONENT.team + ' by ' +\
                      str(team_pts-oppo_pts) + ' points.')
            print('Also, ' + TEAM.team + ' had ' + str(team_stats) + ' ' + CHOSEN_STAT\
                  + ' and ' + OPPONENT.team + ' had ' + str(oppo_stats) + ' ' +\
                      CHOSEN_STAT + '.')
        #What to print if Team wins
        elif oppo_pts > team_pts:
            print('')
            print('With a final score of ' + str(oppo_pts) + ' to ' + str(team_pts)\
                  + ', ' + OPPONENT.team + ' beat ' + TEAM.team + ' by ' +\
                      str(oppo_pts-team_pts) + ' points.')
            print('Also, ' + OPPONENT.team + ' had ' + str(oppo_stats) + ' ' +\
                  CHOSEN_STAT + ' and ' + TEAM.team + ' had ' + str(team_stats)\
                      + ' ' + CHOSEN_STAT + '.')
        #What to print if there's a tie
        else:
            print('')
            print('The game ended in a tie with a score of ' + str(team_pts) +\
                  ' to ' + str(oppo_pts) + '.')
            print('Also, ' + TEAM.team + ' had ' + str(team_stats) + ' ' + CHOSEN_STAT\
                  + ' and ' + OPPONENT.team + ' had ' + str(oppo_stats) + ' ' +\
                      CHOSEN_STAT + '.')


def final_path(option):
    """Function used to execute different functions based on input
    Preparation for TKinter GUI

    Parameters
    ----------
    option : string
        String taken from TKinter that determines what option to run
    """
    if option == 'Create New Team':
        build_team()
    elif option == 'Play Another Game Against '+OPPONENT.team:
        play_game()
    else:
        return '\nOkay, thanks for making your team! Bye!'


def build_team():
    """Funciton used to interact with user to create their own team using different options
    """
    print('Hello GM!')
    print("Let's make your very own NBA Superteam!")
    print('To begin, choose what stat you want to focus on, and if you want 5'+\
          ' different positions (balanced team) or not.')
    print('If desired, type in the teamname you want as well :)')
    input("Press Enter to continue.")

    #Create GUI interface for selecting options for Superteam with TKinter module
    options = tk.Tk()
    #Create title for window
    options.title('Superteam Preferences')
    #Set dimensions for window
    options.geometry('400x450')
    #Create title for the first drop-down option menu
    label1 = tk.Label(options, text='Balanced or Unbalanced')
    label1.pack()
    #Create list of options
    bal_opt = ['Balanced (One of Each Position)', 'Unbalanced (Strictly Top Players)']
    #Set variable type and default value
    variable1 = tk.StringVar(options)
    variable1.set(bal_opt[0])
    #Create drop-down menu with the different options
    set1 = tk.OptionMenu(options, variable1, *bal_opt)
    set1.pack(pady=10)
    #Create title for the second drop-down menu
    label2 = tk.Label(options, text='Type of Stat')
    label2.pack()
    #Create list of options
    stat_opt = ['Points', 'Assists', 'Rebounds', 'Steals', 'Blocks']
    #Set variable type and default value
    variable2 = tk.StringVar(options)
    variable2.set(stat_opt[0])
    #Create drop-down menu with the different options
    set2 = tk.OptionMenu(options, variable2, *stat_opt)
    set2.pack(pady=10)
    #Create title for teamname entry
    label3 = tk.Label(options, text='Teamname (Optional)')
    label3.pack()
    #Create entry box to input name of Superteam
    name = tk.Entry(options)
    name.pack(pady=10)
    #Create submission button that also creates the Superteam once clicked
    button1 = tk.Button(options, text='Submit', command=lambda: \
                        print(create_team(variable1.get(), variable2.get(), name.get())))
    button1.pack()
    #Create instructions to close TKinter window once finished
    label4 = tk.Label(options, text='Once finished and submitted exit out of window')
    label4.pack()
    #Make sure TKinter window gets brought to front of screen
    options.lift()
    options.attributes('-topmost', True)
    #Execute TKinter GUI window
    options.mainloop()

    input('Press Enter to continue.')
    print('')
    print("Let's see how " + TEAM.team + " would do against an NBA team.")
    print('Choose which team you would like to play against.')
    input("Press Enter to continue.")

    #Create GUI interface for selecting which NBA team to play aginst with TKinter module
    nba_teams = tk.Tk()
    #Craete title for window
    nba_teams.title('NBA Teams')
    #Set dimensions for window
    nba_teams.geometry('400x400')
    #Create instructions and who will be chosen from the NBA team
    label5 = tk.Label(nba_teams, text='The top 5 players in chosen stat and'+\
                      ' team will be taken')
    label5.pack(pady=10)
    #Create list of NBA teams
    nba_names = ['Atlanta Hawks',
                 'Boston Celtics',
                 'Brooklyn Nets',
                 'Charlotte Hornets',
                 'Chicago Bulls',
                 'Cleveland Cavaliers',
                 'Dallas Mavericks',
                 'Denver Nuggets',
                 'Detroit Pistons',
                 'Golden State Warriors',
                 'Houston Rockets',
                 'Indiana Pacers',
                 'Los Angeles Clippers',
                 'Los Angeles Lakers',
                 'Memphis Grizzlies',
                 'Miami Heat',
                 'Milwaukee Bucks',
                 'Minnesota Timberwolves',
                 'New Orleans Pelicans',
                 'New York Knicks',
                 'Oklahoma City Thunder',
                 'Orlando Magic',
                 'Philadelphia 76ers',
                 'Phoenix Suns',
                 'Portland Trail Blazers',
                 'Sacramento Kings',
                 'San Antonio Spurs',
                 'Toronto Raptors',
                 'Utah Jazz',
                 'Washington Wizards']
    #Create listbox with NBA teams
    lstbx = tk.Listbox(nba_teams, selectmode='SINGLE')
    lstbx.insert('end', *nba_names)
    lstbx.pack(pady=10)
    #Create submission button that creates team to play
    button2 = tk.Button(nba_teams, text='Submit', command=lambda:\
                        print(create_opponent(lstbx.get(lstbx.curselection()))))
    button2.pack()
    #Create instructions to close TKinter window once finished
    label6 = tk.Label(nba_teams, text='Once finished and submitted exit out of window')
    label6.pack()
    #Make sure TKinter window gets brought to front of screen
    nba_teams.lift()
    nba_teams.attributes('-topmost', True)
    #Execute TKinter GUI window
    nba_teams.mainloop()

    input('Press Enter to simulate a game with ' + OPPONENT.team + '.')
    #Run function to simulate game
    play_game()

    input('Press Enter to continue')

    #Create GUI interface for the final screen asking what the user wants to do
    final = tk.Tk()
    #Create title for window
    final.title('Options')
    #Set dimensions for window
    final.geometry('450x450')
    #Create instructions on what each option means nad that this is final step
    label7 = tk.Label(final, text="You've finished! Select what you would like to do next below.")
    label7.pack(pady=10)
    #Create list of options to select
    final_options = ['Create New Team', 'Play Another Game Against '+OPPONENT.team, 'Exit']
    #Create listbox with options
    final_lstbx = tk.Listbox(final, width='30', selectmode='SINGLE')
    final_lstbx.insert('end', *final_options)
    final_lstbx.pack()
    #Create submission button that executes option chosen
    button3 = tk.Button(final, text='Submit', command=lambda:\
                        print(final_path(final_lstbx.get(final_lstbx.curselection()))))
    button3.pack()
    #Create instructions to close TKinter window once finished
    label6 = tk.Label(final, text='If Creating New Team press Enter to close this'+\
                      ' window and move on.\n Otherwise exit this window once done.')
    label6.pack()
    #Make sure TKinter window gets brought to front of screen
    final.lift()
    final.attributes('-topmost', True)
    #Execute TKinter GUI window
    final.mainloop()


def build_team_jupyter():
    """Funciton used to interact with user on Jupyter to create their own team using different options
    """
    print('Hello GM!')
    print("Let's make your very own NBA Superteam!")
    print('To begin, choose what stat you want to focus on, and if you want 5'+\
          ' different positions (balanced team) or not.')
    print('If desired, type in the teamname you want as well :)')
    bal_unbal = input('Please type either "Balanced" or "Unbalanced".')
    type_stat = input('Please type either "Points", "Assists", "Rebounds", "Steals", or "Blocks".')
    opt_name = input("Type in desired teamname. If you don't want one, press enter")

    #Check if input is correct
    correct = 0
    while correct < 1:
        if bal_unbal in ['Balanced', 'Unbalanced'] and type_stat in ['Points', 'Rebounds', 'Assists', 'Steals', 'Blocks']:
            print(create_team(bal_unbal, type_stat, opt_name))
            correct += 1
        else:
            print('')
            print('Uh oh, your inputs did not exatcly match the options. Please type in the correct inputs.')
            bal_unbal = input('Please type either "Balanced" or "Unbalanced".')
            type_stat = input('Please type either "Points", "Assists", "Rebounds", "Steals", or "Blocks".')
            opt_name = input("Type in desired teamname. If you don't want one, press enter")

    input('Press Enter to continue.')
    print('')
    print("Let's see how " + TEAM.team + " would do against an NBA team.")
    print('Choose which team you would like to play against. Please type out'+\
          ' the team exactly how it is printed below.')
    input('Press Enter to see NBA teams.')
    nba_names = ['Atlanta Hawks',
                 'Boston Celtics',
                 'Brooklyn Nets',
                 'Charlotte Hornets',
                 'Chicago Bulls',
                 'Cleveland Cavaliers',
                 'Dallas Mavericks',
                 'Denver Nuggets',
                 'Detroit Pistons',
                 'Golden State Warriors',
                 'Houston Rockets',
                 'Indiana Pacers',
                 'Los Angeles Clippers',
                 'Los Angeles Lakers',
                 'Memphis Grizzlies',
                 'Miami Heat',
                 'Milwaukee Bucks',
                 'Minnesota Timberwolves',
                 'New Orleans Pelicans',
                 'New York Knicks',
                 'Oklahoma City Thunder',
                 'Orlando Magic',
                 'Philadelphia 76ers',
                 'Phoenix Suns',
                 'Portland Trail Blazers',
                 'Sacramento Kings',
                 'San Antonio Spurs',
                 'Toronto Raptors',
                 'Utah Jazz',
                 'Washington Wizards']
    print('')
    for nba_team in nba_names:
        print(nba_team)
    opponent_name = input("Type in desired team to continue.")

    new_correct = 0
    while new_correct < 1:
        if opponent_name in nba_names:
            print(create_opponent(opponent_name))
            new_correct += 1
        else:
            print('')
            print('Uh oh, your input did not exactly match the options above.'+\
                  ' Please type in the teamname exactly how it was above.')
            opponent_name = input("Type in desired team to continue.")

    input('Press Enter to simulate a game with ' + OPPONENT.team + '.')
    #Run function to simulate game
    play_game()

    input('Press Enter to continue')

    print('')
    print('Congratulations, you finished creating your team! Try starting'+\
          ' over and creating another team if you want!')
