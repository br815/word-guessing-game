import config
from abc import ABC, abstractmethod

# GLOBALS:
# Add new rulesets to RULESETS at the end of this file.



class Ruleset(ABC):
    """
    Abstract base class for all game rule systems.
    """
    # Print base rules that apply to all subclasses, ie. how to quit, how to use hints.
    def print_rules(self) -> None:
        print()

        print("=" * config.BORDER_LEN)
        print("WORD GUESSING GAME")
        print("=" * config.BORDER_LEN)
        print("Let's play a word guessing game!")
        print(f"Enter {config.QUIT_CHAR} at any time to quit.")
        print(f"Enter {config.HINT_CHAR} to use a hint.")

        # Then print the rules specific to a subclass.
        self.print_mode_rules()

    # Method defined by Ruleset subclasses for printing mode-specific rules.
    @abstractmethod
    def print_mode_rules(self) -> None:
        pass

    # Method defined by Ruleset subclasses for the displayed mode name.
    @abstractmethod
    def display_name(self) -> str:
        pass

    # Method defined by Ruleset subclasses for the mode-specific starting score.
    @abstractmethod
    def initial_value(self) -> int:
        pass

    # Method defined by Ruleset subclasses for the mode-specific score-updating system.
    @abstractmethod
    def update(self, current_value: int, guess_is_correct: bool, occurrences: int) -> int:
        pass

    # Method defined by Ruleset subclasses for the mode-specific loss condition.
    @abstractmethod
    def has_lost(self, current_value: int) -> bool:
        pass
# End of Ruleset() abstract base class



class PointsRuleset(Ruleset):
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

    def print_mode_rules(self) -> None:
        print("=" * config.BORDER_LEN)
        print("INSTRUCTIONS FOR POINTS MODE")
        print("=" * config.BORDER_LEN)
        print(f"Start with {config.MIN_TOK_LEN} points.")
        print("Correct guesses gain you as many points as that guess occurs in the word.")
        print("Incorrect guesses subtract 1 point from your score.")
        print("You win if you correctly guess all the letters. You lose if your score goes below 0.")

    def display_name(self) -> str:
        return "Points"

    def initial_value(self) -> int:
        # The number of points starts at the minimum length of a token in the wordlist.
        return config.MIN_TOK_LEN

    def update(self, score: int, guess_is_correct: bool, occurrences: int) -> int:
        if guess_is_correct:
            # A correct guess increments the score by the number of times that guess appears in the word.
            return score + occurrences
        else:
            # An incorrect guess decrements the score by 1 point.
            return score - 1

    def has_lost(self, score: int) -> bool:
        # The lose condition is once the score goes BELOW 0 (ie. reaches -1).
        return score < 0
# End of PointsRuleset() subclass



class LivesRuleset(Ruleset):
    """
    Hangman-style mode.

    Start with 6 lives (symbolizing the head, body, 2 arms, 2 legs).

    Correct:
        no change

    Incorrect:
        lose 1 life

    Lose:
        0 lives remaining
    """

    STARTING_LIVES = 6

    def print_mode_rules(self) -> None:
        print("=" * config.BORDER_LEN)
        print("INSTRUCTIONS FOR LIVES MODE")
        print("=" * config.BORDER_LEN)
        print(f"Start with {self.STARTING_LIVES} lives.")
        print("Incorrect guesses cost 1 life.")
        print("Correct guesses do not restore lives.")
        print("You win if you correctly guess all the letters. You lose if you reach 0 lives.")

    def display_name(self) -> str:
        return "Lives"

    def initial_value(self) -> int:
        # The number of lives starts at the maximum amount.
        return self.STARTING_LIVES

    def update(self, lives: int, guess_is_correct: bool, occurrences: int) -> int:
        if guess_is_correct:
            # A correct guess leaves the number of lives unchanged.
            return lives
        else:
            # An incorrect guess uses a life.
            return lives - 1

    def has_lost(self, lives: int) -> bool:
        # The lose condition is if the number of lives goes down to 0.
        return lives <= 0
# End of LivesRuleset() subclass



class CountdownRuleset(Ruleset):
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

    def print_mode_rules(self) -> None:
        print("=" * config.BORDER_LEN)
        print("INSTRUCTIONS FOR COUNTDOWN MODE")
        print("=" * config.BORDER_LEN)
        print(f"Start with {self.STARTING_SCORE} points.")
        print(f"Every guess costs {self.GUESS_COST} points. Points cannot be gained back.")
        print("You win if you correctly guess all the letters. You lose if your score reaches 0.")

    def display_name(self) -> str:
        return "Countdown"

    def initial_value(self) -> int:
        # Score starts at maximum points.
        return self.STARTING_SCORE

    def update(self, score: int, guess_is_correct: bool, occurrences: int) -> int:
        # Score decrements regardless of if a guess is correct or incorrect.
        return score - self.GUESS_COST

    def has_lost(self, score: int) -> bool:
        # The lose condition is if the score goes down to 0.
        return score <= 0
# End of CountdownRuleset() subclass



class StreakRuleset(Ruleset):
    """
    Simple streak mode.

    Correct guess:
        streak += 1

    Wrong guess:
        streak = 0

    No loss condition.
    The player may continue until the word is solved or they choose to quit.
    """

    def print_mode_rules(self) -> None:
        print("=" * config.BORDER_LEN)
        print("INSTRUCTIONS FOR STREAK MODE")
        print("=" * config.BORDER_LEN)
        print("Build the longest streak of correct consecutive guesses you can.")
        print("Correct guesses each add 1 point to your streak.")
        print("Incorrect guesses reset your streak to 0.")
        print(f"There is no loss condition. Enter {config.QUIT_CHAR} at any time to quit.")

    def display_name(self) -> str:
        return "Streak"

    def initial_value(self) -> int:
        # Streak starts at 0.
        return 0

    def update(self, current_value: int, guess_is_correct: bool, occurrences: int) -> int:
        if guess_is_correct:
            # A correct guess increments the streak.
            return current_value + 1
        else:
            # An incorrect guess resets the streak to 0.
            return 0

    def has_lost(self, current_value: int) -> bool:
        # There is no lose condition in this mode; the player can only end the game by quitting.
        return False
# End of StreakRuleset() subclass



# Add new rulesets to this dict after defining their classes (and don't forget to add a comma!).
RULESETS = {"1": ("Points Mode", PointsRuleset),
            "2": ("Lives Mode", LivesRuleset),
            "3": ("Countdown Mode", CountdownRuleset),
            "4": ("Streak Mode", StreakRuleset)}
