from abc import ABC, abstractmethod
from config import MIN_TOK_LEN


class RuleSet(ABC):
    """
    Abstract base class for all game rule systems.
    """

    @abstractmethod
    def print_rules(self):
        pass

    @abstractmethod
    def initial_value(self):
        pass

    @abstractmethod
    def update(
        self,
        current_value,
        correct_guess,
        occurrences
    ):
        pass

    @abstractmethod
    def has_lost(
        self,
        current_value
    ):
        pass

    @abstractmethod
    def display_label(self):
        pass


class PointsRuleSet(RuleSet):
    """
    Original scoring system.

    Start with MIN_TOK_LEN points.

    Correct:
        + occurrences

    Incorrect:
        -1

    Lose:
        score < 0
    """

    def print_rules(self):

        print("\nPOINTS MODE")
        print(
            f"Start with {MIN_TOK_LEN} points."
        )

        print(
            "Correct guess: "
            "+ number of occurrences."
        )

        print(
            "Incorrect guess: "
            "-1 point."
        )

        print(
            "Lose when score goes below 0."
        )

    def initial_value(self):

        return MIN_TOK_LEN

    def update(
        self,
        score,
        correct_guess,
        occurrences
    ):

        if correct_guess:
            return score + occurrences

        return score - 1

    def has_lost(
        self,
        score
    ):

        return score < 0

    def display_label(self):

        return "Points"


class LivesRuleSet(RuleSet):
    """
    Hangman-style mode.

    Start with 6 lives.

    Correct:
        no change

    Incorrect:
        lose 1 life

    Lose:
        0 lives remaining
    """

    STARTING_LIVES = 6

    def print_rules(self):

        print("\nLIVES MODE")

        print(
            f"Start with "
            f"{self.STARTING_LIVES} lives."
        )

        print(
            "Incorrect guesses "
            "cost one life."
        )

        print(
            "Correct guesses "
            "do not restore lives."
        )

    def initial_value(self):

        return self.STARTING_LIVES

    def update(
        self,
        lives,
        correct_guess,
        occurrences
    ):

        if correct_guess:
            return lives

        return lives - 1

    def has_lost(
        self,
        lives
    ):

        return lives <= 0

    def display_label(self):

        return "Lives"


class CountdownRuleSet(RuleSet):
    """
    Countdown mode.

    Start with 100 points.

    Every guess:
        -5 points

    Lose:
        score <= 0
    """

    STARTING_SCORE = 100
    GUESS_COST = 5

    def print_rules(self):

        print("\nCOUNTDOWN MODE")

        print(
            f"Start with "
            f"{self.STARTING_SCORE} points."
        )

        print(
            f"Every guess costs "
            f"{self.GUESS_COST} points."
        )

        print(
            "Solve the word "
            "before reaching 0."
        )

    def initial_value(self):

        return self.STARTING_SCORE

    def update(
        self,
        score,
        correct_guess,
        occurrences
    ):

        return score - self.GUESS_COST

    def has_lost(
        self,
        score
    ):

        return score <= 0

    def display_label(self):

        return "Countdown"