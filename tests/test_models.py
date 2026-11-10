import pandas as pd

from audio_libs_tlk.models import AudioLibrary, Playlist, itunes_schema


def test_itunes_schema_apply_schema_converts_types():
    df = pd.DataFrame(
        {
            "Total Time": ["123", "456"],
            "Album Rating": ["5", "7"],
            "Album Loved": [True, False],
            "Date Added": ["2025-01-01", "2025-02-01"],
        }
    )

    result = itunes_schema.apply_schema(df)

    assert str(result["Total Time"].dtype) == "Int64"
    assert str(result["Album Rating"].dtype) == "Int64"
    assert str(result["Album Loved"].dtype) == "boolean"
    assert pd.api.types.is_datetime64_any_dtype(result["Date Added"])


def test_itunes_schema_validate_dataframe():
    df = pd.DataFrame(
        {
            "Total Time": ["123", "456"],
            "Album Rating": ["5", "7"],
            "Album Loved": [True, False],
            "Date Added": ["2025-01-01", "2025-02-01"],
        }
    )

    result = itunes_schema.apply_schema(df)

    assert itunes_schema.validate_dataframe(result)


def test_audio_library_describes_tracks_from_dataframe():
    dataframe = pd.DataFrame(
        {
            "Name": ["Song Title"],
            "Artist": ["Artist Name"],
            "Album": ["Album Title"],
            "Album Artist": ["Album Artist"],
            "Genre": ["Rock"],
            "Location": ["file:/tmp/song.mp3"],
        }
    )

    library = AudioLibrary.from_dataframe(dataframe, name="Music")

    assert library.name == "Music"
    assert library.tracks[0].name == "Song Title"
    assert library.tracks[0].album_artist == "Album Artist"


def test_playlist_accepts_name_or_title_dataframe_columns():
    dataframe = pd.DataFrame(
        {
            "Title": ["Song Title"],
            "Artist": ["Artist Name"],
            "Total Time": [1500],
            "Location": ["file:/tmp/song.mp3"],
        }
    )

    playlist = Playlist.from_dataframe("Example", dataframe)

    assert playlist.name == "Example"
    assert playlist.tracks[0].name == "Song Title"
    assert playlist.tracks[0].total_time == 1500
