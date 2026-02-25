from display_with_border import *


def update_player_score(player, points_earned):
    """Update a player's score"""
    player['score'] = player['score'] + points_earned
    return player


def display_final_results(players):
    """Display final game results"""
    # Sort players by score, highest first
    sorted_players = []
    for player in players:
        sorted_players.append(player)
    
    # Bubble sort - simple sorting
    for i in range(len(sorted_players)):
        for j in range(len(sorted_players) - 1):
            if sorted_players[j]['score'] < sorted_players[j + 1]['score']:
                # Swap if current is less than next
                temp = sorted_players[j]
                sorted_players[j] = sorted_players[j + 1]
                sorted_players[j + 1] = temp
    frame_top()
    fprint("\n" + "=" * content_width, C.YELLOW)
    fprint(" " * (content_width // 2 - 7) + "FINAL RESULTS", C.RED)
    fprint("=" * content_width + "\n", C.YELLOW)
    
    winner = sorted_players[0]
    winner_name = winner['name']
    winner_score = winner['score']
    
    fprint(f"WINNER: {winner_name} with {winner_score} points!", C.GREEN)
    
    fprint("-" * content_width, C.YELLOW)
    fprint(" " * (content_width // 2 - 6) + "SCOREBOARD", C.GREEN)
    fprint("-" * content_width, C.YELLOW)
    
    position = 1
    for player in sorted_players:
        player_name = player['name']
        player_score = player['score']
        fprint(f"{position}. {player_name:20} Score: {player_score}", C.MAGENTA)
        position += 1
    
    fprint("=" * content_width + "\n", C.YELLOW)
    frame_bottom()
    return winner





if __name__ == "__main__":
    # Test the score functions
    test_players = [
        {'name': 'Mohamed', 'id': 1, 'score': 0},
        {'name': 'Lily', 'id': 2, 'score': 0}
    ]

    # Simulate rounds
    update_player_score(test_players[0], 1)
    update_player_score(test_players[1], 0)
   
    display_final_results(test_players)