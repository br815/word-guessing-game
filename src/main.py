from pathlib import Path
from text_utils.process_file import process_file
from text_utils.process_text import process_text
from game.word_guessing_game import WordGuessingGame
from game.rulesets import (
    PointsRuleSet,
    LivesRuleSet,
    CountdownRuleSet
)
from game.statistics import Statistics
import config

# GLOBALS:
# Path to this repo's root.
REPO_ROOT = Path(__file__).resolve().parent.parent
# Test wordlist to easily run word_guessing_game() on.
TEST_LIST = ["callous", "germane"]
# ...
SESSION_STATS = Statistics()



if __name__ == "__main__":
    # Provide the path to the sub-directory with input files.
    dir_with_texts = REPO_ROOT / "texts"

    try:
        while True:
            # Attempt to get valid input text from file.
            text_in = process_file(dir_with_texts)

            # If file processing failed, user must choose another file.
            if text_in is None:
                continue

            # Attempt to process input text.
            word_list = process_text(text_in)

            # If text processing failed, user must choose another file.
            if word_list is None:
                continue

            # Valid word list generated.
            break
        # End of user input validation loop
    # Try-except block is necessary in the event that the provided directory does not exist (see select_file_from_dir() in process_file.py).
    except FileNotFoundError as err_msg:
        print(err_msg)
        exit()

    if config.PROJECT_DEBUGGER or config.MAIN_DEBUGGER:
        print("***LIST OF VALID WORDS FROM MAIN():***")
        print(word_list)

    # Before starting the game loop, user selects a game mode based on ruleset.
    print("\nSelect a game mode:")
    print("1. Points Mode")
    print("2. Lives Mode")
    print("3. Countdown Mode")
    game_mode = input("Selection: ")
    if game_mode == "2":
        ruleset = LivesRuleSet()
    elif game_mode == "3":
        ruleset = CountdownRuleSet()
    else:
        ruleset = PointsRuleSet()

    # Loop word_guessing_game so long as the user wants to keep playing.
    while True:
        try:
            if config.PROJECT_DEBUGGER or config.MAIN_DEBUGGER:
                # Instantiate a WordGuessingGame object using the global test list.
                print("***TEST LIST FROM MAIN():***")
                print(TEST_LIST)
                game = WordGuessingGame(TEST_LIST, ruleset)
            else:
                # Instantiate a WordGuessingGame object using the processed word list.
                game = WordGuessingGame(word_list, ruleset)
            
            # Call the actual game function and store its results.
            game_results = game.play()
            # Update stats tracker.
            SESSION_STATS.record_game(game_results)

            # Ask user if they want to restart.
            restart = input(f"Enter {config.QUIT_CHAR} to quit. Enter any other character(s) to restart the game. ")
            if restart == config.QUIT_CHAR:
                break
        # Try-except block is necessary in the event that the user has played every word in the word list (see choose_word() in word_guessing_game.py).
        except ValueError as err_msg:
            print(err_msg)
            break
    # End of game loop
    
    print("Goodbye.")
    SESSION_STATS.print_report()



# End of main()