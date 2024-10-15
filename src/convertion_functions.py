import pandas as pd
import os
import xml.etree.ElementTree as ET  ## XML parsing
from pathlib import Path

from urllib.parse import unquote

import os
import unicodedata
import logging


def convert_a_playlist(
    path_to_playlist_folder,
    path_to_destination_folder,
    orginal_path,
    updated_path,
    file_name,
):
    """Change the location of the songs in a playlist
    by replacing orginal_path with updated_path

    Args:
        path_to_playlist_folder (Path): _description_
        path_to_destination_folder (Path): _description_
        orginal_path (str): part of the path to be replaced
        updated_path (str): _description_
        file_name (str): file name for saving
    """

    playlist_file = open(path_to_playlist_folder / file_name)
    lines = playlist_file.readlines()
    playlist_file.close()

    target_file_name = file_name
    f = open(path_to_destination_folder / target_file_name, "w")

    for line in lines:
        if not (line.startswith("#EXTINF:") or line.startswith("#EXTM3U")):

            line = str(line.replace(orginal_path, updated_path))
        f.write((unicodedata.normalize("NFC", line).encode("utf-8")).decode("utf-8"))

    f.close()


def m3u8_to_csv(path_to_playlist, playlist_name):
    """Create a csv file from a m3u8

    Args:
        path_to_playlist (_type_): path to playlist folder
        playlist_name (_type_): playlist name

    Returns:
        _type_: a pandas df containing the songs from the m3u8 file
    """

    file1 = open(path_to_playlist / playlist_name, "r")
    count = 0

    duration_list = []
    title_list = []
    artist_list = []
    location_list = []

    for line in file1:

        line_strip = line.strip()
        if line_strip.startswith("#EXTINF:"):

            line_strip = line_strip.replace("#EXTINF:", "")
            duration = line_strip.split(",")[0]
            line_strip = line_strip.replace(f"{duration},", "")
            title = line_strip.split(" - ")[0]
            artist = line_strip.split(" - ")[1]

            count += 1

            duration_list.append(duration)
            title_list.append(title)
            artist_list.append(artist)
        elif not line_strip.startswith("#EXT"):
            location = line.strip()
            location_list.append(location)

    # Closing files
    file1.close()

    df = pd.DataFrame(
        {
            "Artist": artist_list,
            "Title": title_list,
            "Total Time": duration_list,
            "Location": location_list,
        }
    )

    df.loc[:, "Location"] = df.loc[:, "Location"].apply(
        lambda x: Path(unquote(x.replace("file:", "")))
    )
    df.loc[:, "Album Location"] = df.loc[:, "Location"].apply(lambda x: x.parent)
    df.to_csv(path_to_playlist / playlist_name.replace("m3u8", "csv"))

    return df


def df_to_m3u8(df, file_name, path_to_m3u8_folder):
    """_summary_

    Args:
        df (_type_): _description_
        file_name (_type_): _description_
        path_to_m3u8_folder (_type_): _description_
    """

    if not file_name.endswith(".m3u8"):
        file_name += ".m3u8"

    f = open(path_to_m3u8_folder / file_name, "w+")
    f.write(f"#EXTM3U\r\n")

    for _, row in df.iterrows():

        total_time = row["Total Time"]
        name = row["Name"]
        artist = row["Artist"]
        location = str(row["Location"])

        f.write(f"#EXTINF:{round(int(total_time)/1000)} ,{name} - {artist}\r\n")
        f.write(f"{unquote(location)}\r\n".replace("%20", " "))

    f.close()


def PL_to_m3u8(
    path_to_playlists_folder,
    playlist,
):
    """_summary_

    Args:
        path_to_lib_folder (_type_): _description_
        playlist (_type_): _description_

    Returns:
        _type_: _description_
    """
    file_name = f"{playlist.itunesAttributes['Name']}.m3u8"
    if file_name in os.listdir():
        file_name = f"{playlist.itunesAttributes['Name']} -  {playlist.itunesAttributes['Playlist ID']}.m3u"

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

    df = pd.DataFrame(
        {
            "Artist": artist_list,
            "Name": name_list,
            "Total Time": total_time_list,
            "Location": location_list,
        }
    )
    df.loc[:, "Location"] = df.loc[:, "Location"].apply(lambda x: unquote(x))
    return df
