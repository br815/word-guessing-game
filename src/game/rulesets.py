import config
from abc import ABC, abstractmethod

# GLOBALS:
# Add new rulesets to RULESETS at the end of this file.



class RuleSet(ABC):
    """
    Abstract base class for all game rule systems.
    """
    # Print base rules that apply to all subclasses, ie. how to quit, how to use hints.
    def print_rules(self):
        print("\n===WORD GUESSING GAME===")
        print("Let's play a word guessing game!")
        print(f"Enter {config.QUIT_CHAR} at any time to quit.")
        print(f"Enter {config.HINT_CHAR} to use a hint.")
        print("=" * 24)
        # Then print the rules specific to a subclass.
        self.print_mode_rules()

    @abstractmethod
    def print_mode_rules(self):
        pass

    @abstractmethod
    def initial_value(self):
        pass

    @abstractmethod
    def update(self, current_value, guess_is_correct, occurrences):
        pass

    @abstractmethod
    def has_lost(self, current_value):
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

    def print_mode_rules(self):
        print("POINTS MODE")
        print(f"Start with {config.MIN_TOK_LEN} points.")
        print("Correct guess: + number of occurrences.")
        print("Incorrect guess: -1 point.")
        print("Lose when score goes below 0.")

    def initial_value(self):
        # The number of points starts at the minimum length of a token in the wordlist.
        return config.MIN_TOK_LEN

    def update(self, score, guess_is_correct, occurrences):
        if guess_is_correct:
            # A correct guess increments the score by the number of times that guess appears in the word.
            return score + occurrences
        else:
            # An incorrect guess decrements the score by 1 point.
            return score - 1

    def has_lost(self, score):
        # The lose condition is once the score goes BELOW 0 (ie. reaches -1).
        return score < 0

    def display_label(self):
        return "Points"



class LivesRuleSet(RuleSet):
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

    def print_mode_rules(self):
        print("LIVES MODE")
        print(f"Start with {self.STARTING_LIVES} lives.")
        print("Incorrect guesses cost one life.")
        print("Correct guesses do not restore lives.")

    def initial_value(self):
        # The number of lives starts at the maximum amount.
        return self.STARTING_LIVES

    def update(self, lives, guess_is_correct, occurrences):
        if guess_is_correct:
            # A correct guess leaves the number of lives unchanged.
            return lives
        else:
            # An incorrect guess uses a life.
            return lives - 1

    def has_lost(self, lives):
        # The lose condition is if the number of lives goes down to 0.
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

    def print_mode_rules(self):
        print("COUNTDOWN MODE")
        print(f"Start with {self.STARTING_SCORE} points.")
        print(f"Every guess costs {self.GUESS_COST} points.")
        print("Solve the word before reaching 0.")

    def initial_value(self):
        # Score starts at maximum points.
        return self.STARTING_SCORE

    def update(self, score, guess_is_correct, occurrences):
        # Score decrements regardless of if a guess is correct or incorrect.
        return score - self.GUESS_COST

    def has_lost(self, score):
        # The lose condition is if the score goes down to 0.
        return score <= 0

    def display_label(self):
        return "Countdown"



class StreakRuleSet(RuleSet):
    """
    Simple streak mode.

    Correct guess:
        streak += 1

    Wrong guess:
        streak = 0

    No loss condition.
    The player may continue until the word is solved or they choose to quit.
    """

    def print_mode_rules(self):
        print("STREAK MODE")
        print("Build the longest streak of consecutive correct guesses possible.")
        print("Each correct guess increases your streak.")
        print("A wrong guess resets your streak to 0.")
        print("There is no loss condition.")
        print("Enter ! at any time to quit.")

    def initial_value(self):
        # Streak starts at 0.
        return 0

    def update(self, current_value, guess_is_correct, occurrences):
        if guess_is_correct:
            # A correct guess increments the streak.
            return current_value + 1
        else:
            # An incorrect guess resets the streak to 0.
            return 0

    def has_lost(self, current_value):
        # There is no lose condition in this mode; the player can only end the game by quitting.
        return False

    def display_label(self):
        return "Streak"



RULESETS = {"1": ("Points Mode", PointsRuleSet),
            "2": ("Lives Mode", LivesRuleSet),
            "3": ("Countdown Mode", CountdownRuleSet),
            "4": ("Streak Mode", StreakRuleSet)

            # Remember to add new rulesets here (don't forget the preceding comma!)
            }