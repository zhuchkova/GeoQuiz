from display_with_border import *


def display_welcome_message():
    frame_top()
    fprint(f"{"#" * 8} Welcome to GeoQuiz {"#" * 8}\n\n", C.RED)
    fprint("A fun and educational game for curious people to expand their world knowledge. Built by the Many Minds team at Masterschool.", C.YELLOW)
    fprint("This multiplayer game allows you to compete with friends for points and bragging rights and learn about our world along the way.", C.YELLOW)
    frame_bottom()


def display_confirmation_message(players_dict):
    user_input = ""
    ready_to_go = False
    validation_passed = False
    allowed_answers = ['Y', 'y', 'N', 'n']
    while not ready_to_go:
        frame_top()
        fprint("Great to meet you, you're going to take turns in a race to the finish line. Let's go!", C.YELLOW)
        for player, name in players_dict.items():
            fprint(f"{player}: {name}", C.MAGENTA)
        frame_bottom()
        while not validation_passed:
            user_input = cinput(f"Ready to start? (Y or N) ")
            if validat_only_contains_list(user_input, allowed_answers):
                validation_passed = True
                break
            error(f"\n'{user_input}' is not a valid input!\n")
        if user_input.upper() == 'N':
            players_dict = get_player_name(get_player_number())
            validation_passed = False
        else:
            ready_to_go = True
    return players_dict


def get_player_number():
    max_players = 3
    validation_passed = False
    while not validation_passed:
        number_of_players = cinput(f"How many players (max. {max_players}) will take part? ")
        if number_of_players.isdigit():
            if validat_only_contains_list(number_of_players, [str(number) for number in range(1, max_players + 1)]):
                validation_passed = True
                break
        error(f"\n'{number_of_players}' is not a valid player number!\n")
    return number_of_players


def get_player_name(number_of_players):
    counter = 0
    player_dict = dict()
    while counter < int(number_of_players):
        player = cinput(f"Enter player {counter + 1}'s name: ")
        player_dict[(f"Player {counter + 1}")] = player
        counter += 1
    return player_dict


def create_player_list(player_dict):
    player_list = []
    for player, name in player_dict.items():
        player_list.append({'name': name, 'id': player, 'score': 0, 'round': 0})
    return player_list


def validat_only_contains_list(input, allowed_chars):
    for char in input:
        if char not in allowed_chars:
            return False
    return True


def initialize_game():
    display_welcome_message()
    player_dict = get_player_name(get_player_number())
    player_dict = display_confirmation_message(player_dict)
    return (create_player_list(player_dict))
