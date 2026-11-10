"""Command-line entry point for scanning and processing an audio library."""

import argparse
from pathlib import Path

from .lib_scan import scan_and_process


def parse_bool(value: str) -> bool:
    """Parse a case-insensitive command-line boolean value."""
    normalized_value = value.lower()
    if normalized_value in {"true", "1", "yes"}:
        return True
    if normalized_value in {"false", "0", "no"}:
        return False
    raise argparse.ArgumentTypeError("Expected true or false.")


def main() -> None:
    """Parse command-line options and scan the requested audio library."""
    parser = argparse.ArgumentParser(
        description="Scan an iTunes XML export or folder-organized music library."
    )
    parser.add_argument(
        "--path-to-library-data",
        required=True,
        type=Path,
        help="Directory containing an XML export or music folders.",
    )
    parser.add_argument(
        "--original-path-written-in-playlists",
        type=Path,
        help="Source path prefix to replace in M3U8 playlists.",
    )
    parser.add_argument(
        "--updated-path-written-in-playlists",
        type=Path,
        help="Replacement path prefix for converted M3U8 playlists.",
    )
    for argument, help_text in (
        (
            "--create-cover-jpg",
            "Create cover.jpg files from embedded artwork.",
        ),
        (
            "--create-album-title-jpg",
            "Create album-title JPEG files from embedded artwork.",
        ),
        (
            "--complete-missing-cover-art",
            "Copy available album artwork to tracks missing it.",
        ),
        (
            "--convert-to-non-prog",
            "Re-encode artwork as non-progressive JPEG.",
        ),
        (
            "--create-special-playlists",
            "Create CSV and M3U8 consistency reports.",
        ),
    ):
        parser.add_argument(argument, type=parse_bool, default=False, help=help_text)

    args = parser.parse_args()
    scan_and_process(
        path_to_library_data=args.path_to_library_data,
        orginal_path_written_in_playlists=args.original_path_written_in_playlists,
        updated_path_written_in_playlists=args.updated_path_written_in_playlists,
        create_cover_jpg=args.create_cover_jpg,
        create_album_title_jpg=args.create_album_title_jpg,
        complete_missing_cover_art=args.complete_missing_cover_art,
        convert_to_non_prog=args.convert_to_non_prog,
        create_special_playlists=args.create_special_playlists,
    )


if __name__ == "__main__":
    main()
