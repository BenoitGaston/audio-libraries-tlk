from audio_libs_tlk.lib_scan import collect_output_artifacts


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
