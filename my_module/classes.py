"""Classes used throughout project"""

import random as rd

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
                upper = plyr_st+3
                #Create a lower bound for stat that doesn't go negative
                if plyr_st-3 < 0:
                    lower = 0
                else:
                    lower = plyr_st-3
                #Create a random stat total that a player could acquire in a game
                total += rd.triangular(lower, upper, plyr_st)
        else:
            #Iterate over player's average stats per game as the 0th element
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
