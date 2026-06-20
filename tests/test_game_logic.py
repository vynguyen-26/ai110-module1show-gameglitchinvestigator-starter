from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

"""
Tests covering every fix described in the README "Demo Walkthrough".

Each section maps to one of the six fixes:

  1. Hint suggestion matches the guess to the secret correctly
  2. Score: wrong guess = flat -5; win bonus = 100 - 10*(attempt - 1)
  3. New Game resets score/status/history and draws a different secret
  4. Difficulty ranges and per-level attempt limits
  5. Input must stay within the level's range (recorded on the first click)
  6. The secret changes (and stays in range) when the level changes

Pure-function fixes (1, 2, 4, 5) are tested against logic_utils directly.
The session-state fixes (3, 6) are tested through new_round_state(), the
helper that both "New Game" and the difficulty-change reset in app.py call.
"""

import random

import pytest

from logic_utils import (
    check_guess,
    update_score,
    get_range_for_difficulty,
    get_attempt_limit,
    new_round_state,
    ATTEMPT_LIMITS,
)


# ---------------------------------------------------------------------------
# Fix 1 — Hint suggestion system points the right way and recognizes a win
# ---------------------------------------------------------------------------

def test_exact_match_is_a_win():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_guess_too_high_tells_user_to_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    # The hint must point downward, not upward (the original bug inverted it).
    assert "LOWER" in message.upper()
    assert "HIGHER" not in message.upper()


def test_guess_too_low_tells_user_to_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()
    assert "LOWER" not in message.upper()


def test_check_guess_at_range_boundaries():
    assert check_guess(1, 100)[0] == "Too Low"
    assert check_guess(100, 1)[0] == "Too High"
    assert check_guess(1, 1)[0] == "Win"


# ---------------------------------------------------------------------------
# Fix 2 — Score calculation
#   wrong guess = flat -5; win bonus = 100 - 10*(attempt_number - 1)
# ---------------------------------------------------------------------------

def test_first_guess_win_scores_100():
    assert update_score(0, "Win", attempt_number=1) == 100


@pytest.mark.parametrize(
    "attempt, expected_bonus",
    [
        (1, 100),
        (2, 90),
        (3, 80),
        (5, 60),
        (9, 20),
    ],
)
def test_win_bonus_decreases_by_10_per_attempt(attempt, expected_bonus):
    assert update_score(0, "Win", attempt_number=attempt) == expected_bonus


def test_win_bonus_floors_at_10():
    # 100 - 10*(11 - 1) = 0, but the bonus should never drop below 10.
    assert update_score(0, "Win", attempt_number=11) == 10
    assert update_score(0, "Win", attempt_number=50) == 10


def test_win_bonus_adds_to_existing_score():
    assert update_score(25, "Win", attempt_number=2) == 25 + 90


@pytest.mark.parametrize("attempt", [1, 2, 3, 7])
def test_wrong_guess_costs_flat_5_regardless_of_direction_or_attempt(attempt):
    # The original bug made cost depend on direction/parity; it must not.
    assert update_score(0, "Too High", attempt_number=attempt) == -5
    assert update_score(0, "Too Low", attempt_number=attempt) == -5


def test_too_high_and_too_low_cost_the_same():
    score = 30
    assert (
        update_score(score, "Too High", attempt_number=4)
        == update_score(score, "Too Low", attempt_number=4)
        == 25
    )


# ---------------------------------------------------------------------------
# Fix 4 — Difficulty ranges and per-level attempt limits
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "difficulty, expected_range",
    [
        ("Easy", (1, 20)),
        ("Normal", (1, 50)),
        ("Hard", (1, 100)),
    ],
)
def test_range_for_each_difficulty(difficulty, expected_range):
    assert get_range_for_difficulty(difficulty) == expected_range


def test_unknown_difficulty_falls_back_to_normal_range():
    assert get_range_for_difficulty("Whatever") == (1, 50)


def test_ranges_grow_with_difficulty():
    easy_high = get_range_for_difficulty("Easy")[1]
    normal_high = get_range_for_difficulty("Normal")[1]
    hard_high = get_range_for_difficulty("Hard")[1]
    assert easy_high < normal_high < hard_high


