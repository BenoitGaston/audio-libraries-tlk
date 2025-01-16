import streamlit as st

from  src.audio_libs_tlk.lib_scan import scan_and_process

from pathlib import Path

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

            
            st.success(f"Your MiniDisc Labels have been created and are available under this path: {Path(path_to_library_data)}/MiniDisc-Labels")
            st.write("After reviewing the svg files created, you might find necessary to modify (in particular shorten/abreviate) some Artist and Album names. You might also want to update the text and background colomns label by label")
            st.write("This can be done by")
            st.write(f"1: Updating the file called 'your-playlist-name_albums.csv' (for instance 'MiniDisc_albums.csv') present in {Path(path_to_library_data)}")
            st.write("In this csv file, you can modify (in particular shorten/abbreviate) the values in the columns 'Display Album','Display Album Artist' (becarefull not to change the columns 'Album','Album Artist' ) and file the columns text_color and background_color")
            st.write("2: After saving the updated csv file, just press again the Run button above.")
            st.write("You can use custom text and background colors using any hexadecimal color or use one of the colors (as a string) in the list below.")
            st.code("""'black','sky_blue','blue','blue_steel','blue_green',
                        'navy_blue','blue_turquoise','fushia','gold','green',
                        'pink','purple_light','purple','orange','red','yellow',
                        'white','silver'""")





    # Sidebar menu
    create_md_labels()
main()
