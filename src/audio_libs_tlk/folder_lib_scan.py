from __future__ import annotations

import os

import music_tag
import pandas as pd

import shutil
from .parameters import (
    tag_keys,
    itunes_cols,
    tags_to_itunes_cols_dict,
    music_extentions,
    playlist_extensions,
)
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


import datetime


def extract_tags(
    song_tag: music_tag.AudioFile, album_path: Path, song_file: Path
) -> dict:
    """Extract supported audio tags and filesystem locations from one file.

    Returns:
        Metadata compatible with the iTunes-style dataframe used by the package.
    """
    result_dict = {}
    keys_to_get = tag_keys + [
        col
        for col in itunes_cols
        if (
            col not in tag_keys
            and "#" + col not in tag_keys
            and "#" + col not in tags_to_itunes_cols_dict.values()
            and col not in tags_to_itunes_cols_dict.values()
        )
    ]
    for feature in keys_to_get:

        try:
            result_dict[feature] = str(song_tag[feature])
        except:
            result_dict[feature] = None

    result_dict["Location"] = album_path / song_file
    result_dict["Album Location"] = str(album_path)
    return result_dict


def loop_over_a_music_path(music_lib_path: Path) -> pd.DataFrame:
    """Scan all supported audio files below a music-library directory.

    Args:
        music_lib_path: Root directory to scan.

    Returns:
        Dataframe with one row per discovered audio file.
    """
    music_lib_list = []

    suffixes = music_extentions

    for album_path, _, filenames in os.walk(music_lib_path):
        logger.info("Scanning album at %s", album_path)

        for song_file in filenames:
            if os.path.splitext(song_file)[1].lower() in suffixes:

                album_path = Path(album_path)

                song_tag = music_tag.load_file(album_path / song_file)

                tags_dict = extract_tags(song_tag, album_path, song_file)

                music_lib_list.append(tags_dict)

    music_lib_df = pd.DataFrame(music_lib_list)

    return music_lib_df


def loop_over_a_songs_df(songs_df: pd.DataFrame) -> pd.DataFrame:
    """Rescan the audio files referenced by a dataframe.

    Args:
        songs_df: Dataframe containing a ``Location`` column.

    Returns:
        Dataframe containing refreshed metadata for each referenced file.
    """
    music_lib_list = []

    for _, row in songs_df.iterrows():

        song_location = row["Location"]
        album_path = Path(song_location).parent

        song_tag = music_tag.load_file(str(song_location).replace("file:", ""))
        tags_dict = extract_tags(song_tag, album_path, Path(song_location).name)

        music_lib_list.append(tags_dict)

    music_lib_df = pd.DataFrame(music_lib_list)

    return music_lib_df


def loop_over_playlist_path(music_lib_path: Path, path_to_dest_folder: Path) -> None:
    """Copy M3U8 files from a music library into a destination folder.

    Args:
        music_lib_path: Root directory containing playlists.
        path_to_dest_folder: Destination folder for copied playlists.
    """
    suffixes = playlist_extensions
    for playlist_path, _, filenames in os.walk(music_lib_path):
        for playlist_file in filenames:
            if os.path.splitext(playlist_file)[1].lower() in suffixes:
                if playlist_file not in os.listdir(path_to_dest_folder):
                    # (Path(playlist_path)/ playlist_file)
                    playlist_path = Path(playlist_path)

                    shutil.copy2(
                        Path(playlist_path) / playlist_file,
                        Path(path_to_dest_folder) / playlist_file,
                    )


def format_df_to_iTunes_csv_format(df_lib_scanned: pd.DataFrame) -> pd.DataFrame:
    """Normalize scanned tag names and numeric values to iTunes column names.

    Args:
        df_lib_scanned: Raw dataframe returned by the folder scanner.

    Returns:
        The normalized dataframe.
    """
    df_lib_scanned.rename(columns=tags_to_itunes_cols_dict, inplace=True)
    df_lib_scanned.rename(
        columns={col: col.replace("#", "") for col in df_lib_scanned.columns},
        inplace=True,
    )

    numeric_columns = [
        "Album Rating",
        "Artwork Count",
        "Bit Rate",
        "Disc Count",
        "Disc Number",
        "Movement Count",
        "Movement Number",
        "Play Count",
        "Play Date",
        "Rating",
        "Sample Rate",
        "Size",
        "Skip Count",
        "Track Count",
        "Track ID",
        "Track Number",
        "Year",
        "Total Time",
    ]

    numeric_columns = [col for col in numeric_columns if col in df_lib_scanned.columns]

    df_lib_scanned[numeric_columns] = df_lib_scanned[numeric_columns].apply(
        pd.to_numeric
    )
    return df_lib_scanned


class FolderLibraryScan:
    """Scan a folder-organized music library and preserve its playlists."""

    def __init__(
        self,
        path_to_music_folder: Path = None,
        path_to_dest_folder: Path = None,
        force_scan: bool = True,
    ):
        """Configure a folder scanner and ensure its playlist folder exists."""

        self.path_to_music_folder = path_to_music_folder
        self.path_to_dest_folder = path_to_dest_folder
        self.force_scan = force_scan

        if "Playlists" not in os.listdir(self.path_to_music_folder):
            os.mkdir(Path(self.path_to_music_folder) / "Playlists")

        self.path_to_playlist_folder = Path(self.path_to_music_folder) / "Playlists"

        self.df_lib = pd.DataFrame([])

    def get_folder_library_as_csv(self):
        """Load a cached folder scan or scan the music folder and save a CSV.

        Returns:
            Normalized dataframe containing the scanned track metadata.
        """

        files = os.listdir(self.path_to_dest_folder)

        scanned_files = sorted(
            [
                f
                for f in files
                if f.endswith(
                    f"{str(datetime.datetime.now().date())}_music_lib_scan.csv"
                )
            ]
        )

        if len(scanned_files) > 0 and not self.force_scan:
            logger.info("Loading cached music library scan from %s", scanned_files[-1])
            df_lib_scanned = pd.read_csv(self.path_to_dest_folder / scanned_files[-1])
        else:
            logger.info(
                "Scanning music library at %s; this may take a long time.",
                self.path_to_music_folder,
            )

            df_lib_scanned = loop_over_a_music_path(
                music_lib_path=self.path_to_music_folder
            )

        if not df_lib_scanned.empty:
            df_lib_scanned = format_df_to_iTunes_csv_format(df_lib_scanned)

        scan_path = (
            self.path_to_dest_folder
            / f"{str(datetime.datetime.now().date())}_music_lib_scan.csv"
        )
        df_lib_scanned.to_csv(scan_path, index=False)
        logger.info("Saved music library scan to %s", scan_path)
        return df_lib_scanned

    def get_all_playlists_from_a_folder(self):
        """Copy M3U8 playlists from the music folder into its playlist directory."""

        loop_over_playlist_path(self.path_to_music_folder, self.path_to_playlist_folder)
