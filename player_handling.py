def read_score_for(player):
    for player_dict in players:
        if  player_dict['name'] == player:
            if 'score' in player_dict:
                return player_dict['score']
            else:
                return "no score"


def add_score_for(player, score):
    for player_dict in players:
        if player_dict['name'] == player:
            if 'score' in player_dict:
                player_dict['score'] += score
            else:
                player_dict['score'] = score


def read_what_round_is(player):
    for player_dict in players:
        if player_dict['name'] == player:
            if 'round' in player_dict:
                return player_dict['round']



def add_one_round_for(player):
    for player_dict in players:
        if player_dict['name'] == player:
            if 'round' in player_dict:
                player_dict['round'] += 1