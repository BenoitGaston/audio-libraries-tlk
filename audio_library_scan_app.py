import streamlit as st

from  src.audio_libs_tlk.lib_scan import scan_and_process

import os

def main():
# Function for each menu option
    def scan_music_lib():
        st.title("Scan Music Library")
        st.write("Upload a file to scan and process.")
        
        # Additional string arguments
        path_to_library_data = st.text_input("Path to a directory containing an iTunes/Apple Music library .xml file or all a music library organized in folders (typically Artist/Album).", value="")
        orginal_path_written_in_playlists = st.text_input("Part of the path to be replaced in the original playlists (for instance '/Users/user_name/Music/'). Open an m3u8 playlist with a text editor to know what to use.", value="")
        updated_path_written_in_playlists = st.text_input("Part to be used in the new music location (for instance '/home/sony/walkman/Music'). Open an m3u8 playlist with a text editor to know what to use.", value="")
        
        # Additional binary (checkbox) arguments
        create_cover_jpg = st.checkbox("If True an image file called 'cover.jpg' will be created inside each location containig some music files. Only 1 file will be created per location. Even if two songs have distinct coverart", value=False)
        create_album_title_jpg = st.checkbox("If True an image file called 'title of the album.jpg' will be created inside each location containig some music files. Only 1 file will be created per location. Even if two songs have distinct coverart", value=False)
        complete_missing_cover_art = st.checkbox("Use the coverart of a song (any arbitrary one) conatinied in the same location to fil all the missing coverarts", value=False)
        convert_to_non_prog = st.checkbox("Convert the coverarts to non-prog images.", value=False)
        create_special_playlists = st.checkbox("Create some playlists and csv file to underline some aspects of a music library.", value=False)
        
        
        # Run button
        if st.button("Run"):
            st.session_state.confirmation_needed = True
            

        if st.session_state.get("confirmation_needed"):
            st.warning("Are you sure you want to run the process? Depending on the chosen options, the scanning process will potentially modify the metadata contained in your music files.")
            if st.button("Confirm"):

                scan_and_process(path_to_library_data = path_to_library_data,
                orginal_path_written_in_playlists = orginal_path_written_in_playlists,
                updated_path_written_in_playlists =  updated_path_written_in_playlists,
                create_cover_jpg = create_cover_jpg,
                create_album_title_jpg = create_album_title_jpg,
                complete_missing_cover_art = complete_missing_cover_art,
                convert_to_non_prog = convert_to_non_prog,
                create_special_playlists =  create_special_playlists)
                st.session_state.confirmation_needed = False

                st.success(f"The scan of your library has happened properly")
                st.success(f"If you have extracted")

            elif st.button("Cancel"):
                st.session_state.confirmation_needed = False
            
    scan_music_lib()
main()

