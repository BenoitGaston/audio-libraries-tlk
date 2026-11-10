import pandas as pd

from audio_libs_tlk.processing_lib import LibraryProcessing


def make_library_dataframe():
    return pd.DataFrame(
        {
            "Name": [
                "Duplicate",
                "Duplicate",
                "Duplicate",
                "Genre Song 1",
                "Genre Song 2",
                "Shared Title A",
                "Shared Title B",
                "Unique",
            ],
            "Artist": [
                "Artist A",
                "Artist A",
                "Artist B",
                "Artist C",
                "Artist C",
                "Artist D",
                "Artist E",
                "Artist F",
            ],
            "Album": [
                "First Album",
                "Second Album",
                "Third Album",
                "Mixed Genre Album",
                "Mixed Genre Album",
                "Same Album Title",
                "Same Album Title",
                "Unique Album",
            ],
            "Album Artist": [
                "Artist A",
                "Artist A",
                "Artist B",
                "Artist C",
                "Artist C",
                "Artist D",
                "Artist E",
                "Artist F",
            ],
            "Genre": [
                "Rock",
                "Rock",
                "Rock",
                "Rock",
                "Jazz",
                "Pop",
                "Pop",
                "Classical",
            ],
            "Total Time": [1000] * 8,
            "Location": [f"file:/tmp/song-{index}.mp3" for index in range(8)],
        }
    )


def assert_analysis_files_exist(output_folder, file_name):
    assert (output_folder / "Special_Playlists" / f"{file_name}.csv").exists()
    assert (output_folder / "Special_Playlists" / f"{file_name}.m3u8").exists()


def test_find_duplicate_songs_exports_configurable_matches(tmp_path):
    processor = LibraryProcessing(tmp_path, make_library_dataframe())

    duplicate_songs_by_artist = processor.find_duplicate_songs()
    duplicate_songs = processor.find_duplicate_songs(match_columns=("Name",))

    assert len(duplicate_songs_by_artist) == 2
    assert len(duplicate_songs) == 3
    assert set(duplicate_songs["Name"]) == {"Duplicate"}
    assert_analysis_files_exist(tmp_path, "Duplicate_Songs")


def test_find_inconsistent_album_genres_exports_tracks(tmp_path):
    processor = LibraryProcessing(tmp_path, make_library_dataframe())

    inconsistent_genres = processor.find_inconsistent_album_genres()

    assert set(inconsistent_genres["Name"]) == {"Genre Song 1", "Genre Song 2"}
    assert_analysis_files_exist(tmp_path, "Albums_With_Inconsistent_Genres")


def test_find_albums_with_shared_titles_exports_tracks(tmp_path):
    processor = LibraryProcessing(tmp_path, make_library_dataframe())

    shared_title_albums = processor.find_albums_with_shared_titles()

    assert set(shared_title_albums["Name"]) == {"Shared Title A", "Shared Title B"}
    assert_analysis_files_exist(tmp_path, "Albums_With_Shared_Titles")
