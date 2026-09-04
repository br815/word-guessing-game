# Type hints modeling the structured data types created for the game loop & game summary.
from typing import TypedDict



# TypedDict type hint for the return value of play_game() in WordGuessingGame() that is also the parameter of record_game() in Statistics().
class GameResults(TypedDict):
    mode: str
    word: str
    result: str
    score: int
    guesses: int
    completion: float
# End of this TypedDict class



# TypedDict type hint for the mode_stats attribute of Statistics(), which is a dict of mode name strings to ModeStats dicts.
class ModeStats(TypedDict):
    games: int
    words_won: list[str]
    words_lost: list[str]
    total_score: int
    best_score: int | None
    worst_score: int | None
# End of this TypedDict class