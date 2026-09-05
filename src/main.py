import config
from game.rulesets import RULESETS, Ruleset
from game.statistics import Statistics
from game.word_guessing_game import WordGuessingGame
from text_utils.process_file import process_file
from text_utils.process_text import process_text
from web_utils.generate_texts import generate_text_file



def load_word_list(words_played_set: set[str], dir_with_texts: str | None = None, word_list: list[str] | None = None) -> list[str] | None:
    # If the test list has not been provided, generate a word list from a user-chosen input file.
    if word_list is None:
        # Try-except block is necessary in case of potential file-handling errors (see select_file_from_dir() in process_file.py).
        try:
            while True:
                # Attempt to get valid raw text from input file.
                raw_text_file_name, raw_text = process_file(dir_with_texts)

                # If file processing failed, return to caller.
                if raw_text is None:
                    return None

                # Attempt to process raw text.
                word_list = process_text(raw_text_file_name, raw_text)

                # If text processing failed, return to caller.
                if word_list is None:
                    return None

                # Valid word list generated.
                break
            # End of user input validation loop
        except FileNotFoundError as err_msg:
            print(err_msg)
            return

    # Filter out words that have already been played in this session (ie. across all chosen input files, or across all loads of the test list).
    word_list = [
        word
        for word in word_list
        if word not in words_played_set]

    return word_list
# End of load_word_list()



def load_ruleset() -> Ruleset:
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
    _, ruleset_class = RULESETS[user_input]
    
    return ruleset_class()
# End of load_ruleset()



def run_game(this_session: Statistics) -> None:
    # Load word list.
    if config.MAIN_TEST_LIST_DEBUGGER or config.DEBUG_ALL:
        word_list = load_word_list(this_session.words_played, word_list=config.TEST_LIST)
        print("***LIST OF TEST WORDS FROM MAIN():***")
        print(word_list)
    else:
        word_list = load_word_list(this_session.words_played, dir_with_texts=config.TEXTS)
        if config.MAIN_WORD_LIST_DEBUGGER or config.DEBUG_ALL:
            print("***LIST OF VALID INPUT FILE WORDS FROM MAIN():***")
            print(word_list)

    # "None" means: the input file itself contained only invalid words (ie. it could not produce a valid word list):
    if word_list is None:
        return
    # "not" means: the input file contained valid words, but its word list is empty (ie. every word in it has already been played this session):
    if not word_list:
        print("Congratulations! You have played every word available in this word list.")
        return

    # Load ruleset.
    ruleset = load_ruleset()
    if config.MAIN_TEST_LIST_DEBUGGER or config.MAIN_WORD_LIST_DEBUGGER or config.DEBUG_ALL:
        print(f"***CHOSEN RULESET FROM MAIN(): {ruleset.display_name()}***")

    # Instantiate a WordGuessingGame object on the given word list and ruleset.
    this_game = WordGuessingGame(word_list, ruleset)
    # Call the actual function to play the game, then store its results (return format is dict).
    game_results = this_game.play_game()
    # Update stats tracker.
    this_session.record_game(game_results)
# End of run_game()



def run_crawler() -> None:
    seed_url = input("Enter starting URL: ").strip()

    # User input validation loop.
    while True:
        user_input = input(f"Enter a number of webpages to collect (maximum {config.MAX_WEBPAGES}): ").strip()

        # Case 1: input is not int only.
        if not user_input.isdigit():
            print("ERROR: Input must be within valid range and contain no other characters.")
            continue

        # If this point has been reached, input must be an int and can be cast as such.
        webpage_count = int(user_input)

        # Case 2: int is out of range.
        if webpage_count < 1 or webpage_count > config.MAX_WEBPAGES:
            print(f"ERROR: {webpage_count} is outside valid range.")
            continue

        # Valid input received.
        break
    # End of user input validation loop

    print("\nCrawling website...\n")

    # Try-except block is necessary in case no webpages could be collected (see generate_text_file() in generate_texts.py).
    try:
        file_path = generate_text_file(seed_url, webpage_count)
    except ValueError as err_msg:
        print(err_msg)
        return

    print(f"\nNew text file created: {file_path}")
# End of run_crawler()



def main() -> None:
    # Instantiate a Statistics object to track & record the statistics of all games played during the current session.
    this_session = Statistics()

    # Main menu loop.
    while True:
        # ...
        print(f"\nMAIN MENU\n1) Generate Input File (web crawler)\n2) Play Word Guessing Game\n{config.QUIT_CHAR}) Quit")
        
        user_input = input(f"Choose an option from the main menu or enter {config.QUIT_CHAR} to quit: ").strip()

        if user_input == config.QUIT_CHAR:
            break

        # Case 1: input is not int only.
        if not user_input.isdigit():
            print("ERROR: Input must be from among the options listed.")
            continue

        # If this point has been reached, input must be an int and can be cast as such.
        menu_option = int(user_input)

        # Case 2: int is out of range.
        if menu_option < 1 or menu_option > 2:
            print(f"ERROR: {menu_option} is outside valid range.")
            continue
        # Valid input received.

        # Option 1: run web crawler.
        if menu_option == 1:
            run_crawler()
            continue

        # Option 2: run word guessing game.
        if menu_option == 2:
            run_game(this_session)
            continue
    # End of main menu loop

    # Print the session's statistics report.
    this_session.print_report()
    print("\nGoodbye.\n")
# End of main()



if __name__ == "__main__":
    main()
# End of __main__
