import logging

from audio_libs_tlk.folder_lib_scan import loop_over_a_music_path


def test_music_library_scan_logs_scanned_directory(tmp_path, caplog):
    with caplog.at_level(logging.INFO):
        loop_over_a_music_path(tmp_path)

    assert f"Scanning album at {tmp_path}" in caplog.messages
