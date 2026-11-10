from .itunes_lib_scan import iTunesLibraryScan
from .folder_lib_scan import FolderLibraryScan
from .edit_cover_artwork import EditCoverArtwork

from .processing_lib import LibraryProcessing
from .models import ProcessingResult

from pathlib import Path
import os


OUTPUT_FILE_SUFFIXES = {".csv", ".m3u8", ".pickle"}


def collect_output_artifacts(
    library_data_path: Path, playlist_directory: Path
) -> list[Path]:
    """Return generated CSV, M3U8, and cache files for a processing operation."""
    artifacts = set()
    for output_directory in {library_data_path, playlist_directory}:
        if output_directory.exists():
            artifacts.update(
                path
                for path in output_directory.rglob("*")
                if path.is_file() and path.suffix.lower() in OUTPUT_FILE_SUFFIXES
            )
    return sorted(artifacts)


class LibraryScan:
    """Select and coordinate an iTunes XML or folder-based library scanner."""

    def __init__(
        self,
        path_to_library_file: Path = None,
        path_to_music_folder: Path = None,
        path_to_dest_folder: Path = None,
        force_scan: bool = True,
    ):
        """Choose an XML or folder scanner from the supplied source paths."""

        if path_to_library_file is not None and path_to_music_folder is None:

            self.Scan = iTunesLibraryScan(path_to_library_file, path_to_dest_folder)
            self.iTunes_lib = True

        elif path_to_library_file is None and path_to_music_folder is not None:

            self.Scan = FolderLibraryScan(
                path_to_music_folder,
                path_to_dest_folder,
                force_scan,
            )
            self.iTunes_lib = False

    def get_library_as_csv(self):
        """Return the selected library source as a track dataframe.

        Returns:
            iTunes-style track dataframe.
        """
        if self.iTunes_lib:

            self.lib_df = self.Scan.get_itunes_library_as_csv()

        else:
            self.lib_df = self.Scan.get_folder_library_as_csv()
        return self.lib_df

    def get_library_playlists(self):
        """Export or copy the playlists associated with the selected library."""

        if self.iTunes_lib:

            self.Scan.get_all_playlists_from_itunes_library()

        else:
            self.Scan.get_all_playlists_from_a_folder()


def scan_and_process(
    path_to_library_data: Path,
    orginal_path_written_in_playlists: Path = None,
    updated_path_written_in_playlists: Path = None,
    create_cover_jpg: bool = False,
    create_album_title_jpg: bool = False,
    complete_missing_cover_art: bool = False,
    convert_to_non_prog: bool = False,
    create_special_playlists: bool = False,
) -> ProcessingResult:
    """Scan a library and run the requested playlist and artwork operations.

    Args:
        path_to_library_data: Directory containing an XML export or music folders.
        orginal_path_written_in_playlists: Source prefix to replace in playlists.
        updated_path_written_in_playlists: Replacement prefix for converted playlists.
        create_cover_jpg: Create ``cover.jpg`` files from embedded artwork.
        create_album_title_jpg: Create title-named JPEG files from embedded artwork.
        complete_missing_cover_art: Copy available artwork to tracks missing it.
        convert_to_non_prog: Re-encode artwork as non-progressive JPEG.
        create_special_playlists: Export library consistency reports.

    Returns:
        Processing locations and the CSV, M3U8, and pickle artifacts available
        after the operation.
    """
    xml_files = [f for f in os.listdir(path_to_library_data) if f.endswith(".xml")]

    if len(xml_files) > 0:
        path_to_library_file = Path(path_to_library_data) / xml_files[0]
        path_to_dest_folder = Path(path_to_library_data)
        path_to_music_folder = None
        path_to_playlist_folder = (
            path_to_dest_folder / f"{xml_files[0].replace('.xml','_Playlists')}"
        )
        scan_only_for_playlists_convertion = False

    else:
        path_to_library_file = None
        path_to_dest_folder = Path(path_to_library_data)
        path_to_music_folder = path_to_library_data

        path_to_playlist_folder = path_to_dest_folder / "Playlists"
        if (
            orginal_path_written_in_playlists != None
            and updated_path_written_in_playlists != None
            and create_cover_jpg == False
            and create_album_title_jpg == False
            and complete_missing_cover_art == False
            and convert_to_non_prog == False
            and create_special_playlists == False
        ):
            scan_only_for_playlists_convertion = True
        else:
            scan_only_for_playlists_convertion = False

    library_scan = LibraryScan(
        path_to_library_file=path_to_library_file,
        path_to_music_folder=path_to_music_folder,
        path_to_dest_folder=path_to_dest_folder,
    )
    if scan_only_for_playlists_convertion:
        lib_df = None
    else:
        lib_df = library_scan.get_library_as_csv()

    library_scan.get_library_playlists()

    library_processing = LibraryProcessing(
        df_lib=lib_df, path_to_playlist_folder=path_to_playlist_folder
    )

    if (
        orginal_path_written_in_playlists != None
        and updated_path_written_in_playlists != None
    ):

        library_processing.convert_playlists_with_new_path(
            orginal_path=orginal_path_written_in_playlists,
            updated_path=updated_path_written_in_playlists,
        )
    if create_special_playlists:
        library_processing.get_special_playlists()
    if (
        create_cover_jpg
        | create_album_title_jpg
        | complete_missing_cover_art
        | convert_to_non_prog
    ):

        edit_covers = EditCoverArtwork(
            df_lib=lib_df,
            create_cover_jpg=create_cover_jpg,
            create_album_jpg=create_album_title_jpg,
            complete_missing_cover_art=complete_missing_cover_art,
            convert_to_non_prog=convert_to_non_prog,
        )

        edit_covers.loop_over_albums_path()

    return ProcessingResult(
        library_data_path=path_to_dest_folder,
        playlist_directory=path_to_playlist_folder,
        artifacts=collect_output_artifacts(
            library_data_path=path_to_dest_folder,
            playlist_directory=path_to_playlist_folder,
        ),
    )
