import config
from abc import ABC, abstractmethod



class RuleSet(ABC):
    """
    Abstract base class for all game rule systems.
    """
    # Print base rules about ! and ?
    def print_rules(self):
        print("\n---WORD GUESSING GAME---")
        print("Let's play a word guessing game!")
        print(f"Enter {config.QUIT_CHAR} at any time to quit.")
        print(f"Enter {config.HINT_CHAR} to use a hint.")
        self.print_mode_rules()

    @abstractmethod
    def print_mode_rules(self):
        pass

    @abstractmethod
    def initial_value(self):
        pass

    @abstractmethod
    def update(self, current_value, correct_guess, occurrences):
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
        print("\nPOINTS MODE")
        print(f"Start with {config.MIN_TOK_LEN} points.")
        print("Correct guess: + number of occurrences.")
        print("Incorrect guess: -1 point.")
        print("Lose when score goes below 0.")

    def initial_value(self):
        return config.MIN_TOK_LEN

    def update(self, score, correct_guess, occurrences):
        if correct_guess:
            return score + occurrences
        return score - 1

    def has_lost(self, score):
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

    def print_mode_rules(self):
        print("\nLIVES MODE")
        print(f"Start with {self.STARTING_LIVES} lives.")
        print("Incorrect guesses cost one life.")
        print("Correct guesses do not restore lives.")

    def initial_value(self):
        return self.STARTING_LIVES

    def update(self, lives, correct_guess, occurrences):
        if correct_guess:
            return lives
        return lives - 1

    def has_lost(self, lives):
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
        print("\nCOUNTDOWN MODE")
        print(f"Start with {self.STARTING_SCORE} points.")
        print(f"Every guess costs {self.GUESS_COST} points.")
        print("Solve the word before reaching 0.")

    def initial_value(self):
        return self.STARTING_SCORE

    def update(self, score, correct_guess, occurrences):
        return score - self.GUESS_COST

    def has_lost(self, score):
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
    The player may continue until the word is solved
    or they choose to quit.
    """

    def print_mode_rules(self):
        print("\nSTREAK MODE")
        print("Build the longest streak of consecutive correct guesses possible.")
        print("Each correct guess increases your streak.")
        print("A wrong guess resets your streak to 0.")
        print("There is no loss condition.")
        print("Enter ! at any time to quit.")

    def initial_value(self):
        """
        Value represents current streak.
        """
        return 0

    def update(self, current_value, correct_guess, occurrences):
        if correct_guess:
            return current_value + 1
        return 0

    def has_lost(self, current_value):
        return False

    def display_label(self):
        return "Streak"



RULESETS = {"1": ("Points Mode", PointsRuleSet),
            "2": ("Lives Mode", LivesRuleSet),
            "3": ("Countdown Mode", CountdownRuleSet),
            "4": ("Streak Mode", StreakRuleSet)
            # Remember to add new rulesets here (don't forget the preceding comma!)
            }