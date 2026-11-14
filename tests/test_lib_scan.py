from pathlib import Path
from shutil import copyfile

from audio_libs_tlk.lib_scan import collect_output_artifacts
from audio_libs_tlk.itunes_lib_scan import iTunesLibraryScan


def test_collect_output_artifacts_includes_supported_files(tmp_path):
    playlist_directory = tmp_path / "Playlists"
    playlist_directory.mkdir()
    (tmp_path / "library.csv").touch()
    (playlist_directory / "report.m3u8").touch()
    (playlist_directory / "cover.jpg").touch()

    artifacts = collect_output_artifacts(tmp_path, playlist_directory)

    assert set(artifacts) == {
        tmp_path / "library.csv",
        playlist_directory / "report.m3u8",
    }


def test_itunes_library_scan_reads_small_library_fixture(tmp_path):
    fixture_path = Path(__file__).with_name("Small-Library.xml")
    library_file = tmp_path / fixture_path.name
    copyfile(fixture_path, library_file)

    scanner = iTunesLibraryScan(library_file, tmp_path)
    library = scanner.get_itunes_library_as_csv()

    assert not library.empty
    assert {"Name", "Artist", "Location"}.issubset(library.columns)
    assert (tmp_path / "Small-Library.csv").exists()
