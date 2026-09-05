import config
from game.data_types import GameResults
from game.rulesets import Ruleset

import random
import re



class WordGuessingGame:
    """
    Class:	            WordGuessingGame()
	Descr:              This class manages a word guessing game with guess handling, hints, and rule-based scoring.
                        It contains 7 attributes and 13 methods.
                        It is instantiated in main().
    """
    def __init__(self, word_list: list[str], ruleset: Ruleset) -> None:
        self.word_list: list[str] = word_list   # List of potential words to be picked for a game
        self.ruleset: Ruleset = ruleset         # User-specified ruleset that defines the rules of the game

        self.word: str = ""                     # The word picked for the current game
        self.display: list[str] = []            # The displayed (incompleted or completed) word
        self.value: int | None = None           # The user's score being tracked
        self.guesses: list[str] = []            # List of guesses the user has inputted so far (counts only hints & valid input, not repeat guesses or invalid input)
        self.hints_remaining: int = -1          # Number of hints the player can use up
    # End of init()



    def choose_word(self) -> None:
        """
        Function 1:	        choose_word()
	    Descr:              This function ...
                            It raises a ValueError if no elements are in the word list. (NO LONGER)
                            It is called by play_game().
	    Param:              N/A.
	    Return:             None.
        """
        # Select a random integer within the range of the word list & retrieve the word at that index.
        index = random.randint(0, len(self.word_list) - 1)
        # Remove the word from the word list so that the same word is never chosen twice across games.
        self.word = self.word_list.pop(index)

        if config.GAME_DEBUGGER or config.DEBUG_ALL:
            print(f"***WORD_LIST FROM CHOOSE_WORD(): {', '.join(self.word_list)}***")
            print(f"***RANDOM WORD POPPED FROM WORD_LIST: {self.word}***")

        # List comprehension to replace every letter in the word with an underscore & set that as the display.
        self.display = [
            '_'
            for _   # The underscore used here is convention to indicate that the loop variable's value is not needed anywhere in the list comprehension.
            in self.word]

        # Retrieve the initial score defined in the given ruleset.
        self.value = (self.ruleset.initial_value())
        # Initialize the list of guesses to an empty list.
        self.guesses = []
    # End of choose_word()



    def display_game_state(self) -> None:
        # Print a header to clearly separate this iteration of the display from the printout of the previous result.
        print(f"{config.BORDER_LEN * "="}")

        print()

        # Display the word in whatever incompleted or completed state it's in, with spaces between every element of the list.
        print(' '.join(self.display))
        # Display the word's length so that the player can easily refer to that information.
        print(f"Total Letters: {len(self.word)}")
        # Display the number of hidden letters so that the player can easily refer to that information.
        print(f"Letters Remaining: {self.display.count('_')}")

        print()

        # Display the player's score, which is named however the given ruleset names it.
        print(f"{self.ruleset.display_name()}: {self.value}")
        # Display the number of hints that the player still has remaining.
        print(f"Hints: {self.hints_remaining}")

        print()

        # Display the list of the player's already-guessed letters.
        print("Guesses:", ' '.join(self.guesses))
    # End of display_game_state()



    def get_valid_guess(self) -> str:
        # Continue looping until the player inputs a valid guess.
        while True:
            guess = input("Guess a letter: ").lower()

            # If the player inputs a special character, return it so that the caller of this function can decide what to do with it.
            if guess == config.QUIT_CHAR or guess == config.HINT_CHAR:
                return guess

            # If player does not input an alphabetic single character, continue to the next iteration.
            if not re.fullmatch(r"[a-z]", guess):
                print("Please enter one letter (a-z).")
                continue
            # If player inputs a letter which has already been guessed, continue to the next iteration.
            if guess in self.guesses:
                print("Please enter a letter you haven't already guessed or revealed through hints.")
                continue

            return guess
    # End of get_valid_guess()



    def apply_guess(self, guess: str) -> int:
        # The number of times a letter may appear in the word.
        occurrences = 0

        for i in range(len(self.word)):
            # Check if the guessed letter exists at any index in the word.
            if self.word[i] == guess:
                # Replace the displayed underscore with the letter.
                self.display[i] = guess
                # Increment the number of occurrences of the letter.
                occurrences += 1

        return occurrences
    # End of apply_guess()



    def print_guess_result(self, guess_is_correct: bool, occurrences: int, guess: str) -> None:
        if guess_is_correct:
            plural = ""
            if occurrences > 1:
                # Should read as "occurrences" if number of occurrences is greater than 1.
                plural = "s"
            print(f"Correct! You found {occurrences} occurrence{plural} of the letter \"{guess}\".")
        else:
            print(f"Sorry, there are no occurrences of the letter \"{guess}\".")

        # Display the new score resulting from the user's guess, whether correct (increased score) or incorrect (decreased score).
        print(f"Updated {self.ruleset.display_name()}: {self.value}")
    # End of print_guess_result()



    def calculate_hints(self) -> int:
        # The number of hints the player deserves is calculated based on the length of the word.
        word_length = len(self.word)

        # 1 hint if the word length caps at the the minimum token length.
        if word_length <= config.MIN_TOK_LEN:
            return 1
        # 2 hints if the word is at most 2 letters greater than the minimum token length.
        if word_length > config.MIN_TOK_LEN and word_length <= (config.MIN_TOK_LEN + 2):
            return 2
        # 3 hints for words any longer than that; consider this the default number of hints.
        return 3
    # End of calculate_hints()



    def get_hint_letter(self) -> str:
        # Set comprehension to remove multiple occurrences from the list of hidden letters, so all have an equal chance to be returned.
        available_letters = {
            self.word[i]
            for i in range(len(self.word))
            if self.display[i] == '_'}
        
        if config.GAME_DEBUGGER or config.DEBUG_ALL:
            print(f"***SET OF AVAILABLE LETTERS:***\n{available_letters}")

        # Randomly pick a letter from the set.
        return random.choice(list(available_letters))
    # End of get_hint_letter()



    def use_hint(self) -> None:
        # First, check that there are even any hints remaining; if not, print an error message and leave the function.
        if self.hints_remaining == 0:
            print("ERROR: No hints remaining.")
            return

        # Get a letter to offer the player as a hint.
        hint_letter = self.get_hint_letter()
        # Call the function that updates the displayed word with this letter.
        self.apply_guess(hint_letter)
        # Add this letter to the list of already-guessed letters so that the player can't guess it again later.
        self.guesses.append(hint_letter)
        # Decrement the number of hints the player has left.
        self.hints_remaining -= 1

        # Print a message indicating the usage of the hint & informing the player how many hints they have left.
        print(f"Hint used! The letter \"{hint_letter}\" was revealed.")
        plural = ""
        if self.hints_remaining != 1:
            # Should read as "hints" if number of hints remaining is 0 or greater than 1.
            plural = "s"
        print(f"You now have {self.hints_remaining} hint{plural} remaining.")
    # End of use_hint()



    def completion_percent_all(self) -> float:
        # List comprehension to calculate percentage of ALL letters revealed, which even includes multiple occurrences.
        # Is a more player-intuitive statistic because it accounts for every individual character the player sees on their display,
        # ie. multiple occurrences of correct letters that occur multiple times
        # and blanks for letters they didn't get, even if those letters occur multiple times.
        revealed_letters = sum(
            1
            for char
            in self.display
            if char != '_')

        completion_percent = (revealed_letters / len(self.word)) * 100
        if config.GAME_DEBUGGER or config.DEBUG_ALL:
            print(f"***COMPLETION PERCENT (ALL): {completion_percent}***")
        
        return completion_percent
    # End of completion_percent_all()



    # Unused completion calculation function. If desired, change calculated completion statistic to call this function instead.
    def completion_percent_unique(self) -> float:
        # List comprehension to calculate percentage of UNIQUE letters revealed,
        # so that player completion only considers the single letters they inputted
        # and is not artificially inflated if those letters occurred more than once.
        unique_letters_in_word = len(set(self.word))
        revealed_letters = len(set(self.display) - {'_'})
        completion_percent = (revealed_letters / unique_letters_in_word) * 100
        
        if config.GAME_DEBUGGER or config.DEBUG_ALL:
            print(f"***COMPLETION PERCENT (UNIQUE): {completion_percent}***")
        
        return completion_percent
    # End of completion_percent_unique()



    def get_result(self) -> str | None:
        # Checks win as no underscores in display, ie. full word is displayed.
        # The same check can be done using ''.join(self.display) == self.word: ie. display with spaces removed matches the full word.
        if '_' not in self.display:
            return "WIN"
        # Checks loss against the definition of a loss as defined in the given ruleset.
        if self.ruleset.has_lost(self.value):
            return "LOSS"
        return None
    # End of get_result()



    def play_game(self) -> GameResults:
        # 1st: Set up the game.
        # Randomly select a word from the wordlist supplied to the object.
        self.choose_word()
        # Determine the number of hints the player can use during this game.
        self.hints_remaining = self.calculate_hints()
        # Print the rules for this game.
        self.ruleset.print_rules()
        # Initialize result to None; over the course of the game, it may change to either WIN, LOSS, or QUIT.
        result = None
        # Initialize a dict for the game results, which will be what this function returns.
        game_results = {}

        # 2nd: Continue looping through player inputs until a break condition is met.
        while True:
            # Start each iteration by displaying all necessary items to be displayed: the incompleted word, the player's score, etc.
            self.display_game_state()
            # Then prompt the player to input their next guess.
            guess = self.get_valid_guess()

            # First make sure the input isn't one of the special characters.
            # If the input is the QUIT character, end the game loop.
            if guess == config.QUIT_CHAR:
                print(f"The word was \"{self.word}\".")
                result = "QUIT"
                break
            # If the input is the HINT character, use a hint.
            elif guess == config.HINT_CHAR:
                self.use_hint()
            # Otherwise, handle the input like a valid guess.
            else:
                # Add guess to the list of already-guessed letters.
                self.guesses.append(guess)
                # Try to apply the guess to the word. Occurrences will be > 0 if the guess exists anywhere in the word.
                occurrences = (self.apply_guess(guess))
                # Create a boolean determining whether the player's guess is a correct one (ie. occurs at least once).
                if occurrences > 0:
                    guess_is_correct = True
                else:
                    guess_is_correct = False
                # Update the player's score according to the update() function in the given ruleset.
                self.value = (self.ruleset.update(self.value, guess_is_correct, occurrences))
                # Inform the player if their guess was correct or not.
                self.print_guess_result(guess_is_correct, occurrences, guess)

            # Check if the game has been won or lost after this current iteration's guess or hint.
            result = self.get_result()

            if result == "WIN":
                # Display the final state of the game (ie. solved word, final score, etc) for the player.
                self.display_game_state()
                print(f"\nCongratulations! You solved \"{self.word}\"!")
                break
            if result == "LOSS":
                print(f"\nYou lost. The word was \"{self.word}\".")
                break

        if config.GAME_DEBUGGER or config.DEBUG_ALL:
            print("***DISPLAYING BOTH COMPLETION PERCENTS:***")
            self.completion_percent_all()
            self.completion_percent_unique()
            print()

        # Fill out the return dict with the statistics of the game (intended to be compatible with record_game() in the Statistics class).
        game_results = {
            "mode": self.ruleset.display_name(),
            "word": self.word,
            "result": result,
            "score": self.value,
            "guesses": len(self.guesses), 
            "completion": self.completion_percent_all()}
        
        return game_results
    # End of play_game()
# End of WordGuessingGame() class
