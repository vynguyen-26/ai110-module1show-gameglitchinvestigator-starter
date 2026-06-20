import random


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50


# Attempts allowed per difficulty. Harder levels (bigger range) get fewer
# attempts: Easy (1-20) -> 8, Normal (1-50) -> 6, Hard (1-100) -> 5.
ATTEMPT_LIMITS = {
    "Easy": 8,
    "Normal": 6,
    "Hard": 5,
}


def get_attempt_limit(difficulty: str) -> int:
    """Return the number of attempts allowed for a given difficulty."""
    return ATTEMPT_LIMITS.get(difficulty, 6)


def new_round_state(low: int, high: int, secret=None):
    """
    Build a fresh per-round state dict.

    Used by both "New Game" and a difficulty change so a new round always
    starts from zero: score 0, no attempts, empty history, status "playing",
    and a brand-new secret somewhere in [low, high].

    Pass an explicit ``secret`` to make the state deterministic (e.g. in tests);
    otherwise one is drawn at random from the inclusive range.
    """
    if secret is None:
        secret = random.randint(low, high)
    return {
        "secret": secret,
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
    }


def parse_guess(raw: str, low=None, high=None):
    """
    Parse user input into an int guess.

    If low/high are given, the guess must fall within that inclusive range,
    otherwise it is rejected as out of range.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    if low is not None and high is not None and not (low <= value <= high):
        return False, None, "Your input is out of range. Please enter an input that is within the range."

    return True, value, None


# FIXME: Logic breaks here and what had been fixed
# Problem 1 — Hint system was inaccurate.
#   - The hint messages were inverted: "Too High" told the user to "Go HIGHER!"
#     and "Too Low" told them to "Go LOWER!" (both backwards).
#   - A separate bug elsewhere turned the secret into a string on even attempts,
#     which made the int-vs-string comparison fall back to broken lexicographic
#     logic and also stopped correct guesses from registering as a win.
#   Fixed: hints now point the right way (too high -> go lower, too low -> go
#   higher), an exact match always wins, and the secret stays an int (see submit).
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct! You guessed it!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


# FIXME: Logic breaks here and what had been fixed
# Problem 2 — Score calculation was inconsistent.
#   - Wrong guesses scored differently by direction/parity: "Too High" added +5
#     on even attempts but -5 on odd ones, while "Too Low" was always -5.
#   - The win bonus had an off-by-one (100 - 10*(attempt_number + 1)), so a
#     first-guess win only gave 70 instead of 100.
#   - New Game never reset the score, so it carried over instead of starting at 0.
#   Fixed: every wrong guess costs a flat -5, the win bonus is
#   100 - 10*(attempt_number - 1) (first-guess win = 100), and New Game now
#   resets score/status/history (see the new_game handler in app.py).
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    # Any wrong guess costs the same, regardless of direction or attempt.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
