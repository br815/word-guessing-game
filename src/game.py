import re
from random import randint
from process_text import MIN_TOK_LEN


# GLOBALS
QUIT_CHAR = '!'



def choose_word(word_list):
    """
    Chooses and removes a random word.

    Returns:
        chosen word

    Raises:
        ValueError if no words remain.
    """

    if len(word_list) == 0:
        raise ValueError(
            "Congratulations! You have played every word available in the word list."
        )

    index = randint(
        0,
        len(word_list) - 1
    )

    return word_list.pop(index)
# End of choose_word()



def print_rules():
    """
    Display game rules.
    """

    print("\nLet's play a word guessing game! Here are the rules:")

    print("1. You start with 5 points.")

    print(
        "2. When you guess a letter correctly, "
        "you gain as many points as that letter occurs in the word."
    )

    print(
        "3. When you guess a letter incorrectly, "
        "you lose 1 point."
    )

    print(
        "4. You win if you correctly guess all the letters."
    )

    print(
        "5. You lose if your score goes below 0."
    )

    print(
        "6. Enter ! at anytime to quit."
    )
# End of print_rules()



def display_game_state(display, points, guesses):
    """
    Display current game information.
    """

    print()

    print(' '.join(display))

    print("Score:", points)

    print(
    "Guesses:",
    ' '.join(guesses))
# End of display_game_state()



def get_valid_guess(guesses):
    """
    Prompt user until valid input is entered.

    Returns:
        lowercase character
        OR
        QUIT_CHAR
    """

    while True:

        guess = input("Guess a letter: ").lower()

        # Quit condition
        if guess == QUIT_CHAR:
            return guess

        # Input must be exactly one alphabetical character
        if not re.fullmatch(r"[a-z]", guess):

            print("Please enter one letter (a-z).")

            continue

        # Guess must not already exist
        if guess in guesses:

            print(
                "Please enter a letter "
                "you haven't already guessed."
            )

            continue

        return guess
# End of get_valid_guess()



def apply_guess(word, display, guess):
    """
    Reveal guessed letters in display.

    Returns:
        occurrences -> number of matches
    """

    occurrences = 0

    for i in range(len(word)):

        if word[i] == guess:

            display[i] = guess

            occurrences += 1

    return occurrences
# End of apply_guess()



def update_score(points, correct_guess, occurrences):
    """
    Update score according to scoring rules.

    Correct:
        +occurrences

    Incorrect:
        -1
    """

    if correct_guess:

        return points + occurrences

    return points - 1
# End of update_score()



def print_guess_result(correct_guess, occurrences, points):
    """
    Display result of player's guess.
    """

    if correct_guess:

        plural = ""

        if occurrences > 1:
            plural = "s"

        print(
            f"Right! You earned "
            f"{occurrences} point{plural}."
        )

    else:

        print(
            "Sorry, you lost 1 point."
        )

    print(f"Your score is {points}.")
# End of print_guess_result()



def get_game_result(display, points):
    """
    Returns:
        "WIN"
        "LOSS"
        None
    """

    if '_' not in display:
        return "WIN"

    if points < 0:
        return "LOSS"

    return None
# End of get_game_result()



def word_guessing_game(word_list):
    """
    Main game loop.
    """

    # Setup game state
    word = choose_word(word_list)

    display = ['_'] * len(word)
    """
    Create hidden-word display.

    Example:
        "apple" -> ['_', '_', '_', '_', '_']
    """

    points = MIN_TOK_LEN

    guesses = []

    print_rules()

    # Main gameplay loop
    while True:

        # Render current game state
        display_game_state(
            display,
            points,
            guesses
        )

        # Get validated user input
        guess = get_valid_guess(guesses)

        # Quit condition
        if guess == QUIT_CHAR:

            print(f'The word was "{word}".')
            print(f'Your score for this game was {points}.')

            return points

        # Store guess
        guesses.append(guess)

        # Update hidden-word display
        occurrences = apply_guess(
            word,
            display,
            guess
        )

        correct_guess = occurrences > 0

        # Update score
        points = update_score(
            points,
            correct_guess,
            occurrences
        )

        # Display guess result
        print_guess_result(
            correct_guess,
            occurrences,
            points
        )



        result = get_game_result(display, points)

        if result == "WIN":

            display_game_state(
                display,
                points,
                guesses
            )

            print(
                f'\nCongratulations! '
                f'You solved the word "{word}"!'
            )

            print(
                f'Your score for this game was {points}.'
            )

            return points

        elif result == "LOSS":

            print(
                f'\nSorry, your score is {points}.'
            )

            print(
                f'The word was "{word}".'
            )

            return points
# End of word_guessing_game()