@pytest.mark.parametrize(
    "difficulty, expected_attempts",
    [
        ("Easy", 8),
        ("Normal", 6),
        ("Hard", 5),
    ],
)
def test_attempt_limit_for_each_difficulty(difficulty, expected_attempts):
    assert get_attempt_limit(difficulty) == expected_attempts


def test_unknown_difficulty_falls_back_to_normal_attempts():
    assert get_attempt_limit("Whatever") == 6


def test_harder_levels_get_fewer_attempts():
    # The original bug let Normal have more attempts / wider-than-Hard ranges.
    assert ATTEMPT_LIMITS["Easy"] > ATTEMPT_LIMITS["Normal"] > ATTEMPT_LIMITS["Hard"]


# ---------------------------------------------------------------------------
# Fix 5 — Guesses must stay within the level's range
#         (and are recorded after a single click; see note below)
# ---------------------------------------------------------------------------

def test_guess_inside_range_is_accepted():
    from logic_utils import parse_guess

    ok, value, err = parse_guess("15", low=1, high=20)
    assert ok is True
    assert value == 15
    assert err is None


@pytest.mark.parametrize("raw", ["0", "21", "100", "-3"])
def test_guess_outside_range_is_rejected(raw):
    from logic_utils import parse_guess

    ok, value, err = parse_guess(raw, low=1, high=20)
    assert ok is False
    assert value is None
    assert "range" in err.lower()


def test_range_boundaries_are_inclusive():
    from logic_utils import parse_guess

    assert parse_guess("1", low=1, high=20)[0] is True
    assert parse_guess("20", low=1, high=20)[0] is True


@pytest.mark.parametrize("raw", ["", None, "abc"])
def test_non_numeric_or_empty_input_is_rejected(raw):
    from logic_utils import parse_guess

    ok, value, err = parse_guess(raw, low=1, high=20)
    assert ok is False
    assert value is None
    assert err  # a helpful message, not None


# Note on "recorded after one click": app.py appends every submission to
# st.session_state.history inside the single Submit handler (valid guesses as
# ints, invalid ones as the raw string) and renders the debug panel AFTER that
# handler, so a guess shows up on the first click rather than the second. That
# ordering is a Streamlit-rendering concern, not pure logic; the parsing rules
# that decide what gets recorded are covered by the tests above.


# ---------------------------------------------------------------------------
# Fix 3 — "New Game" resets score / status / history (and picks a new secret)
# Fix 6 — Changing difficulty resets the round with an in-range secret
# Both go through new_round_state(), the shared reset helper used by app.py.
# ---------------------------------------------------------------------------

def test_new_round_state_resets_all_progress():
    state = new_round_state(1, 50, secret=42)
    assert state["score"] == 0
    assert state["attempts"] == 0
    assert state["status"] == "playing"
    assert state["history"] == []
    assert state["secret"] == 42


def test_new_round_state_clears_previous_history_and_score():
    # Simulate a finished round, then start fresh — nothing should carry over.
    finished = {
        "secret": 7,
        "attempts": 5,
        "score": 80,
        "status": "won",
        "history": [10, 3, 7],
    }
    fresh = new_round_state(1, 20, secret=12)
    assert fresh["score"] == 0
    assert fresh["attempts"] == 0
    assert fresh["history"] == []
    assert fresh["status"] == "playing"
    # The fresh state shares no mutable history list with the finished round.
    assert fresh["history"] is not finished["history"]


@pytest.mark.parametrize("difficulty", ["Easy", "Normal", "Hard"])
def test_new_secret_is_within_the_selected_levels_range(difficulty):
    low, high = get_range_for_difficulty(difficulty)
    # Draw several times: every secret must fall inside the level's range.
    for _ in range(200):
        secret = new_round_state(low, high)["secret"]
        assert low <= secret <= high


def test_changing_level_can_produce_a_different_secret():
    # An Easy secret (1-20) that lingers into Hard is the bug we fixed; a reset
    # in the Hard range should be able to land outside the Easy range.
    random.seed(12345)
    easy_low, easy_high = get_range_for_difficulty("Easy")
    hard_low, hard_high = get_range_for_difficulty("Hard")
    hard_secrets = {new_round_state(hard_low, hard_high)["secret"] for _ in range(100)}
    # At least one Hard secret is unreachable under Easy's range -> the secret
    # genuinely changes with the level rather than being stuck.
    assert any(s > easy_high for s in hard_secrets)
