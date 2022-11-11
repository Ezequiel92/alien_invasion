import json
import sys

from menu import Menu
from ranking import *
from user_input import InputBox

####################################################################################################
# Main flow control function for the menus
####################################################################################################


def conff_menu(main_path):
    """
    Initial configuration menus to start a game, show ranking or load up saved
    games and to set up screen size, initial difficulty, and type of user
    """
    repeat = flow_1 = flow_2 = flow_3 = flow_4 = True

    # Set flow variable to normal state.
    def _reset_state():
        nonlocal repeat, flow_1, flow_2, flow_3, flow_4
        repeat, flow_1, flow_2, flow_3, flow_4 = (
            False,
            True,
            True,
            True,
            True,
        )

    while repeat:

        # Start game, show ranking or load up saved games.
        if flow_1:
            _reset_state()
            main_menu = _select_main_action(main_path)
            if main_menu != "new_game":
                # Return store configuration.
                return _game_data(main_path, main_menu)

        # Choose between fullscreen or an small screen.
        if flow_2:
            _reset_state()
            screen_size = _select_screen_size(main_path)
            if screen_size == "Back":
                repeat = True
                flow_3 = False
                flow_4 = False

        # Choose initial difficulty.
        if flow_3:
            _reset_state()
            difficulty = _select_difficulty(main_path)
            if difficulty == "Back":
                repeat = True
                flow_1 = False
                flow_4 = False

        # Select between an old user, entering a new user or playing anonymously.
        if flow_4:
            _reset_state()
            user = _select_user(main_path)
            if user == "Back":
                repeat = True
                flow_1 = False
                flow_2 = False
            elif user == "Stay":
                repeat = True
                flow_1 = False
                flow_2 = False
                flow_3 = False

            # Returns user selected configuration.
            else:
                return (user, difficulty, screen_size, None)


####################################################################################################
# Menu functions
####################################################################################################


def _select_main_action(main_path):
    """Menu for the selection of main action"""

    # Stay in start menu?
    start_menu = True
    while start_menu:
        start_menu = False
        menu = Menu(
            main_path,
            ["Start game", "Saved games", "Ranking", "Exit"],
            "Alien Invasion",
            back=False,
        )
        action = menu.run_menu()

        if action == "Start game":
            # Go to next menu.
            return "new_game"
        elif action == "Saved games":
            # Choose and load saved games.
            saved_game = _select_saved_games(main_path)
            if saved_game:
                return saved_game
            else:
                start_menu = True
        elif action == "Ranking":
            # Show user ranking.
            _show_ranking(main_path)
            start_menu = True
        elif action == "Exit":
            # Exit game.
            sys.exit()


def _select_screen_size(main_path):
    """Menu for the selection of screen size"""
    menu = Menu(
        main_path,
        ["Small Screen", "Full Screen"],
        "Choose screen size",
    )
    size = menu.run_menu()

    return size


def _select_difficulty(main_path):
    """Menu for the selection of initial difficulty"""
    menu = Menu(main_path, ["Easy", "Medium", "Hard"], "Choose difficulty")
    diff = menu.run_menu()

    # Setting for different difficulties:
    # (Initial alien speed, Initial bullet speed, Initial ship speed).
    if diff == "Hard":
        return (2, 4, 2.5)
    elif diff == "Medium":
        return (1.5, 3.5, 2)
    elif diff == "Easy":
        return (1, 3, 1.5)
    else:
        # Go back.
        return diff


def _select_user(main_path):
    """Menu for the selection of type of user"""

    # Get list of saved users.
    old_user_filename = main_path + "user_data/high_scores.json"
    try:
        with open(old_user_filename) as f:
            # List of old user.
            old_users = list(json.load(f).keys())
    except FileNotFoundError:
        # The list of old users is empty.
        old_users = []

    # User selection menu.
    if old_users:
        options = ["New User", "Old User", "Anonymous"]
    else:
        options = ["New User", "Anonymous"]
    menu = Menu(main_path, options, "Choose user")
    user = menu.run_menu()

    if user == "New User":
        # New User: Ask for name of new user.
        new_user = _get_new_user(main_path, old_users)
        if new_user == "Back":
            return "Stay"
        else:
            return new_user
    elif user == "Old User":
        # Old User: Show list of old users to select one.
        old_user = _get_old_user(main_path, old_users)
        if old_user == "Back":
            return "Stay"
        else:
            return old_user
    elif user == "Anonymous":
        # Anonymous: Doesn't store high score in file.
        return "anon"
    else:
        # Back
        return user


####################################################################################################
# Auxiliary functions.
####################################################################################################


