from pathlib import Path

from ui.logic import artwork_execution_allowed
from ui.logic import is_supported_library_source


def test_artwork_execution_does_not_require_confirmation_without_artwork_options():
    assert artwork_execution_allowed(False, False, False)


def test_artwork_execution_requires_confirmation_for_new_session():
    assert not artwork_execution_allowed(True, False, False)
    assert artwork_execution_allowed(True, True, False)


def test_artwork_execution_allows_prior_session_confirmation():
    assert artwork_execution_allowed(True, False, True)


def test_is_supported_library_source_accepts_directories_and_xml_files(tmp_path):
    xml_file = tmp_path / "Library.XML"
    xml_file.touch()
    audio_file = tmp_path / "track.mp3"
    audio_file.touch()

    assert is_supported_library_source(tmp_path)
    assert is_supported_library_source(xml_file)
    assert not is_supported_library_source(audio_file)
    assert not is_supported_library_source(tmp_path / "missing.xml")
