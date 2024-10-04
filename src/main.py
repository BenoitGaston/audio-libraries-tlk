import os
import xml.etree.ElementTree as ET  ## XML parsing

from itunes_lib_scan import LibScan


#

lib_location = os.path.join(os.path.dirname(os.getcwd()), "itunes-lib-data")
lib_name = "iTunes Music Library-2024-05-24"
path_to_dest_folder = lib_location
sd_walkman_path = "/Volumes/MasterAudio/NewiTunes/iTunes Media/Music"
new_root_folder = "/Volumes/MasterAudio/NewiTunes/iTunes Media/Music"
path_to_music_folder = (
    None  #'/Volumes/MasterAudio/Audio/Gros iTunes/2024-04-AppleMusic/'
)


create_cover_jpg = False
create_album_jpg = False
complete_missing_cover_art = False  #
convert_to_non_prog = False
force_scan = False
skip_scanning = True


LS = LibScan(
    path_to_library_file=os.path.join(lib_location, lib_name),
    path_to_dest_folder=path_to_dest_folder,
    path_to_music_folder=path_to_music_folder,
    create_cover_jpg=create_cover_jpg,
    create_album_jpg=create_album_jpg,
    complete_missing_cover_art=complete_missing_cover_art,
    convert_to_non_prog=convert_to_non_prog,
    force_scan=force_scan,
    skip_scanning=skip_scanning,
)


LS.get_all_playlists_from_a_lib()
LS.get_all_playlists_with_alternative_path(new_root_folder=new_root_folder)
LS.get_locations_with_multiple_album()

LS.split_lib_by_features(
    split_features=[
        "Grand Genre",
        "CD Scoring",
    ],
    maximum_size_feature="CD Total Time",
    maximum_bin_size_in_hours=40,
    maximum_bin_size_in_gb=30,
    mix_genre=False,
)

LS.split_lib_by_location(
    audio_location="/Volumes/MasterAudio/Audio/Gros iTunes/", level=0
)

LS.split_lib_by_format()
LS.split_lib_by_resolution()
