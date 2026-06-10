import pathlib
import config

from utils.process_file import process_file
from utils.process_text import process_text
from game.word_guessing_game import WordGuessingGame
from game.rulesets import RULESETS
from game.statistics import Statistics

# GLOBALS:
# Path to this repo's root.
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
# Test wordlist to easily run word_guessing_game() on.
TEST_LIST = ["pain", "piano", "stuffy", "germane", "asteroid", "inflorescence"]
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
    while True:
        # Display modes with numbers & parantheses: 1), 2), ... etc.
        print("\nAVAILABLE GAME MODES:")
        for key, (name, _) in RULESETS.items():
            print(f"{key}) {name}")

        user_input = input("Choose a game mode number: ").strip()

        # Case 1: input is not int only.
        if not user_input.isdigit():
            print("ERROR: Input must be within valid range and contain no other characters.")
            continue

        # Case 2: int is out of range.
        if user_input not in RULESETS:
            print(f"ERROR: {user_input} is outside valid range.")
            continue

        # Valid input received.
        break
    # End of user input validation loop

    # Choose user-specified ruleset.
    _, ruleset_class = RULESETS[user_input]
    ruleset = ruleset_class()

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