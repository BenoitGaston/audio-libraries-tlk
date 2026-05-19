import pandas as pd

from audio_libs_tlk.convertion_functions import (
    convert_a_playlist,
    df_to_m3u8,
    m3u8_to_csv,
)


def test_m3u8_to_csv_writes_csv(tmp_path):
    playlist_file = tmp_path / "playlist.m3u8"
    playlist_file.write_text(
        "#EXTM3U\n#EXTINF:123,Song Title - Artist Name\nfile:/tmp/song1.mp3\n",
        encoding="utf-8",
    )

    df = m3u8_to_csv(tmp_path, "playlist.m3u8")
    csv_file = tmp_path / "playlist.csv"

    assert csv_file.exists()
    assert list(df.columns) == [
        "Artist",
        "Title",
        "Total Time",
        "Location",
        "Album Location",
    ]
    assert df.loc[0, "Artist"] == "Artist Name"
    assert df.loc[0, "Title"] == "Song Title"
    assert str(df.loc[0, "Location"]).endswith("tmp/song1.mp3")


def test_df_to_m3u8_writes_playlist(tmp_path):
    playlist_df = pd.DataFrame(
        {
            "Name": ["Song Title"],
            "Artist": ["Artist Name"],
            "Total Time": [1500],
            "Location": ["file:/tmp/song1.mp3"],
        }
    )

    df_to_m3u8(playlist_df, "out.m3u8", tmp_path)
    output_file = tmp_path / "out.m3u8"
    content = output_file.read_text(encoding="utf-8")

    assert output_file.exists()
    assert content.startswith("#EXTM3U")
    assert "#EXTINF:2 ,Song Title - Artist Name" in content
    assert "file:/tmp/song1.mp3" in content


def test_convert_a_playlist_replaces_paths(tmp_path):
    source_folder = tmp_path / "source"
    source_folder.mkdir()
    destination_folder = tmp_path / "destination"
    destination_folder.mkdir()

    playlist_file = source_folder / "playlist.m3u8"
    playlist_file.write_text(
        "#EXTM3U\n#EXTINF:123,Song Title - Artist Name\nfile:/old/path/song1.mp3\n",
        encoding="utf-8",
    )

    convert_a_playlist(
        source_folder,
        destination_folder,
        "file:/old/path",
        "file:/new/path",
        "playlist.m3u8",
    )

    output_file = destination_folder / "playlist.m3u8"
    content = output_file.read_text(encoding="utf-8")

    assert output_file.exists()
    assert "file:/new/path/song1.mp3" in content
