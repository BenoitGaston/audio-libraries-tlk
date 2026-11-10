"""Pure helpers used by the Streamlit interface."""


def artwork_execution_allowed(
    artwork_operations_selected: bool,
    confirmed_for_run: bool,
    always_allowed_this_session: bool,
) -> bool:
    """Return whether the selected artwork operations have user authorization."""
    return (
        not artwork_operations_selected
        or confirmed_for_run
        or always_allowed_this_session
    )
