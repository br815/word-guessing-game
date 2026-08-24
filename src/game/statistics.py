class Statistics:
    def __init__(self):
        # Overall session statistics.
        self.words_played = set()
        self.games_played = 0

        self.wins = 0
        self.losses = 0
        self.quits = 0

        self.total_guesses = 0

        self.fewest_guesses = None
        self.most_guesses = None

        self.total_completion = 0.0

        self.best_completion = None
        self.worst_completion = None

        # Statistics that are specific to each game mode.
        self.mode_stats = {}



    def record_game(self, game_results):
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
                "total_score": 0,
                "best_score": None,
                "worst_score": None,
                "words_won": [],
                "words_lost": []}

        mode_data = self.mode_stats[mode]

        # Update overall session statistics.
        self.games_played += 1

        if result == "WIN":
            self.wins += 1
            mode_data["words_won"].append(word)

        elif result == "LOSS":
            self.losses += 1
            mode_data["words_lost"].append(word)

        elif result == "QUIT":
            self.quits += 1       
            mode_data["words_lost"].append(word)     

        self.total_guesses += guesses

        self.total_completion += completion

        if self.fewest_guesses is None or guesses < self.fewest_guesses:
            self.fewest_guesses = guesses

        if self.most_guesses is None or guesses > self.most_guesses:
            self.most_guesses = guesses

        if self.best_completion is None or completion > self.best_completion:
            self.best_completion = completion

        if self.worst_completion is None or completion < self.worst_completion:
            self.worst_completion = completion
        

        # Update statistics specific to the current mode.
        mode_data["games"] += 1

        mode_data["total_score"] += score

        if (
            mode_data["best_score"] is None
            or score > mode_data["best_score"]
        ):
            mode_data["best_score"] = score

        if (
            mode_data["worst_score"] is None
            or score < mode_data["worst_score"]
        ):
            mode_data["worst_score"] = score



    # Helper print function used to print words in final report.
    def print_word_list(self, label, words, width=50):
        # Only print either list of words won or lost if any words actually WERE won or lost.
        if not words:
            return

        prefix = f"{label:<30}"
        current_line = prefix

        for index, word in enumerate(words):

            # Add a comma if this is not the final word in the list.
            if index < len(words) - 1:
                word += ","

            if current_line == prefix:
                proposed_line = current_line + word
            else:
                proposed_line = current_line + " " + word

            if len(proposed_line) > width:
                print(current_line)
                current_line = " " * len(prefix) + word
            else:
                current_line = proposed_line

        print(current_line)



    def print_report(self):
        if self.games_played == 0:
            print("No games played.")
            return

        avg_guesses = (
            self.total_guesses
            / self.games_played
        )

        avg_completion = (
            self.total_completion
            / self.games_played
        )

        win_rate = (
            self.wins
            / self.games_played
        ) * 100

        print()
        print("=" * 50)
        print("SESSION SUMMARY")
        print("=" * 50)

        print(
            f"{'Games Played':<30}"
            f"{self.games_played}"
        )

        print(
            f"{'Wins':<30}"
            f"{self.wins}"
        )

        print(
            f"{'Losses':<30}"
            f"{self.losses}"
        )

        print(
            f"{'Quits':<30}"
            f"{self.quits}"
        )

        print(
            f"{'Win Rate':<30}"
            f"{win_rate:.2f}%"
        )

        print("-" * 50)

        print(
            f"{'Average Guesses':<30}"
            f"{avg_guesses:.2f}"
        )

        print(
            f"{'Fewest Guesses':<30}"
            f"{self.fewest_guesses}"
        )

        print(
            f"{'Most Guesses':<30}"
            f"{self.most_guesses}"
        )

        print("-" * 50)

        print(
            f"{'Average Completion':<30}"
            f"{avg_completion:.2f}%"
        )

        print(
            f"{'Best Completion':<30}"
            f"{self.best_completion:.2f}%"
        )

        print(
            f"{'Worst Completion':<30}"
            f"{self.worst_completion:.2f}%"
        )

        print("=" * 50)
        print("PER-MODE SUMMARY")
        print("=" * 50)

        for index, (mode, mode_data) in enumerate(self.mode_stats.items()):
            avg_score = (mode_data["total_score"] / mode_data["games"])

            print(f"{mode.upper()} MODE")
        
            print(
                f"{'Games Played':<30}"
                f"{mode_data['games']}")

            self.print_word_list(
                "Words Correctly Guessed",
                mode_data["words_won"])

            self.print_word_list(
                "Words Failed to Guess",
                mode_data["words_lost"])

            print(
                f"{'Average Score':<30}"
                f"{avg_score:.2f}")

            print(
                f"{'Best Score':<30}"
                f"{mode_data['best_score']}")

            print(
                f"{'Worst Score':<30}"
                f"{mode_data['worst_score']}")

            # Print a separator between modes, or the end-of-report line after the final mode.
            if index < len(self.mode_stats) - 1:
                print("-" * 50)
            else:
                print("=" * 50)
# End of Statistics class