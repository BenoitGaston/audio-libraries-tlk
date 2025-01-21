from .convertion_functions import df_to_m3u8
from .convertion_functions import convert_a_playlist
import numpy as np
from pathlib import Path
import pandas as pd
import os


def group_by_cd(x):
    """_summary_

    Args:
        x (_type_): _description_
    """
    if "Total Time" in x.columns:
        total_duration = np.sum(x["Total Time"])
    else:
        total_duration = -1
    if "Size" in x.columns:
        size = sum(x["Size"].astype(int))
    else:
        size = -1
    if "it Rate" in x.columns:
        mean_bit_rate = np.mean(x["Bit Rate"].astype(int))
    else:
        mean_bit_rate = 0
    num_track = len(x)

    if "Track Number" in x.columns:

        min_track = np.min(x["Track Number"])
        max_track = np.max(x["Track Number"])
        track_num_delta = max_track + 1 - min_track
        all_track_present = track_num_delta == num_track
    else:
        min_track = 0
        max_track = 0
        track_num_delta = None
        all_track_present = None
    if "Rating" in x.columns:
        min_rating = np.min(x["Rating"])
        max_rating = np.max(x["Rating"])
        avg_rating = np.mean(x["Rating"])
    else:
        min_rating = None
        max_rating = None
        avg_rating = None

    album_type = x.Kind.mode()[0]
    if "Year" in x.columns:
        try:
            album_year = x.Year.mode()[0]
        except:
            album_year = None

    else:
        album_year = None
    if "Genre" in x.columns:
        album_multi_genre = len(x["Genre"].unique()) > 1
        album_genre = x.Genre.mode()[0]
    else:
        album_multi_genre = None
        album_genre = None

    album_location = x["Album Location"].mode()[0]
    album_multi_location = len(x["Album Location"].unique()) > 1
    try:
        principal_artist = x["Artrist"].mode()[0]
    except:
        principal_artist = None 

    return pd.Series(
        {
            "CD Total Time": total_duration,
            "CD Size": size,
            "CD Rating Min": min_rating,
            "CD Rating Max": max_rating,
            "CD Rating AVG": avg_rating,
            "CD Bit Rate": mean_bit_rate,
            "CD Files Kind": album_type,
            "CD Location": album_location,
            "CD Year": album_year,
            "CD Has Multiple Locations": album_multi_location,
            "CD Genre": album_genre,
            "CD Has Multiple Genre": album_multi_genre,
            "Num Tracks": num_track,
            "Min Track Number": min_track,
            "Max Track Number": max_track,
            "Track Number Delta": track_num_delta,
            "CD Is Missing Tracks": ~all_track_present,
            "CD Principal Artist" :  principal_artist,
        }
    )


