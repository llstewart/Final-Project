import unittest
from Final_Project import NBAPlayerData  # Assuming the original code is saved in a file named nba_player_data.py

class TestNBAPlayerData(unittest.TestCase):

    def setUp(self):
        self.player_data = NBAPlayerData()

    def test_get_player_id(self):
        player_id = self.player_data.get_player_id("LeBron James")
        self.assertIsNotNone(player_id)
        self.assertEqual(player_id, 2544)

        player_id = self.player_data.get_player_id("Nonexistent Player")
        self.assertIsNone(player_id)

    def test_get_season_averages(self):
        lebron_id = 2544
        season_averages = self.player_data.get_season_averages(lebron_id, 2020)
        self.assertIsNotNone(season_averages)
        self.assertEqual(season_averages["PLAYER_AGE"], 35)

        season_averages = self.player_data.get_season_averages(lebron_id, 1999)
        self.assertIsNone(season_averages)

    def test_get_player_data(self):
        player_data = self.player_data.get_player_data("LeBron James", 2020)
        self.assertIsNotNone(player_data)
        self.assertEqual(player_data["PLAYER_AGE"], 35)

        player_data = self.player_data.get_player_data("Nonexistent Player", 2020)
        self.assertIsNone(player_data)

        player_data = self.player_data.get_player_data("LeBron James", 1999)
        self.assertIsNone(player_data)

if __name__ == "__main__":
    unittest.main()
