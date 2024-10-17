import pandas as pd
import os
import xml.etree.ElementTree as ET  ## XML parsing
from collections import defaultdict
import numpy as np
from itunesLibrary import library
from urllib.parse import unquote

from .convertion_functions import PL_to_m3u8
from .parameters import itunes_numeric_columns,itunes_bool_columns,itunes_usefull_cols,itunes_date_columns

import pickle

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class iTunesLibraryScan:

    def __init__(
        self,
        path_to_library_file=None,
        path_to_dest_folder=None,
    ):

        if path_to_dest_folder != None:
            self.path_to_dest_folder = path_to_dest_folder
        else:
            self.path_to_dest_folder = os.getcwd().parent[1] / "itunes-lib-data"

            if "itunes-lib-data" not in os.listdir(os.getcwd().parent[1]):
                os.mkdir(self.path_to_dest_folder)

        self.path_to_library_file = path_to_library_file
        self.path_to_library_folder = self.path_to_library_file.parent
        self.lib_name = self.path_to_library_file.name

        self.path_to_library_file = path_to_library_file

        self.path_to_playlists_folder = (
            self.path_to_dest_folder / self.lib_name.replace(".xml", "_Playlists")
        )

        if self.lib_name.replace(".xml", "_Playlists") not in os.listdir(
            self.path_to_dest_folder
        ):
            os.mkdir(self.path_to_playlists_folder)

        self.lib_lib = self.get_lib_as_lib_object()

    def get_lib_as_lib_object(self):
        """_summary_

        Args:
            path_to_lib_folder (_type_): _description_
            lib_name (_type_): _description_

        Returns:
            _type_: _description_
        """

        pkl_name = self.lib_name.replace(".xml", ".pickle")

        if pkl_name in os.listdir(self.path_to_dest_folder):

            with open(self.path_to_dest_folder / pkl_name, "rb") as handle:

                lib = pickle.load(handle)
        else:
            # must first parse...

            logging.info(
                f"! Be Patient. Parsing your {self.lib_name} will take a long time (~60mins for a 30k songs lib with a Mac mini M2) !"
            )
            lib = library.parse(self.path_to_library_file)

            with open(self.path_to_dest_folder / pkl_name, "wb") as handle:
                pickle.dump(lib, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return lib

    def convert_lib_to_csv(self):
        """_summary_

        Args:
            path_to_lib_folder (_type_): _description_
            lib_name (_type_): _description_

        Returns:
            _type_: _description_
        """

        tree = ET.parse(self.path_to_library_file)
        root = tree.getroot()

        columns = sorted(
            list(
                set(
                    [
                        root[0][17][i][j].text
                        for i, _ in enumerate(root[0][17])
                        for j, _ in enumerate(root[0][17][i])
                        if root[0][17][i][j].tag == "key"
                    ]
                )
            )
        )

        data = defaultdict(list)

        for i, _ in enumerate(root[0][17]):
            temp_columns = list.copy(columns)
            if i % 2 == 1:
                for j, _ in enumerate(root[0][17][i]):
                    if root[0][17][i][j].tag == "key":
                        if root[0][17][i][j].text in itunes_bool_columns:
                            data[root[0][17][i][j].text].append(
                                root[0][17][i][j + 1].tag
                            )
                            temp_columns.remove(root[0][17][i][j].text)
                        else:
                            data[root[0][17][i][j].text].append(
                                root[0][17][i][j + 1].text
                            )
                            temp_columns.remove(root[0][17][i][j].text)
                for column in temp_columns:
                    data[column].append(np.nan)
        df = pd.DataFrame(data)

        logging.info(f"Shape of your Lib Data {df.shape}")
        logging.info(f"Columns of your Lib csv {df.columns}")

        df[itunes_numeric_columns] = df[itunes_numeric_columns].apply(
            pd.to_numeric
        )

        df[itunes_date_columns] = df[itunes_date_columns].apply(
            pd.to_datetime
        )

        df["Play Date"] = pd.to_datetime(df["Play Date"] - 2082826800, unit="s")

        # df.loc[:,'Total Time'] = pd.to_timedelta(df['Total Time'], unit='ms')

        df[["Album Rating", "Rating", "Bit Rate"]] = df[
            ["Album Rating", "Rating", "Bit Rate"]
        ].fillna(0)

        df[itunes_usefull_cols].to_csv(
            self.path_to_dest_folder / self.lib_name.replace(".xml", ".csv"),
            index=False,
        )

        return df[itunes_usefull_cols]

    def get_itunes_library_as_csv(self):
        """_summary_

        Args:
            path_to_lib_folder (_type_): _description_
            lib_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        csv_name = self.lib_name.replace(".xml", ".csv")
        if csv_name in os.listdir(self.path_to_dest_folder):
            """dtype_dict = {col:str for col in itunes_usefull_cols if col in itunes_bool_columns}
            dtype_dict.update({col:float for col in itunes_usefull_cols if col in itunes_numeric_columns })
            dtype_dict.update({col:str for col in itunes_usefull_cols if not (col in itunes_numeric_columns
                                                                 or col in  itunes_bool_columns)})
            print(dtype_dict.keys())"""
            df_lib = pd.read_csv(
                self.path_to_dest_folder / csv_name
            )  # ,dtype = dtype_dict)


        else:
            # must first parse...
            logging.info("! Be Patient this will take a few seconds !")
            df_lib = self.convert_lib_to_csv()

        df_lib = df_lib.dropna(subset=["Artist"])
        df_lib.loc[:, "CloudLocation"] = (
            "Cloud/" + df_lib.loc[:, "Album Artist"] + "/" + df_lib.loc[:, "Album"]
        )
        df_lib.loc[:, "Location"] = df_lib.loc[:, "Location"].fillna(
            df_lib.loc[:, "CloudLocation"]
        )
        df_lib.loc[:, "Location"] = df_lib.loc[:, "Location"].apply(
            lambda x: unquote(x)
        )
        df_lib.loc[:, "Album Location"] = np.where(
            df_lib["Track Type"] == "File",
            df_lib["Location"],
            df_lib.loc[:, "CloudLocation"],
        )

        df_lib.loc[:, "Album Location"] = df_lib["Location"].apply(
            lambda y: Path(y).parent
        )

        return df_lib

    def get_all_playlists_from_itunes_library(self):
        """_summary_


        Args:
            path_to_lib_folder (_type_): _description_
            lib_name (_type_): _description_
        """
        if self.lib_lib != None:
            for playlist in self.lib_lib.playlists:

                PL_to_m3u8(self.path_to_playlists_folder, playlist)
