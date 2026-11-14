"""Pure helpers used by the Streamlit interface."""

from pathlib import Path


def is_supported_library_source(path: Path) -> bool:
    """Return whether a path is a library directory or an XML export file."""
    return path.is_dir() or (path.is_file() and path.suffix.lower() == ".xml")


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
