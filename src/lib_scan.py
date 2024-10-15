from itunes_lib_scan import iTunesLibraryScan
from folder_lib_scan import FolderLibraryScan


class LibraryScan:

    def __init__(
        self,
        path_to_library_file=None,
        path_to_music_folder=None,
        path_to_dest_folder=None,
        force_scan=True,
    ):

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

        if self.iTunes_lib:

            self.lib_df = self.Scan.get_itunes_library_as_csv()

        else:
            self.lib_df = self.Scan.get_folder_library_as_csv()
        return self.lib_df

    def get_library_playlists(self):

        if self.iTunes_lib:

            self.Scan.get_all_playlists_from_itunes_library()

        else:
            self.Scan.get_all_playlists_from_a_folder()