def _show_ranking(main_path):
    """Show the stored users in a ranking by their scores"""
    high_scores_filename = main_path + "user_data/high_scores.json"

    try:
        with open(high_scores_filename) as f:
            # Stored users and their scores.
            high_scores = json.load(f)
    except FileNotFoundError:
        high_scores = None

    if high_scores:
        # Sort and complete data.
        scores = sort_scores(high_scores)
        scores = set_date_and_idx(scores)

        # Add title row.
        scores.insert(0, ["#", "User:", "High score:", "Lives left:", "Date:"])

        # Construct nice row string.
        max_len = get_max_len(scores, [0, 1, 2, 3, 4])
        rows = []
        for item in scores:
            rows.append(get_str_for_ranking(item, max_len))

        # Construct full dictionary for Menu class.
        first_row = {rows[0]: {"t_size": 25, "b_width": "auto"}}
        ranking = dict.fromkeys(
            rows[1:],
            {"b_color": (230, 230, 230), "t_size": 25, "b_width": "auto"},
        )
        rows = {**first_row, **ranking}
        menu = Menu(main_path, rows, "Ranking", click=False)
    else:
        menu = Menu(
            main_path,
            {"There are no ranked scores yet": {"b_color": (230, 230, 230)}},
            "Ranking",
            click=False,
        )

    menu.run_menu()


def _select_saved_games(main_path):
    """Displays saved games and allows to choose one to load up"""
    saved_games_filename = main_path + "user_data/saved_games.json"

    try:
        with open(saved_games_filename) as f:
            saved_games = json.load(f)
    except FileNotFoundError:
        saved_games = None

    if saved_games:
        rows = _get_saved_games_str(saved_games)
        users = dict.fromkeys(rows, {"b_width": "auto"})
        menu = Menu(main_path, users, "Saved games")
    else:
        menu = Menu(
            main_path,
            {"No saved games yet": {"b_color": (230, 230, 230)}},
            "Ranking",
            click=False,
        )
    saved_game = menu.run_menu()

    if saved_game == "Back":
        return None
    else:
        return _get_saved_game_key(saved_game)


def _get_saved_games_str(saved_games):
    """
    Constructs the string to show as a button
    representing the saved game: "username date"
    """

    usernames_and_dates = list(saved_games.keys())

    # The username part is the string - (date part).
    usernames = [item[:-19] for item in usernames_and_dates]

    # 17 + 2 is the length of the date part of the string: (YYYY-MM-DD, HH:MM).
    dates = [item[-18:-1] for item in usernames_and_dates]

    max_len = len(max(usernames, key=len))
    whitespaces = [max_len - len(username) for username in usernames]
    sep = ["".join(" " for j in range(space)) for space in whitespaces]
    rows = [f"{usernames[i]}{sep[i]}  {dates[i]}" for i in range(len(dates))]

    return rows


def _get_saved_game_key(saved_game):
    """
    From the string generated by _get_saved_games_str:
    "username + *some white space* + date (len = 17)"
    reconstructs the original key use to store the saved game:
    "username + *one space* + (date)"
    """
    date = saved_game[-17:]
    username = saved_game[:-17].rstrip()

    return f"{username}({date})"


def _game_data(main_path, key):
    """Get a saved game instance"""

    saved_games_filename = main_path + "user_data/saved_games.json"

    # If this function is executed, the file exist.
    with open(saved_games_filename) as f:
        saved_games = json.load(f)
        game = saved_games[key]

        # (Username, Initial difficulty, Screen size, Rest of game state)
        return (game["user"], game["ini_diff"], game["screen_size"], game)


def _get_old_user(main_path, old_users):
    """Show old user options"""

    buttons = old_users

    # Create and show old users menu.
    old_user_menu = Menu(main_path, buttons, "Old users")
    user_selected = old_user_menu.run_menu()

    return user_selected


def _get_new_user(main_path, old_users):
    """Ask for new user name"""

    input_box = InputBox(main_path, old_users)
    new_user = input_box.run_menu()
    if new_user == "Back":
        return "Back"

    # Construct high_scores list element for the new user.
    old_user_filename = main_path + "user_data/high_scores.json"
    new_user_dict = {
        "high_score": 0,
        "lives_left": None,
        "max_level": 1,
        "date": None,
    }

    # Add new user to high score list.
    try:
        with open(old_user_filename) as f:
            user_list = json.load(f)
            user_list[new_user] = new_user_dict
    except FileNotFoundError:
        user_list = {new_user: new_user_dict}
    finally:
        with open(old_user_filename, "w") as f:
            json.dump(user_list, f)
    return new_user
