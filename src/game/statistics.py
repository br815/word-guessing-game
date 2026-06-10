class Statistics:
    def __init__(self):
        self.mode = None
        self.games_played = 0

        self.wins = 0
        self.losses = 0
        self.quits = 0

        self.total_score = 0

        self.best_score = None
        self.worst_score = None

        self.total_guesses = 0

        self.best_guesses = None
        self.worst_guesses = None

        self.total_completion = 0.0

        self.best_completion = None
        self.worst_completion = None



    def record_game(self, game_result):
        if self.mode is None:
            self.mode = game_result["mode"]
        result = game_result["result"]
        score = game_result["score"]
        guesses = game_result["guesses"]
        completion = game_result["completion"]

        self.games_played += 1

        if result == "WIN":
            self.wins += 1

        elif result == "LOSS":
            self.losses += 1

        elif result == "QUIT":
            self.quits += 1

        self.total_score += score

        self.total_guesses += guesses

        self.total_completion += completion

        if self.best_score is None or score > self.best_score:
            self.best_score = score

        if self.worst_score is None or score < self.worst_score:
            self.worst_score = score

        if self.best_guesses is None or guesses < self.best_guesses:
            self.best_guesses = guesses

        if self.worst_guesses is None or guesses > self.worst_guesses:
            self.worst_guesses = guesses

        if (self.best_completion is None or completion > self.best_completion):
            self.best_completion = completion

        if (self.worst_completion is None or completion < self.worst_completion):
            self.worst_completion = completion



    def print_report(self):
        if self.games_played == 0:
            print("No games played.")
            return

        avg_score = (self.total_score / self.games_played)

        avg_guesses = (self.total_guesses / self.games_played)

        avg_completion = (self.total_completion / self.games_played)

        win_rate = (self.wins / self.games_played) * 100

        print("\n")
        print("=" * 50)
        print(f"SESSION SUMMARY: {self.mode.upper()} MODE")
        print("=" * 50)

        print(f"{'Games Played':<30}{self.games_played}")
        print(f"{'Wins':<30}{self.wins}")
        print(f"{'Losses':<30}{self.losses}")
        print(f"{'Quits':<30}{self.quits}")

        print("-" * 50)

        print(f"{'Win Rate':<30}{win_rate:.1f}%")

        print("-" * 50)

        print(f"{'Total Score':<30}{self.total_score}")
        print(f"{'Average Score':<30}{avg_score:.2f}")
        print(f"{'Best Score':<30}{self.best_score}")
        print(f"{'Worst Score':<30}{self.worst_score}")

        print("-" * 50)

        print(f"{'Average Guesses':<30}{avg_guesses:.2f}")
        print(f"{'Fewest Guesses':<30}{self.best_guesses}")
        print(f"{'Most Guesses':<30}{self.worst_guesses}")

        print("-" * 50)

        print(f"{'Average Completion':<30}{avg_completion:.1f}%")

        print(f"{'Best Completion':<30}{self.best_completion:.1f}%")

        print(f"{'Worst Completion':<30}{self.worst_completion:.1f}%")

        print("=" * 50)