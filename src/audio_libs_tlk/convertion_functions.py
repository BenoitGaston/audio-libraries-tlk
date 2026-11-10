from pathlib import Path
from urllib.parse import unquote
import unicodedata

import pandas as pd

from .models import Playlist


def convert_a_playlist(
    path_to_playlist_folder: Path,
    path_to_destination_folder: Path,
    orginal_path: str,
    updated_path: str,
    file_name: str,
) -> None:
    """Copy an M3U8 playlist while replacing its media-path prefix.

    Args:
        path_to_playlist_folder: Folder containing the source playlist.
        path_to_destination_folder: Folder for the converted playlist.
        orginal_path: Prefix to replace in media-location lines.
        updated_path: Replacement path prefix.
        file_name: Name of the playlist to convert.
    """
    with (
        open(path_to_playlist_folder / file_name) as source_file,
        open(path_to_destination_folder / file_name, "w") as destination_file,
    ):
        for line in source_file:
            if not (line.startswith("#EXTINF:") or line.startswith("#EXTM3U")):
                line = line.replace(orginal_path, updated_path)
            destination_file.write(
                (unicodedata.normalize("NFC", line).encode("utf-8")).decode("utf-8")
            )


def m3u8_to_csv(path_to_playlist: Path, playlist_name: str) -> pd.DataFrame:
    """Parse an M3U8 playlist and save its entries as a CSV file.

    Args:
        path_to_playlist: Folder containing the M3U8 playlist.
        playlist_name: M3U8 file name.

    Returns:
        A dataframe containing artist, title, duration, and location columns.
    """

    duration_list = []
    title_list = []
    artist_list = []
    location_list = []

    with open(path_to_playlist / playlist_name, "r") as playlist_file:
        for line in playlist_file:
            line_strip = line.strip()
            if line_strip.startswith("#EXTINF:"):
                duration, separator, label = line_strip.removeprefix(
                    "#EXTINF:"
                ).partition(",")
                if not separator or " - " not in label:
                    raise ValueError(f"Invalid M3U8 entry: {line_strip}")
                title, artist = label.rsplit(" - ", 1)

                duration_list.append(duration)
                title_list.append(title.strip())
                artist_list.append(artist.strip())
            elif not line_strip.startswith("#EXT"):
                location_list.append(line_strip)

    playlist_df = pd.DataFrame(
        {
            "Artist": artist_list,
            "Title": title_list,
            "Total Time": duration_list,
            "Location": location_list,
        }
    )

    playlist_df.loc[:, "Location"] = playlist_df.loc[:, "Location"].apply(
        lambda x: Path(unquote(x.replace("file:", "")))
    )
    playlist_df.loc[:, "Album Location"] = playlist_df.loc[:, "Location"].apply(
        lambda x: x.parent
    )
    playlist_df.to_csv(
        path_to_playlist / playlist_name.replace("m3u8", "csv"), index=False
    )

    return playlist_df


def df_to_m3u8(
    playlist_df: pd.DataFrame, file_name: str, path_to_m3u8_folder: Path
) -> None:
    """Write a dataframe of tracks to an M3U8 playlist.

    Args:
        playlist_df: Track dataframe with name, artist, duration, and location columns.
        file_name: Output playlist name, with or without the ``.m3u8`` suffix.
        path_to_m3u8_folder: Destination directory.
    """

    if not file_name.endswith(".m3u8"):
        file_name += ".m3u8"

    playlist = Playlist.from_dataframe(file_name, playlist_df)
    with open(path_to_m3u8_folder / file_name, "w+") as playlist_file:
        playlist_file.write("#EXTM3U\r\n")

        for track in playlist.tracks:
            playlist_file.write(
                f"#EXTINF:{round(track.total_time / 1000)} ,"
                f"{track.name} - {track.artist}\r\n"
            )
            playlist_file.write(
                f"{unquote(str(track.location))}\r\n".replace("%20", " ")
            )


def PL_to_m3u8(
    path_to_playlists_folder: Path,
    playlist,
) -> pd.DataFrame:
    """Export an iTunes playlist object to M3U8 and return its track dataframe.

    Args:
        path_to_playlists_folder: Destination directory for the M3U8 file.
        playlist: Playlist object supplied by ``itunesLibrary``.

    Returns:
        Dataframe with the exported playlist's tracks.
    """
    file_name = f"{playlist.itunesAttributes['Name']}.m3u8"
    if (path_to_playlists_folder / file_name).exists():
        file_name = (
            f"{playlist.itunesAttributes['Name']} - "
            f"{playlist.itunesAttributes['Playlist ID']}.m3u8"
        )

    f = open(path_to_playlists_folder / file_name, "w+")
    f.write(f"#EXTM3U\r\n")

    total_time_list = []
    name_list = []
    artist_list = []
    location_list = []

    for item in playlist.items:
        # try:
        try:
            total_time = item.itunesAttributes["Total Time"]
        except:
            total_time = 0

        name = item.itunesAttributes["Name"]
        try:
            artist = item.itunesAttributes["Artist"]
        except:
            artist = None
        location = item.itunesAttributes["Location"]

        total_time_list.append(total_time)
        name_list.append(name)
        artist_list.append(artist)
        location_list.append(location)

        f.write(f"#EXTINF:{round(int(total_time)/1000)} ,{name} - {artist}\r\n")
        f.write(f"{location}\r\n".replace("%20", " "))

    f.close()

    playlist_df = pd.DataFrame(
        {
            "Artist": artist_list,
            "Name": name_list,
            "Total Time": total_time_list,
            "Location": location_list,
        }
    )
    playlist_df.loc[:, "Location"] = playlist_df.loc[:, "Location"].apply(
        lambda x: unquote(x)
    )
    return playlist_df
