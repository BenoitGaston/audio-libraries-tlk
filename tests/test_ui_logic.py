from ui.logic import artwork_execution_allowed


def test_artwork_execution_does_not_require_confirmation_without_artwork_options():
    assert artwork_execution_allowed(False, False, False)


def test_artwork_execution_requires_confirmation_for_new_session():
    assert not artwork_execution_allowed(True, False, False)
    assert artwork_execution_allowed(True, True, False)


def test_artwork_execution_allows_prior_session_confirmation():
    assert artwork_execution_allowed(True, False, True)
