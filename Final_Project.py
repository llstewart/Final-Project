# Import required libraries
# Make sure to run `pip install pandas`, `pip install nba-api`, and `pip install matplotlib` in the terminal
# before running this code
"""
This script allows users to compare the season averages of two NBA players for a given season.
It retrieves the data from the nba_api library, which is available after running:
    pip install pandas
    pip install nba-api
    pip install matplotlib
"""

import requests
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

class NBAPlayerData:
    """
    A class to retrieve and process NBA player data.
    """

    def __init__(self):
        pass

    # Get the player ID using the player's name
    def get_player_id(self, name):
        player_dict = players.find_players_by_full_name(name)
        if len(player_dict) > 0:
            return player_dict[0]['id']
        else:
            return None

    # Get the season averages for the player using player ID and season year
    """
        Get the season averages for the player using player ID and season year.
        
     """
    def get_season_averages(self, player_id, season):
        career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
        career_data = career_stats.get_data_frames()[0]

        season_data = career_data[career_data['SEASON_ID'] == f'{season - 1}-{str(season)[-2:]}']
        
        if not season_data.empty:
            return season_data.iloc[0]
        else:
            return None

    # Placeholder method for potential data cleaning
    def data_cleaning(self):
        pass

    """
        Get the player data using player name and season year.
        
        Parameters:
        player_name (str): Full name of the player.
        season (int): Season year.
        
        Returns:
        pd.Series: Season averages if available, None otherwise.
    """

    def get_player_data(self, player_name, season):
        player_id = self.get_player_id(player_name)
        if player_id:
            return self.get_season_averages(player_id, season)
        else:
                 return None

#Function that prints user's name and welcome messgae with short program explanation\

def welcome_user():
    while True:
        user_name = input("Enter your Name: ").strip()
        if user_name:
            print(user_name + ", welcome to the NBA Seasonal Average Comparison Program. Please input the names of two players you wish to compare.")
            break
        else:
            print("Error. Please enter your name.")

# Function to get user input for player names and season year
    """
    Function to get user input for player names and season year.
    
    Returns:
    tuple: Player1's name, Player2's name, and the season year.
    """
def player_selection():
    while True:
        player1_name = input("Enter the first player's name: ").strip()
        if player1_name and ' ' in player1_name:
            player1_name = ' '.join([name.capitalize() for name in player1_name.lower().split()])
            break
        else:
            print("Error. Please enter the first player's first and last name.")

    while True:
        player2_name = input("Enter the second player's name: ").strip()
        if player2_name and ' ' in player2_name:
            player2_name = ' '.join([name.capitalize() for name in player2_name.lower().split()])
            break
        else:
            print("Error. Please enter the second player's first and last name.")

    season = int(input("Enter the season (year): "))
    return player1_name, player2_name, season

"""
Below is a function that asks users if they want to compare more players once their first comparison is finished.
"""
def compare_more_players():
    while True:
        user_input = input("Do you want to compare more players? (yes/no): ").lower()
        if user_input == 'yes':
            return True #restart the comparison
        elif user_input == 'no':
            return False #stop
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def compare_points(player1_data, player2_data):
    player1_points = player1_data["PTS"]
    player2_points = player2_data["PTS"]

    if player1_points > player2_points:
        print(f"\n{player1_name} had more points in the season with {player1_points} points.")
    elif player1_points < player2_points:
        print(f"\n{player2_name} had more points in the season with {player2_points} points.")
    else:
        print(f"\n{player1_name} and {player2_name} had the same number of points in the season with {player1_points} points each.")

# Main function to run the script
if __name__ == "__main__":
    player_data = NBAPlayerData()
    welcome = welcome_user()

    while True: #while compare more player functions is true, rerun the program
        player1_name, player2_name, season = player_selection()
        player1_data = player_data.get_player_data(player1_name, season)
        player2_data = player_data.get_player_data(player2_name, season)

        if player1_data is not None and player2_data is not None:
            print(f"\n{player1_name}'s season averages for {season}:")
            for key, value in player1_data.items():
                print(f"{key}: {value}")

            print(f"\n{player2_name}'s season averages for {season}:")
            for key, value in player2_data.items():
                print(f"{key}: {value}")

            compare_points(player1_data, player2_data)

            if not compare_more_players():
                break
        else:
            print("One or both players do not have data for the specified season. Please try again.")