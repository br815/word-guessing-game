from pathlib import Path
from process_file import process_file
from process_text import process_text
from game import word_guessing_game
from game import QUIT_CHAR

# GLOBALS:
# Path to this repo's root.
REPO_ROOT = Path(__file__).resolve().parent.parent
# Boolean for main.py (MAIN) to print debug print statements if desired.
MAIN_DEBUGGER = True
# Test wordlist to easily run word_guessing_game() on.
TEST_LIST = ["callous", "germane"]




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

    if MAIN_DEBUGGER:
        print("***LIST OF VALID WORDS FROM MAIN():***")
        print(word_list)

    cumulative_score = 0
    cumulative_games = 0
    # Loop word_guessing_game so long as the user wants to keep playing.
    while True:
        try:
            if MAIN_DEBUGGER:
                # Call word_guessing_game() on the global test list.
                print("***TEST LIST FROM MAIN():***")
                print(TEST_LIST)
                game_score = word_guessing_game(TEST_LIST)
            else:
                # Call word_guessing_game() on the processed word list.
                game_score = word_guessing_game(word_list)
            
            # Update cumulative trackers.
            cumulative_score += game_score
            cumulative_games += 1
            
            # Ask user if they want to restart.
            restart = input("Enter %s to quit. Enter any other character(s) to restart the game. " %QUIT_CHAR)
            if restart == QUIT_CHAR:
                break
        # Try-except block is necessary in the event that the user has played every word in the word list (see choose_word() in game.py).
        except ValueError as err_msg:
            print(err_msg)
            break
    # End of game loop
    plural = ''
    if cumulative_games > 1:
        plural = 's'
    print(f"You played {cumulative_games} game{plural}. Your cumulative score was "f"{cumulative_score}.")
    print("Goodbye.")



# End of main()