class LibraryProcessing:

    def __init__(self, path_to_playlist_folder, df_lib=None):

        self.df_lib = df_lib
        self.path_to_playlist_folder = path_to_playlist_folder
        if type(self.path_to_playlist_folder) == str:
            self.path_to_playlist_folder = Path(self.path_to_playlist_folder)

        if not os.path.isdir(self.path_to_playlist_folder):

            os.mkdir(self.path_to_playlist_folder)

    def convert_playlists_with_new_path(
        self,
        destination_folder="Converted_Playlists",
        orginal_path=Path("."),
        updated_path=Path("."),
    ):

        if destination_folder not in os.listdir(self.path_to_playlist_folder):
            os.mkdir(self.path_to_playlist_folder / destination_folder)

        destination_path = self.path_to_playlist_folder / destination_folder

        files_list = [
            f
            for f in os.listdir(self.path_to_playlist_folder)
            if (f.endswith(".m3u8") and not f.startswith("._"))
        ]

        for file_name in files_list:

            convert_a_playlist(
                path_to_playlist_folder=self.path_to_playlist_folder,
                path_to_destination_folder=destination_path,
                orginal_path=orginal_path,
                updated_path=updated_path,
                file_name=file_name,
            )

    def get_special_playlists(self):
        path_to_pl = self.path_to_playlist_folder / "Special_Playlists"
        if "Special_Playlists" not in os.listdir(self.path_to_playlist_folder):
            os.mkdir(path_to_pl)
        self.get_album_and_disc_df()
        self.get_locations_with_multiple_album()
        self.get_disc_with_missing_tracks()
        self.get_album_with_multiple_genre()
        self.split_library_by_resolution()
        self.split_library_by_format()

    def get_grouped_df(self, path_to_destination=None, disc_or_album="Album"):
        """_summary_

        Args:
            path_to_lib (_type_): _description_
            lib_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        if path_to_destination is None:

            path_to_destination = self.path_to_playlist_folder / "Special_Playlists"
        df_lib = self.df_lib.copy()
        df_lib.loc[:, "Album"] = df_lib.loc[:, "Album"].apply(lambda x: str(x).strip())


        df_lib.loc[:, "Track Number"] = df_lib.loc[:, "Track Number"].fillna(0)
        df_lib.loc[:, "Track Number"] = df_lib.loc[:, "Track Number"].replace("", 0)
        df_lib.loc[:, "Track Number"] = df_lib.loc[:, "Track Number"].astype(int)

        df_lib.loc[:, "Size"] = df_lib.loc[:, "Size"].fillna(
            df_lib.loc[:, "Bit Rate"] * df_lib.loc[:, "Total Time"]
        )

        # df_lib.loc[:, "Year"] = df_lib.loc[:, "Year"].fillna(0)

        group_features = [
            "Album",
            "Album Artist",
        ]
        if disc_or_album == "Disc":
            group_features.append("Disc Number")

        grouped_df = df_lib.groupby(by=group_features).apply(group_by_cd).reset_index()
        grouped_df.rename(
            columns={
                col: col.replace("CD", disc_or_album) for col in grouped_df.columns
            },
            inplace=True,
        )

        #df_lib.loc[:, "Album Artist"] = df_lib.loc[:, "Album Artist"].fillna(df_lib.loc[:,"Artist"])
        # df_lib.loc[:, "Album Artist"] = df_lib.loc[:,"Album Artist"].apply(
        #    lambda x: str(x).strip()
        # )

        # grouped_df.loc[:,'cumsum_time'] = np.cumsum((grouped_df.loc[:,'Total Time']/1000)/(4*60*60))

        self.df_lib = df_lib[
            group_features
            + [col for col in df_lib.columns if col not in grouped_df.columns]
        ].merge(grouped_df, on=group_features)
        grouped_df.to_csv(path_to_destination / f"{disc_or_album}.csv")

        return grouped_df

    def get_album_and_disc_df(self):

        self.album_df = self.get_grouped_df(disc_or_album="Album")
        self.disc_df = self.get_grouped_df(disc_or_album="Disc")

    def get_locations_with_multiple_album(self):

        def group_by_location(x):

            return pd.Series({"Number of Album in Location": len(x.Album.unique())})

        df = self.df_lib.copy()

        grouped_df = (
            df.groupby(by="Album Location").apply(group_by_location).reset_index()
        )

        df = pd.merge(df, grouped_df, on="Album Location", how="left")

        grouped_df[grouped_df["Number of Album in Location"] > 1].to_csv(
            self.path_to_playlist_folder
            / "Special_Playlists/Locations_with_multiple_albums.csv",
            index=False,
        )

        df_to_m3u8(
            df[df["Number of Album in Location"] > 1],
            "Locations_with_multiple_albums",
            self.path_to_playlist_folder / "Special_Playlists",
        )

    def get_disc_or_album_with_multiple_values(
        self, disc_or_album="Album", feature="Has Multiple Genre"
    ):

        if disc_or_album == "Album":

            df_grouped = self.album_df.copy()
        else:
            df_grouped = self.disc_df.copy()

        df_grouped = df_grouped[df_grouped[f"{disc_or_album} {feature}"]]

        df_grouped.to_csv(
            self.path_to_playlist_folder
            / f"Special_Playlists/{disc_or_album} {feature}.csv",
            index=False,
        )

        df = self.df_lib.copy()
        df = df[df[f"{disc_or_album} {feature}"]]

        df_to_m3u8(
            df,
            f"{disc_or_album} {feature}",
            self.path_to_playlist_folder / "Special_Playlists",
        )

    def get_disc_with_missing_tracks(self):

        self.get_disc_or_album_with_multiple_values(
            disc_or_album="Disc", feature="Is Missing Tracks"
        )

    def get_album_with_multiple_genre(self):

        self.get_disc_or_album_with_multiple_values(
            disc_or_album="Album", feature="Has Multiple Genre"
        )

    def split_library_by_resolution(self, resolutions=[128, 192, 256, 320, 1000]):

        path_to_pl = self.path_to_playlist_folder / "Playlists_by_Resolution"
        if "Playlists_by_Resolution" not in os.listdir(self.path_to_playlist_folder):
            os.mkdir(path_to_pl)

        df_temp = self.df_lib.copy()

        for res in sorted(resolutions):
            df = df_temp[df_temp["Disc Bit Rate"] <= res]
            df_temp = df_temp[df_temp["Disc Bit Rate"] > res]

            file_name = f"up_to_{res}_kbps"

            df_to_m3u8(df, file_name, path_to_pl)

        file_name = f"above_{res}_kbps"
        df_to_m3u8(df_temp, file_name, path_to_pl)

    def split_library_by_format(self):
        path_to_pl = self.path_to_playlist_folder / "Playlists_by_Format"
        if "Playlists_by_Format" not in os.listdir(self.path_to_playlist_folder):
            os.mkdir(path_to_pl)
        for format in self.df_lib["Disc Files Kind"].unique():
            df = self.df_lib[self.df_lib["Disc Files Kind"] == format]
            file_name = f"{format}_files"
            df_to_m3u8(df, file_name, path_to_pl)

    '''def split_lib_by_features(
        self,
        split_features=["Genre", "CD Rating AVG"],
        maximum_size_feature="CD Size",
        maximum_bin_size_in_hours=4,
        maximum_bin_size_in_gb=1,
        mix_genre=False,
    ):
        """_summary_

        Args:
            lib_name (_type_): _description_
            path_to_lib_folder (_type_): _description_
            split_type (list, optional): _description_. Defaults to ['Genre','CD Rating AVG',].
            maximum_size_feature (str, optional): _description_. Defaults to 'CD Size'.
            maximum_bin_size_in_hours (int, optional): _description_. Defaults to 4.
            maximum_bin_size_in_gb (int, optional): _description_. Defaults to 1.
        """

        if not mix_genre:

            split_genre = "Genre"

            list_of_df_to_split = []

            for genre in self.df_cd[split_genre].sort_values().unique():

                list_of_df_to_split.append(
                    self.df_cd[self.df_cd[split_genre] == genre].copy()
                )
        else:
            list_of_df_to_split = [self.df_cd.copy()]
            split_genre = "Genre"

        if split_features == None:
            split_type = "random"
        else:
            split_type = split_features

        all_sorted_df_list = []
        all_sorted_df = pd.DataFrame([])
        max_pl_id = 0

        for df_cd_to_split in list_of_df_to_split:

            if split_type == "random":

                sorted_df = df_cd_to_split.sample(frac=1)
                split_name = "random"
            elif type(split_type) == list:
                sorted_df = df_cd_to_split.sample(frac=1)
                sorted_df = sorted_df.sort_values(by=split_type)

                split_name = split_type[0]

                if len(split_type) > 1:
                    for st in split_type[1:]:
                        split_name += "_" + st

                split_name += "_"

            if maximum_size_feature == "CD Total Time":
                maximum_bin_size = maximum_bin_size_in_hours * 60 * 60 * 1000

            else:

                maximum_bin_size = maximum_bin_size_in_gb * (1000 * 1000 * 1000)

            sorted_df.loc[:, "PL Id"] = (
                np.cumsum(
                    (sorted_df.loc[:, maximum_size_feature]) / (maximum_bin_size)
                ).astype(int)
                + max_pl_id
            )

            all_sorted_df = pd.concat([all_sorted_df, sorted_df])

            max_pl_id = 1 + np.max(sorted_df.loc[:, "PL Id"])

        all_sorted_df.loc[:, "PL Id"] = all_sorted_df.loc[:, "PL Id"].astype(str)

        def group_by_pl(x):
            """_summary_

            Args:
                x (_type_): _description_

            Returns:
                _type_: _description_
            """

            mean_rating = round(np.mean(x["CD Rating AVG"]), 1)
            med_genre = x[split_genre].mode()[0].replace("/", "-")
            return pd.Series(
                {
                    "PL Rating": mean_rating,
                    "PL Genre": med_genre,
                    "PL Name": f"{med_genre}_{mean_rating}_",
                }
            )

        # all_sorted_df = pd.concat(all_sorted_df_list)

        pl_df = all_sorted_df.groupby(by="PL Id").apply(group_by_pl)

        all_sorted_df = all_sorted_df.merge(pl_df, on="PL Id")

        all_sorted_df.loc[:, "PL Name"] = (
            all_sorted_df.loc[:, "PL Name"] + all_sorted_df.loc[:, "PL Id"]
        )

        PL_folder_name = f"split_{maximum_size_feature}_{split_type}"

        path_to_pl = self.path_to_dest_folder/PL_folder_name

        if PL_folder_name not in os.listdir(self.path_to_dest_folder):
            os.mkdir(path_to_pl)

        group_features = [
            "Album",
            "Album Artist",
            "Disc Number",
            "Genre",
            "Disc Count",
        ]

        # grouped_df = df_lib.groupby(by=group_features).apply(group_by_cd).reset_index()

        # grouped_df.loc[:,'cumsum_time'] = np.cumsum((grouped_df.loc[:,'Total Time']/1000)/(4*60*60))
        lib_df = self.df_lib.copy()
        lib_df = lib_df.merge(
            all_sorted_df[group_features + ["PL Name"]], on=group_features
        )

        for pl_name in all_sorted_df.loc[:, "PL Name"].unique():

            lib_df[lib_df.loc[:, "PL Name"] == pl_name].to_csv(path_to_pl/"{pl_name}.csv")

            df_to_m3u8(lib_df[lib_df.loc[:, "PL Name"] == pl_name], pl_name, path_to_pl)

    def split_lib_by_location(self, audio_location, level):
        lib_df = self.df_lib.copy()
        lib_df.dropna(subset=["Total Time"], inplace=True)
        lib_df.loc[:, "Location_rep"] = lib_df.Location
        lib_df.loc[:, "audio_loc_in_loc"] = lib_df.Location_rep.apply(
            lambda x: audio_location in x
        )

        lib_df.loc[:, "level_max"] = np.where(
            lib_df.loc[:, "audio_loc_in_loc"],
            lib_df.Location_rep.apply(
                lambda x: len(x.split(audio_location)[-1].split("/"))
            ),
            0,
        )

        lib_df.loc[:, "pl_name"] = np.where(
            lib_df.loc[:, "audio_loc_in_loc"],
            lib_df.Location_rep.apply(
                lambda x: "_".join(
                    x.split(audio_location)[-1].split("/")[
                        0 : min(
                            [level + 1, len(x.split(audio_location)[-1].split("/"))]
                        )
                    ]
                )
            ),
            0,
        )
        path_to_pl = self.path_to_dest_folder/(audio_location.replace("/", "_") + "_PL")
        

        if audio_location.replace("/", "_") + "_PL" not in os.listdir(
            self.path_to_dest_folder
        ):
            os.mkdir(path_to_pl)

        for pl_name in lib_df.loc[:, "pl_name"].unique():
            if pl_name != 0:
                if len(lib_df[lib_df.pl_name == pl_name]) > 1:
                    df_to_m3u8(
                        lib_df[lib_df.pl_name == pl_name],
                        pl_name.replace(" ", "_"),
                        path_to_pl,
                    )'''
