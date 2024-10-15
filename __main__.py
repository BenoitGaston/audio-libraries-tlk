import os

from pathlib import Path
from lib_scan import LibraryScan
from processing_lib import LibraryProcessing
from edit_cover_artwork import EditCoverArtwork
from create_md_labels import MiniDiscCovers

import argparse


def scan_and_process(
    path_to_library_data,
    orginal_path_written_in_playlists=None,
    updated_path_written_in_playlists=None,
    create_cover_jpg=False,
    create_album_title_jpg=False,
    complete_missing_cover_art=False,
    convert_to_non_prog=False,
    create_special_playlists=False,
    create_minidisc_labels=False,
):
    
    if create_minidisc_labels:
        minidisc_covers = MiniDiscCovers(path_to_music_folder=path_to_library_data)
        minidisc_covers.build_md_labels()
    else:
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
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script that extract and manipulate data from audio libraries."
    )
    parser.add_argument(
        "--path_to_library_data",
        required=True,
        type=str,
        help="Path to a directory containing an iTunes/Apple Music library .xml file or all a music library organized in folders (typically Artist/Album).",
    )
    parser.add_argument(
        "--orginal_path_written_in_playlists",
        required=False,
        type=str,
        default=None,
        help="Part of the path to be replaced in the original playlists (for instance '/Users/user_name/Music/'). Open an m3u8 playlist with a text editor to know what to use.",
    )
    parser.add_argument(
        "--updated_path_written_in_playlists",
        required=False,
        type=str,
        default=None,
        help="Part to be used in the new music location (for instance '/home/sony/walkman/Music'). Open an m3u8 playlist with a text editor to know what to use.",
    )
    parser.add_argument(
        "--create_cover_jpg",
        required=False,
        type=bool,
        default=False,
        help="If True an image file called 'cover.jpg' will be created inside each location containig some music files. Only 1 file will be created per location. Even if two songs have distinct cover artwork",
    )
    parser.add_argument(
        "--create_album_title_jpg",
        required=False,
        type=bool,
        default=False,
        help="If True an image file called 'title of the album.jpg' will be created inside each location containig some music files. Only 1 file will be created per location. Even if two songs have distinct cover artworks.",
    )
    parser.add_argument(
        "--complete_missing_cover_art",
        required=False,
        default=False,
        help="Use the cover artworks of a song (any arbitrary one) conatinied in the same location to fil all the missing cover artworks.",
    )
    parser.add_argument(
        "--convert_to_non_prog",
        required=False,
        default=False,
        help="Convert the cover artworks to non-prog images.",
    )

    parser.add_argument(
        "--create_special_playlists",
        required=False,
        default=False,
        help="Create some playlists and csv file to underline some aspects of a music library.",
    )

    parser.add_argument(
        "--create_minidisc_labels",
        required=False,
        default=False,
        help="From an .m3u8 file, create some MiniDisc labels using the cover artwork present in the audio library.",
    )

    args = parser.parse_args()

    path_to_library_data = args.path_to_library_data
    orginal_path_written_in_playlists = args.orginal_path_written_in_playlists
    updated_path_written_in_playlists = args.updated_path_written_in_playlists
    create_cover_jpg = args.create_cover_jpg
    create_album_title_jpg = args.create_album_title_jpg
    complete_missing_cover_art = args.complete_missing_cover_art
    convert_to_non_prog = args.convert_to_non_prog
    create_special_playlists = args.create_special_playlists
    create_minidisc_labels = args.create_minidisc_labels

    scan_and_process(
        path_to_library_data,
        orginal_path_written_in_playlists,
        updated_path_written_in_playlists,
        create_cover_jpg,
        create_album_title_jpg,
        complete_missing_cover_art,
        convert_to_non_prog,
        create_special_playlists,
        create_minidisc_labels,
    )
