import unittest
from Final_Project import NBAPlayerData  # Assuming the original code is saved in a file named Final_Project.py
"""
This module contains unit tests for the NBAPlayerData class in the Final_Project.py file.
"""

class TestNBAPlayerData(unittest.TestCase):

    """
        Set up the test fixture by instantiating the NBAPlayerData object.
     """
    def setUp(self):
        self.player_data = NBAPlayerData()

    """
        Test the get_player_id method by checking the return values for a known player and a nonexistent player.
        """
    def test_get_player_id(self):
        player_id = self.player_data.get_player_id("Lebron James")
        self.assertIsNotNone(player_id)
        self.assertEqual(player_id, 2544)

        player_id = self.player_data.get_player_id("Nonexistent Player")
        self.assertIsNone(player_id)

        """
        Test the get_season_averages method by checking the return values for valid and invalid seasons.
        """
    def test_get_season_averages(self):
        lebron_id = 2544
        season_averages = self.player_data.get_season_averages(lebron_id, 2020)
        self.assertIsNotNone(season_averages)
        self.assertEqual(season_averages["PLAYER_AGE"], 35)

        season_averages = self.player_data.get_season_averages(lebron_id, 1999)
        self.assertIsNone(season_averages)

    """
        Test the get_player_data method by checking the return values for valid and invalid inputs.
        """
    def test_get_player_data(self):
        player_data = self.player_data.get_player_data("Lebron James", 2020)
        self.assertIsNotNone(player_data)
        self.assertEqual(player_data["PLAYER_AGE"], 35)

        player_data = self.player_data.get_player_data("Nonexistent Player", 2020)
        self.assertIsNone(player_data)

        player_data = self.player_data.get_player_data("Lebron James", 1999)
        self.assertIsNone(player_data)

if __name__ == "__main__":
    unittest.main()
