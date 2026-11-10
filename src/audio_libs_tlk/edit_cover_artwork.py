import os
from PIL import Image, ImageFile
import io
import music_tag
import pandas as pd
from .parameters import music_extentions, image_extentions
from pathlib import Path

import logging
from typing import List, Tuple

ImageFile.MAXBLOCK = 2**20

logger = logging.getLogger(__name__)


def assign_artwork_to_song(song_path: Path, image_path: Path) -> None:
    """Replace one audio file's embedded artwork with an image file.

    Args:
        song_path: Audio file whose artwork will be updated.
        image_path: JPEG or PNG file to embed.
    """

    song_tag = music_tag.load_file(song_path)

    with open(image_path, "rb") as image:
        song_tag["artwork"] = image.read()

    song_tag.save()


def assign_non_prog_artwork_to_song_list(
    music_dir: Path, music_files_paths: List[Path], album_title_from_path: str
):
    """Assign the album cover or album-title image to each supplied track.

    Args:
        music_dir: Album directory containing candidate image files.
        music_files_paths: Tracks to update.
        album_title_from_path: Album directory name used for a title image.
    """

    image_files_paths = get_image_files_paths(music_dir)

    if music_dir / "cover.jpg" in image_files_paths:
        image_path = music_dir / "cover.jpg"

        for song_path in music_files_paths:
            assign_artwork_to_song(song_path, image_path)
    elif music_dir / f"{album_title_from_path}.jpg" in image_files_paths:
        image_path = music_dir / f"{album_title_from_path}.jpg"

        for song_path in music_files_paths:
            assign_artwork_to_song(song_path, image_path)


def extract_artwork(
    song_path: Path,
    song_tag: music_tag.AudioFile,
    is_any_cover_image: bool,
    songs_wo_artwork: List[Path],
) -> Tuple[bool, List[Path]]:
    """Collect tracks without artwork and save the first available cover image.

    Args:
        song_path: Path of the track being inspected.
        song_tag: Loaded metadata object for the track.
        is_any_cover_image: Whether an image has already been found in the album.
        songs_wo_artwork: Accumulator for tracks without usable artwork.

    Returns:
        Whether the album has artwork and the accumulated missing-artwork tracks.
    """
    try:
        song_tag["artwork"]
        artwork = True
    except:

        artwork = False

    if not artwork:
        songs_wo_artwork.append(song_path)
    elif song_tag["artwork"] is None:
        songs_wo_artwork.append(song_path)
    elif song_tag["artwork"].first is None:
        songs_wo_artwork.append(song_path)

    else:
        if not is_any_cover_image:
            image = song_tag["artwork"].first.data

            save_image(
                image, song_path.parents[0], str(song_tag["title"]).replace("/", "_")
            )

            is_any_cover_image = True

    return is_any_cover_image, songs_wo_artwork


def extension_files_paths(dir_path: Path, extensions: List[str]) -> List[Path]:
    """Return non-AppleDouble files in a directory matching any extension."""
    files = os.listdir(str(dir_path))

    files = [
        f
        for f in files
        if (True in [f.lower().endswith(form) for form in extensions])
        and not f.startswith("._")
    ]

    paths = [dir_path / file for file in files]

    return paths


def get_music_files_paths(music_dir_path: Path) -> List[Path]:
    """Return supported audio files directly inside an album directory."""
    return extension_files_paths(music_dir_path, music_extentions)


def get_image_files_paths(music_dir_path: Path) -> List[Path]:
    """Return supported image files directly inside an album directory."""
    return extension_files_paths(music_dir_path, image_extentions)


def save_image(image_bytes: bytes, path_to_album: Path, image_save_name: str) -> None:
    """Save embedded image bytes as an optimized non-progressive JPEG."""
    image = Image.open(io.BytesIO(image_bytes))
    try:
        image.save(
            path_to_album / f"{image_save_name}.jpg",
            "JPEG",
            quality=80,
            optimize=True,
            progressive=False,
        )
    except:
        image = image.convert("RGB")
        image.save(
            path_to_album / f"{image_save_name}.jpg",
            "JPEG",
            quality=80,
            optimize=True,
            progressive=False,
        )


class EditCoverArtwork:
    """Apply configured cover-artwork operations to each album in a library."""

    def __init__(
        self,
        df_lib: pd.DataFrame,
        create_cover_jpg: bool = False,
        create_album_jpg: bool = False,
        complete_missing_cover_art: bool = False,
        convert_to_non_prog: bool = False,
    ):
        """Configure the artwork operations to apply to the library dataframe."""
        self.df_lib = df_lib
        self.create_cover_jpg = create_cover_jpg
        self.create_album_jpg = create_album_jpg
        self.complete_missing_cover_art = complete_missing_cover_art
        self.convert_to_non_prog = convert_to_non_prog

    def loop_over_albums_path(self) -> None:
        """Process each unique album location in the library dataframe."""
        paths_to_albums = list(self.df_lib.loc[:, "Album Location"].unique())

        logger.info("Processing cover artwork for %d albums", len(paths_to_albums))

        for path_to_album in paths_to_albums:
            path_to_album = Path(path_to_album)
            logger.debug("Processing cover artwork at %s", path_to_album)

            music_files_paths = get_music_files_paths(path_to_album)
            image_files_paths = get_image_files_paths(path_to_album)

            album_title_from_path = os.path.basename(path_to_album)

            is_any_cover_image = len(image_files_paths) > 0

            songs_wo_artwork_paths = []

            for song_path in music_files_paths:
                song_tag = music_tag.load_file(song_path)
                is_any_cover_image, songs_wo_artwork_paths = extract_artwork(
                    song_path, song_tag, is_any_cover_image, songs_wo_artwork_paths
                )

            if is_any_cover_image:

                image_files_paths = get_image_files_paths(path_to_album)

                image_file_path = image_files_paths[0]

                if self.create_cover_jpg:
                    with open(image_file_path, "rb") as image:

                        image = image.read()
                        save_image(image, path_to_album, image_save_name="cover")
                if self.create_album_jpg:
                    with open(image_file_path, "rb") as image:

                        image = image.read()
                        save_image(
                            image, path_to_album, image_save_name=album_title_from_path
                        )

                if self.convert_to_non_prog:

                    assign_non_prog_artwork_to_song_list(
                        path_to_album, music_files_paths, album_title_from_path
                    )

                if songs_wo_artwork_paths and self.complete_missing_cover_art:

                    assign_non_prog_artwork_to_song_list(
                        path_to_album, songs_wo_artwork_paths, album_title_from_path
                    )

            elif songs_wo_artwork_paths:
                logger.warning("Album has no artwork: %s", path_to_album)
