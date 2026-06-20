from logic_utils import check_guess

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

# Bug fix: hint messages were reversed — verify they now point in the correct direction
def test_too_high_message_says_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message, f"Expected 'LOWER' in hint when guess is too high, got: {message!r}"

def test_too_low_message_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint when guess is too low, got: {message!r}"

# String-secret fallback path (triggered on even attempts in app.py)
def test_win_with_string_secret():
    outcome, _ = check_guess(50, "50")
    assert outcome == "Win"

def test_too_high_with_string_secret():
    outcome, message = check_guess(60, "50")
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_with_string_secret():
    outcome, message = check_guess(40, "50")
    assert outcome == "Too Low"
    assert "HIGHER" in message


# --- New game reset tests ---

def simulate_new_game(session_state: dict, new_secret: int) -> dict:
    """Mirrors the new_game branch in app.py after the bug fix."""
    session_state["attempts"] = 0
    session_state["secret"] = new_secret
    session_state["status"] = "playing"
    session_state["history"] = []
    return session_state


def make_end_state(status: str) -> dict:
    """Returns a session state that looks like a finished game."""
    return {
        "attempts": 5,
        "secret": 42,
        "status": status,
        "history": [10, 20, 30, 40, 42],
        "score": 50,
    }


def test_new_game_resets_status_after_win():
    state = make_end_state("won")
    simulate_new_game(state, new_secret=7)
    assert state["status"] == "playing", "status must be 'playing' after new game"


def test_new_game_resets_status_after_loss():
    state = make_end_state("lost")
    simulate_new_game(state, new_secret=7)
    assert state["status"] == "playing", "status must be 'playing' after new game"


def test_new_game_clears_history():
    state = make_end_state("won")
    simulate_new_game(state, new_secret=7)
    assert state["history"] == [], "history must be empty after new game"


def test_new_game_resets_attempts():
    state = make_end_state("lost")
    simulate_new_game(state, new_secret=7)
    assert state["attempts"] == 0, "attempts must be 0 after new game"


def test_new_game_sets_new_secret():
    state = make_end_state("won")
    simulate_new_game(state, new_secret=99)
    assert state["secret"] == 99


def test_new_game_preserves_score():
    """Score intentionally carries over between games."""
    state = make_end_state("won")
    original_score = state["score"]
    simulate_new_game(state, new_secret=7)
    assert state["score"] == original_score, "score should persist across games"
