# Import required libraries
# Make sure to run `pip install pandas`, `pip install nba-api`, and `pip install matplotlib` in the terminal
# before running this code
import requests
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

class NBAPlayerData:
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

    # Get the player data using player name and season year
    def get_player_data(self, player_name, season):
        player_id = self.get_player_id(player_name)
        if player_id:
            return self.get_season_averages(player_id, season)
        else:
            return None

# Function to get user input for player names and season year
def player_selection():
    player1_name = input("Enter the first player's name: ")
    player1_name = ' '.join([name.capitalize() for name in player1_name.lower().split()])
    player2_name = input("Enter the second player's name: ")
    player2_name = ' '.join([name.capitalize() for name in player2_name.lower().split()])
    season = int(input("Enter the season (year): "))
    return player1_name, player2_name, season

# Main function to run the script
if __name__ == "__main__":
    player_data = NBAPlayerData()
    player1_name, player2_name, season = player_selection()
    player1_data = player_data.get_player_data(player1_name, season)
    player2_data = player_data.get_player_data(player2_name, season)

    # Print the season averages for both players if data is available
    if player1_data is not None and player2_data is not None:
        print(f"\n{player1_name}'s season averages for {season}:")
        for key, value in player1_data.items():
            print(f"{key}: {value}")

        print(f"\n{player2_name}'s season averages for {season}:")
        for key, value in player2_data.items():
            print(f"{key}: {value}")
    else:
        print("One or both players do not have data for the specified season. Please try again.")

