from pathlib import Path
from shutil import copyfile

from audio_libs_tlk.lib_scan import collect_output_artifacts, scan_and_process
from audio_libs_tlk.itunes_lib_scan import iTunesLibraryScan
from audio_libs_tlk.parameters import itunes_usefull_cols


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
    assert set(itunes_usefull_cols).issubset(library.columns)
    assert library["Play Count"].isna().all()
    assert library["Play Date"].isna().all()
    assert (tmp_path / "Small-Library.csv").exists()


def test_scan_and_process_accepts_a_direct_xml_file_path(tmp_path):
    fixture_path = Path(__file__).with_name("Small-Library.xml")
    library_file = tmp_path / fixture_path.name
    copyfile(fixture_path, library_file)

    result = scan_and_process(library_file)

    assert result.library_data_path == tmp_path
    assert result.playlist_directory == tmp_path / "Small-Library_Playlists"
    assert tmp_path / "Small-Library.csv" in result.artifacts
