import config

from text_utils.process_file import process_file
from text_utils.process_text import process_text
from web_utils.text_file_generator import generate_text_file
from game.word_guessing_game import WordGuessingGame
from game.rulesets import RULESETS
from game.statistics import Statistics

# GLOBALS:
# Test wordlist to easily run word_guessing_game() on.
TEST_LIST = ["pain", "piano", "stuffy", "germane", "asteroid", "inflorescence"]
# A Statistics() object for tracking & recording the statistics of a game.
GAME_STATS = Statistics()



def load_word_list(dir_with_texts):
    try:
        while True:
            # Attempt to get valid input text from file.
            input_file_text = process_file(dir_with_texts)

            # If file processing failed, user must choose another file.
            if input_file_text is None:
                continue

            # Attempt to process input text.
            word_list = process_text(input_file_text)

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

    if config.MAIN_DEBUGGER or config.DEBUG_ALL:
        print("***LIST OF VALID WORDS FROM MAIN():***")
        print(word_list)
    
    return word_list
# End of load_word_list()



def load_ruleset():
    # Before starting the game loop, user selects a game mode based on ruleset.
    while True:
        # Display modes with numbers & parantheses: 1), 2), ... etc.
        print("\nAVAILABLE GAME MODES:")
        for key, (mode_name, _) in RULESETS.items():
            print(f"{key}) {mode_name}")

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

    # Load the user-specified ruleset.
    mode_name, ruleset_class = RULESETS[user_input]

    if config.MAIN_DEBUGGER or config.DEBUG_ALL:
        print(f"***CHOSEN RULESET FROM MAIN(): {mode_name}***")
    
    return ruleset_class()
# End of load_ruleset()



def run_game(word_list, ruleset):
    # Loop word_guessing_game so long as the user wants to keep playing.
    while True:
        try:
            if config.MAIN_DEBUGGER or config.DEBUG_ALL:
                # Instantiate a WordGuessingGame object using the global test list.
                this_game = WordGuessingGame(TEST_LIST, ruleset)
            else:
                # Instantiate a WordGuessingGame object using the processed word list.
                this_game = WordGuessingGame(word_list, ruleset)
            
            # Call the actual function to play the game, then store its results (return format is dict).
            game_results = this_game.play_game()
            # Update stats tracker.
            GAME_STATS.record_game(game_results)

            # Ask user if they want to restart.
            restart = input(f"Enter {config.QUIT_CHAR} to quit. Enter any other character(s) to restart the game. ")
            if restart == config.QUIT_CHAR:
                break
        # Try-except block is necessary in the event that the user has played every word in the word list (see choose_word() in word_guessing_game.py).
        except ValueError as err_msg:
            print(err_msg)
            break
    # End of game loop

    GAME_STATS.print_report()
# End of run_game()



def run_crawler():
    seed_url = input("Enter starting URL: ")

    print("\nCrawling website... please wait.\n")

    file_path = generate_text_file(seed_url)

    print(f"\nNew input file created: {file_path}")
# End of run_crawler()



def main():
    print("MAIN MENU\n1) Generate Input File (crawl web)\n2) Play Word Guessing Game\n")
    #user_input = input(f"Choose an option from the main menu or enter {config.QUIT_CHAR} to quit.").strip()

    # Load word list and ruleset.
    word_list = load_word_list(config.TEXTS)
    ruleset = load_ruleset()

    # Run game with given word list and ruleset.
    run_game(word_list, ruleset)
    
    print("\nGoodbye.\n")
# End of main()



if __name__ == "__main__":
    main()
    #run_crawler()
# End of main()