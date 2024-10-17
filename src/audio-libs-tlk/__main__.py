from .lib_scan import scan_and_process

import argparse




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
        type=bool,
        default=False,
        help="Use the cover artworks of a song (any arbitrary one) conatinied in the same location to fil all the missing cover artworks.",
    )
    parser.add_argument(
        "--convert_to_non_prog",
        required=False,
        type=bool,
        default=False,
        help="Convert the cover artworks to non-prog images.",
    )

    parser.add_argument(
        "--create_special_playlists",
        required=False,
        type=bool,
        default=False,
        help="Create some playlists and csv file to underline some aspects of a music library.",
    )

    parser.add_argument(
        "--create_minidisc_labels",
        required=False,
        type=bool,
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
