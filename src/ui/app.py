"""Local Streamlit interface for scanning and processing audio libraries."""

from pathlib import Path

import streamlit as st

from audio_libs_tlk.lib_scan import scan_and_process
from ui.logic import artwork_execution_allowed


ARTWORK_OPERATION_LABELS = {
    "create_cover_jpg": "Create cover.jpg files",
    "create_album_title_jpg": "Create album-title JPEG files",
    "complete_missing_cover_art": "Fill tracks with missing artwork",
    "convert_to_non_prog": "Convert artwork to non-progressive JPEG",
}


def render_artifact_downloads(artifacts: list[Path], library_data_path: Path) -> None:
    """Render download controls for artifacts created or available after a run."""
    if not artifacts:
        st.info("The operation completed without CSV, M3U8, or pickle artifacts.")
        return

    st.subheader("Output files")
    for artifact in artifacts:
        display_name = artifact.relative_to(library_data_path)
        with open(artifact, "rb") as artifact_file:
            st.download_button(
                label=f"Download {display_name}",
                data=artifact_file.read(),
                file_name=artifact.name,
                key=str(artifact),
            )


def main() -> None:
    """Render the application and execute the selected processing workflow."""
    st.set_page_config(page_title="Audio Libraries Toolkit", page_icon="🎵")
    st.title("Audio Libraries Toolkit")
    st.caption("Scan a local music library, convert playlists, and generate reports.")

    st.warning(
        "Artwork options modify source audio files. Use a copy of your library first."
    )

    with st.form("library-processing"):
        library_path_text = st.text_input(
            "Library directory",
            help="Directory containing an iTunes/Apple Music XML export or music folders.",
        )
        st.subheader("Playlist conversion")
        original_path = st.text_input("Original path in playlists (optional)")
        updated_path = st.text_input("Replacement path in playlists (optional)")

        st.subheader("Artwork operations")
        artwork_options = {
            option: st.checkbox(label)
            for option, label in ARTWORK_OPERATION_LABELS.items()
        }

        st.subheader("Reports")
        create_special_playlists = st.checkbox(
            "Create special playlists and consistency reports"
        )

        artwork_selected = any(artwork_options.values())
        session_allowed = st.session_state.get("artwork_always_allowed", False)
        confirmed_for_run = False
        remember_confirmation = False
        if artwork_selected and not session_allowed:
            st.error("Artwork changes are selected and will modify source audio files.")
            confirmed_for_run = st.checkbox(
                "I understand that selected artwork operations modify audio files."
            )
            remember_confirmation = st.checkbox(
                "Always allow artwork operations during this session",
                disabled=not confirmed_for_run,
            )
        elif artwork_selected:
            st.info("Artwork operations are authorized for this browser session.")

        submitted = st.form_submit_button("Run processing")

    if not submitted:
        return

    errors = []
    if not library_path_text.strip():
        errors.append("Enter a library directory.")
    elif not Path(library_path_text).expanduser().is_dir():
        errors.append("The library directory does not exist.")
    if bool(original_path.strip()) != bool(updated_path.strip()):
        errors.append("Provide both playlist conversion paths or leave both blank.")
    if not artwork_execution_allowed(
        artwork_selected, confirmed_for_run, session_allowed
    ):
        errors.append("Confirm the artwork changes before running them.")

    if errors:
        for error in errors:
            st.error(error)
        return

    if remember_confirmation:
        st.session_state["artwork_always_allowed"] = True

    library_data_path = Path(library_path_text).expanduser()
    with st.spinner("Processing the music library..."):
        try:
            result = scan_and_process(
                path_to_library_data=library_data_path,
                orginal_path_written_in_playlists=(
                    Path(original_path).expanduser() if original_path else None
                ),
                updated_path_written_in_playlists=(
                    Path(updated_path).expanduser() if updated_path else None
                ),
                create_cover_jpg=artwork_options["create_cover_jpg"],
                create_album_title_jpg=artwork_options["create_album_title_jpg"],
                complete_missing_cover_art=artwork_options[
                    "complete_missing_cover_art"
                ],
                convert_to_non_prog=artwork_options["convert_to_non_prog"],
                create_special_playlists=create_special_playlists,
            )
        except (OSError, ValueError) as error:
            st.exception(error)
            return

    st.success("Processing completed.")
    st.caption(f"Playlist directory: {result.playlist_directory}")
    render_artifact_downloads(result.artifacts, result.library_data_path)


if __name__ == "__main__":
    main()
