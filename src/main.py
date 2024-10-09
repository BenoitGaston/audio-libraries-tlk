import os

from pathlib import Path
from lib_scan import LibraryScan
from processing_lib import LibraryProcessing
from edit_cover_artwork import EditCoverArtwork

import argparse

def run_full_library_scan(path_to_library_data,
                          orginal_path_written_in_playlists=None,
                         updated_path_written_in_playlists=None,
                         create_cover_jpg=False,
                         create_album_title_jpg=False,
                         complete_missing_cover_art=False,
                         convert_to_non_prog=False,
                         ):
    xml_files = [f for f in os.listdir(path_to_library_data)  
                 if f.endswith('.xml')]
    
    if len(xml_files)>0:
        path_to_library_file = Path(path_to_library_data)/xml_files[0]
        path_to_dest_folder = Path(path_to_library_data)
        path_to_music_folder = None
        path_to_playlist_folder = path_to_dest_folder/f'{xml_files[0]}_Playlists'
    else:
        path_to_library_file = None
        path_to_dest_folder = Path(path_to_library_data)
        path_to_music_folder = path_to_library_data
        path_to_playlist_folder = path_to_dest_folder/'Playlists'
    

    library_scan = LibraryScan(path_to_library_file = path_to_library_file,
                                path_to_music_folder=path_to_music_folder,
                                path_to_dest_folder=path_to_dest_folder,
                                path_to_playlist_folder = path_to_playlist_folder
                                    )
    
    lib_df = library_scan.get_library_as_csv()
    library_scan.get_library_playlists() 

    library_processing = LibraryProcessing(df_lib=lib_df,
                     path_to_playlist_folder=path_to_playlist_folder)
    
    library_processing.convert_playlists_with_new_path(orginal_path= orginal_path_written_in_playlists,
                    updated_path=updated_path_written_in_playlists)
    
    library_processing.get_special_playlists()

    edit_covers = EditCoverArtwork(df_lib = lib_df)

    edit_covers.loop_over_albums_path(create_cover_jpg=create_cover_jpg,
                                    create_album_jpg=create_album_title_jpg,
                                    complete_missing_cover_art=complete_missing_cover_art,
                                    convert_to_non_prog=convert_to_non_prog)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script that create some playlists from iTunes library"
    )
    parser.add_argument("--path_to_library_data", required=True, type=str, help='Blabla')
    parser.add_argument("--orginal_path_written_in_playlists", required=False, type=str, default=None, help='Blabla')
    parser.add_argument("--updated_path_written_in_playlists", required=False, type=str, default=None, help='Blabla')
    parser.add_argument("--create_cover_jpg", required=False, type=bool, default=False, help='Blabla')
    parser.add_argument("--create_album_title_jpg", required=False, type=bool, default=False, help='Blabla')
    parser.add_argument("--complete_missing_cover_art", required=False, default=False, help='Blabla')
    parser.add_argument("--convert_to_non_prog", required=False, default=False, help='Blabla')

    args = parser.parse_args()

    path_to_library_data = args.path_to_library_data
    orginal_path_written_in_playlists = args.orginal_path_written_in_playlists
    updated_path_written_in_playlists = args.updated_path_written_in_playlists
    create_cover_jpg = args.create_cover_jpg
    create_album_title_jpg = args.create_album_title_jpg
    complete_missing_cover_art = args.complete_missing_cover_art
    convert_to_non_prog = args.convert_to_non_prog



    run_full_library_scan(path_to_library_data, 
                          orginal_path_written_in_playlists,
                            updated_path_written_in_playlists,
                            create_cover_jpg,
                            create_album_title_jpg,
                            complete_missing_cover_art,
                            convert_to_non_prog)

