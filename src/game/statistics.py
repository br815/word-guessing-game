import config
from game.data_types import GameResults, ModeStats



class Statistics:
    def __init__(self) -> None:
        # Overall session statistics.
        self.words_played: set[str] = set()
        self.games_played: int = 0

        self.wins: int = 0
        self.losses: int = 0
        self.quits: int = 0

        self.total_guesses: int = 0
        self.total_completion: float = 0.0

        # Initialized to None to clearly indicate that these values have not been assigned yet.
        self.fewest_guesses: int | None = None
        self.most_guesses: int | None = None
        self.best_completion: float | None = None
        self.worst_completion: float | None = None

        # Dictionary of statistics that are specific to each game mode (these stats are wrapped into ModeStats dicts).
        self.mode_stats: dict[str, ModeStats] = {}
    # End of init()



    def record_game(self, game_results: GameResults) -> None:
        mode = game_results["mode"]
        word = game_results["word"]
        self.words_played.add(word)
        result = game_results["result"]
        score = game_results["score"]
        guesses = game_results["guesses"]
        completion = game_results["completion"]

        # If this is the first game played in this mode, initialize its mode-specific statistics.
        if mode not in self.mode_stats:
            self.mode_stats[mode] = {
                "games": 0,
                "words_won": [],
                "words_lost": [],
                "total_score": 0,
                "best_score": None,
                "worst_score": None}

        # Wrap the currently recorded mode in a more aptly-named local variable.
        current_mode_stats = self.mode_stats[mode]

        # 1st: Update overall session statistics.
        self.games_played += 1

        # Handle wins, losses, and quits.
        if result == "WIN":
            self.wins += 1
            current_mode_stats["words_won"].append(word)

        elif result == "LOSS":
            self.losses += 1
            current_mode_stats["words_lost"].append(word)

        elif result == "QUIT":
            self.quits += 1
            current_mode_stats["words_lost"].append(word)   # Quitting on an unsolved word makes it count as a loss.

        # Accumulate totals.
        self.total_guesses += guesses
        self.total_completion += completion

        # Comparisons for fewest/most and best/worst.
        if self.fewest_guesses is None or guesses < self.fewest_guesses:
            self.fewest_guesses = guesses

        if self.most_guesses is None or guesses > self.most_guesses:
            self.most_guesses = guesses

        if self.best_completion is None or completion > self.best_completion:
            self.best_completion = completion

        if self.worst_completion is None or completion < self.worst_completion:
            self.worst_completion = completion

        # 2nd: Update statistics specific to the current mode.
        current_mode_stats["games"] += 1

        # Accumulate total.
        current_mode_stats["total_score"] += score

        # Comparisons for best/worst.
        if (current_mode_stats["best_score"] is None or score > current_mode_stats["best_score"]):
            current_mode_stats["best_score"] = score

        if (current_mode_stats["worst_score"] is None or score < current_mode_stats["worst_score"]):
            current_mode_stats["worst_score"] = score
    # End of record_game()



    # Helper printer function used to print words in the final report.
    def print_words_won_or_lost(self, row_name: str, col_width: int, words_won_or_lost: list[str]) -> None:
        # Only print either list of words won or lost if any words actually WERE won or lost.
        if not words_won_or_lost:
            return

        # Set prefix to be the row name + the column width used for all other columns in the report.
        prefix = f"{row_name:<{col_width}}"
        current_line = prefix

        for index, word in enumerate(words_won_or_lost):
            # Add a comma if this is not the final word in the list.
            if index < len(words_won_or_lost) - 1:
                word += ","

            if current_line == prefix:
                proposed_line = current_line + word
            else:
                proposed_line = current_line + " " + word

            if len(proposed_line) > config.BORDER_LEN:
                print(current_line)
                current_line = " " * len(prefix) + word
            else:
                current_line = proposed_line

        print(current_line)
    # End of print_words_won_or_lost()



    def print_report(self) -> None:
        if self.games_played == 0:
            print("No games played.")
            return

        # Using integer division, come up with an appropriate width for each column in the summary table.
        col_width = config.BORDER_LEN // 2

        # Calculate averages & win rate before printing.
        avg_guesses = (self.total_guesses / self.games_played)
        avg_completion = (self.total_completion / self.games_played)
        win_rate = (self.wins / self.games_played) * 100

        # 1st: print a summary of the overall game session.
        print()
        print("=" * config.BORDER_LEN)
        print("SESSION SUMMARY")
        print("=" * config.BORDER_LEN)

        print(f"{"Games Played":<{col_width}}{self.games_played}")
        print(f"{"Wins":<{col_width}}{self.wins}")
        print(f"{"Losses":<{col_width}}{self.losses}")
        print(f"{"Quits":<{col_width}}{self.quits}")
        print(f"{'Win Rate':<{col_width}}{win_rate:.2f}%")

        print("-" * config.BORDER_LEN)

        print(f"{"Average Guesses":<{col_width}}{avg_guesses:.2f}")
        print(f"{"Fewest Guesses":<{col_width}}{self.fewest_guesses}")
        print(f"{"Most Guesses":<{col_width}}{self.most_guesses}")

        print("-" * config.BORDER_LEN)

        print(f"{"Average Completion":<{col_width}}{avg_completion:.2f}%")
        print(f"{"Best Completion":<{col_width}}{self.best_completion:.2f}%")
        print(f"{"Worst Completion":<{col_width}}{self.worst_completion:.2f}%")

        # 2nd: print a summary of each mode that has been played.
        print("=" * config.BORDER_LEN)
        print("PER-MODE SUMMARY")
        print("=" * config.BORDER_LEN)

        for index, (mode, current_mode_stats) in enumerate(self.mode_stats.items()):
            # Calculate the average score of the mode.
            avg_score = (current_mode_stats["total_score"] / current_mode_stats["games"])

            print(f"{mode.upper()} MODE")
            print(f"{"Games Played":<{col_width}}{current_mode_stats["games"]}")
            self.print_words_won_or_lost("Words Correctly Guessed", col_width, current_mode_stats["words_won"])
            self.print_words_won_or_lost("Words Failed to Guess", col_width, current_mode_stats["words_lost"])
            print(f"{"Average Score":<{col_width}}{avg_score:.2f}")
            print(f"{"Best Score":<{col_width}}{current_mode_stats["best_score"]}")
            print(f"{"Worst Score":<{col_width}}{current_mode_stats["worst_score"]}")

            # Print a separator between modes, or the end-of-report footer after the final mode.
            if index < len(self.mode_stats) - 1:
                print("-" * config.BORDER_LEN)
            else:
                print("=" * config.BORDER_LEN)
    # End of print_report()
# End of Statistics() class