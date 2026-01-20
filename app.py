from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from Final_Project import NBAPlayerData
from nba_api.stats.static import players
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Initialize NBA player data handler
player_data_handler = NBAPlayerData()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200

@app.route('/api/search', methods=['GET'])
def search_players():
    """Search for players by name (autocomplete)"""
    try:
        query = request.args.get('query', '').strip()

        if not query:
            return jsonify([]), 200

        # Search for players
        all_players = players.get_players()
        matching_players = [
            p['full_name'] for p in all_players
            if query.lower() in p['full_name'].lower()
        ]

        # Limit to top 10 results
        return jsonify(matching_players[:10]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/compare', methods=['POST'])
def compare_players():
    """Compare two NBA players for a given season"""
    try:
        data = request.get_json()

        # Validate input
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        player1_name = data.get('player1', '').strip()
        player2_name = data.get('player2', '').strip()
        season = data.get('season')

        # Validation
        if not player1_name or not player2_name:
            return jsonify({
                "success": False,
                "error": "Both player names are required"
            }), 400

        if not season:
            return jsonify({
                "success": False,
                "error": "Season year is required"
            }), 400

        try:
            season = int(season)
        except ValueError:
            return jsonify({
                "success": False,
                "error": "Season must be a valid year"
            }), 400

        if season < 1946 or season > 2025:
            return jsonify({
                "success": False,
                "error": "Season must be between 1946 and 2025"
            }), 400

        # Normalize player names to title case
        player1_name = ' '.join([name.capitalize() for name in player1_name.lower().split()])
        player2_name = ' '.join([name.capitalize() for name in player2_name.lower().split()])

        # Get player data
        player1_data = player_data_handler.get_player_data(player1_name, season)
        player2_data = player_data_handler.get_player_data(player2_name, season)

        # Check if data was found
        if player1_data is None and player2_data is None:
            return jsonify({
                "success": False,
                "error": f"Could not find data for either '{player1_name}' or '{player2_name}' for the {season} season"
            }), 404

        if player1_data is None:
            return jsonify({
                "success": False,
                "error": f"Could not find '{player1_name}' or they did not play in the {season} season"
            }), 404

        if player2_data is None:
            return jsonify({
                "success": False,
                "error": f"Could not find '{player2_name}' or they did not play in the {season} season"
            }), 404

        # Convert pandas Series to dict and handle NaN values
        player1_stats = player1_data.to_dict()
        player2_stats = player2_data.to_dict()

        # Replace NaN with None for JSON serialization
        import math
        for key in player1_stats:
            if isinstance(player1_stats[key], float) and math.isnan(player1_stats[key]):
                player1_stats[key] = None
        for key in player2_stats:
            if isinstance(player2_stats[key], float) and math.isnan(player2_stats[key]):
                player2_stats[key] = None

        # Compare stats and determine leaders
        comparison = {}

        # Points leader
        if player1_stats.get('PTS', 0) > player2_stats.get('PTS', 0):
            comparison['points_leader'] = player1_name
        elif player1_stats.get('PTS', 0) < player2_stats.get('PTS', 0):
            comparison['points_leader'] = player2_name
        else:
            comparison['points_leader'] = 'Tie'

        # Rebounds leader
        if player1_stats.get('REB', 0) > player2_stats.get('REB', 0):
            comparison['rebounds_leader'] = player1_name
        elif player1_stats.get('REB', 0) < player2_stats.get('REB', 0):
            comparison['rebounds_leader'] = player2_name
        else:
            comparison['rebounds_leader'] = 'Tie'

        # Assists leader
        if player1_stats.get('AST', 0) > player2_stats.get('AST', 0):
            comparison['assists_leader'] = player1_name
        elif player1_stats.get('AST', 0) < player2_stats.get('AST', 0):
            comparison['assists_leader'] = player2_name
        else:
            comparison['assists_leader'] = 'Tie'

        # Field Goal Percentage leader
        if player1_stats.get('FG_PCT', 0) > player2_stats.get('FG_PCT', 0):
            comparison['fg_pct_leader'] = player1_name
        elif player1_stats.get('FG_PCT', 0) < player2_stats.get('FG_PCT', 0):
            comparison['fg_pct_leader'] = player2_name
        else:
            comparison['fg_pct_leader'] = 'Tie'

        # Return success response
        return jsonify({
            "success": True,
            "player1": {
                "name": player1_name,
                "stats": player1_stats
            },
            "player2": {
                "name": player2_name,
                "stats": player2_stats
            },
            "comparison": comparison
        }), 200

    except Exception as e:
        # Log the error for debugging
        print(f"Error in compare_players: {str(e)}")
        import traceback
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }), 500

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')

    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
