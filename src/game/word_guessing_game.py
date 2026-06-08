import re
from random import randint

from config import QUIT_CHAR


class WordGuessingGame:
    """
    Main game class.
    """

    def __init__(
        self,
        word_list,
        ruleset
    ):

        self.word_list = word_list
        self.ruleset = ruleset

        self.word = None

        self.display = None

        self.value = None

        self.guesses = []
    




    def choose_word(self):

        if len(self.word_list) == 0:

            raise ValueError(
                "Congratulations! "
                "You have played every word "
                "available in the word list."
            )

        index = randint(
            0,
            len(self.word_list) - 1
        )

        self.word = self.word_list.pop(index)

        self.display = [
            '_'
            for _
            in self.word
        ]

        self.value = (
            self.ruleset.initial_value()
        )

        self.guesses = []
    





    def display_game_state(self):

        print()

        print(
            ' '.join(self.display)
        )

        print(
            f"{self.ruleset.display_label()}: "
            f"{self.value}"
        )

        print(
            "Guesses:",
            ' '.join(self.guesses)
        )





    def get_valid_guess(self):

        while True:

            guess = input(
                "Guess a letter: "
            ).lower()

            if guess == QUIT_CHAR:
                return guess

            if not re.fullmatch(
                r"[a-z]",
                guess
            ):

                print(
                    "Please enter "
                    "one letter (a-z)."
                )

                continue

            if guess in self.guesses:

                print(
                    "Please enter a letter "
                    "you haven't already guessed."
                )

                continue

            return guess






    def apply_guess(
        self,
        guess
    ):

        occurrences = 0

        for i in range(len(self.word)):

            if self.word[i] == guess:

                self.display[i] = guess

                occurrences += 1

        return occurrences









    def print_guess_result(
        self,
        correct_guess,
        occurrences
    ):

        if correct_guess:

            plural = ""

            if occurrences > 1:
                plural = "s"

            print(
                f"Right! "
                f"You found "
                f"{occurrences} occurrence"
                f"{plural}."
            )

        else:

            print(
                "Incorrect guess."
            )

        print(
            f"{self.ruleset.display_label()}: "
            f"{self.value}"
        )









    '''def completion_percent_all(self):
        """
        Percentage of ALL letters discovered.
        """

        revealed_letters = sum(
            1
            for char
            in self.display
            if char != '_'
        )

        return (
            revealed_letters
            / len(self.word)
        ) * 100 '''






    def completion_percent_unique(self):
        """
        Percentage of unique letters discovered.
        """

        unique_letters_in_word = len(
            set(self.word)
        )

        discovered_letters = len(
            set(self.display) - {'_'}
        )

        return (
            discovered_letters
            / unique_letters_in_word
        ) * 100






    def get_result(self):

        if '_' not in self.display:

            return "WIN"

        if self.ruleset.has_lost(
            self.value
        ):

            return "LOSS"

        return None








    def play(self):

        self.choose_word()

        self.ruleset.print_rules()

        result = None

        while True:

            self.display_game_state()

            guess = self.get_valid_guess()

            if guess == QUIT_CHAR:

                print(
                    f'The word was "{self.word}".'
                )

                result = "QUIT"

                break

            self.guesses.append(
                guess
            )

            occurrences = (
                self.apply_guess(
                    guess
                )
            )

            correct_guess = (
                occurrences > 0
            )

            self.value = (
                self.ruleset.update(
                    self.value,
                    correct_guess,
                    occurrences
                )
            )

            self.print_guess_result(
                correct_guess,
                occurrences
            )

            result = self.get_result()

            if result == "WIN":

                print(
                    f'\nCongratulations! '
                    f'You solved '
                    f'"{self.word}"!'
                )

                break

            if result == "LOSS":

                print(
                    '\nYou lost.'
                )

                print(
                    f'The word was '
                    f'"{self.word}".'
                )

                break

        return {
            "mode": self.ruleset.display_label(),
            "result": result,
            "score": self.value,
            "guesses": len(
                self.guesses
            ),
            "completion":
                self.completion_percent_unique()
        }