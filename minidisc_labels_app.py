import streamlit as st

from  src.audio_libs_tlk.lib_scan import scan_and_process



def main():

    def create_md_labels():
        st.title("Create MiniDisc Labels")
        
        # Additional string arguments
        path_to_library_data = st.text_input("Path to a directory containing a .m3u8 playlist containing the string MiniDisc in its name).", value="")
        # Folder path input
        create_minidisc_labels = True
        
        # Run button
        if st.button("Run"):
            scan_and_process(path_to_library_data=path_to_library_data,
            create_minidisc_labels = create_minidisc_labels,)

    # Sidebar menu
    create_md_labels()
main()
