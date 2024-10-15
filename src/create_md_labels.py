import os
import pandas as pd
from convertion_functions import m3u8_to_csv
from folder_lib_scan import loop_over_a_songs_df
from folder_lib_scan import format_df_to_iTunes_csv_format
from processing_lib import LibraryProcessing
from edit_cover_artwork import get_image_files_paths
from edit_cover_artwork import EditCoverArtwork
from pathlib import Path
import shutil
import base64
import numpy as np
import parameters as param
from edit_cover_artwork import get_image_files_paths

import re

import logging


def built_dict_of_styles(theme):

    background_color = theme["background_color"]
    main_text_color = theme["main_text_color"]
    triangle_color = theme["triangle_color"]
    insert_color = theme["insert_color"]
    md_logo_background_color = theme["md_logo_background_color"]
    md_logo_text_color = theme["md_logo_text_color"]

    base_0 = ";fill-rule:nonzero;stroke:none;stroke-width:"
    base_1 = f"fill:#{background_color};fill-opacity:1{base_0}"

    base_2 = "font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:"
    base_3 = (
        ";line-height:1.25;font-family:sans-serif;-inkscape-font-specification:'sans-serif, Bold';"
        + "font-variant-ligatures:normal;font-variant-caps:normal;font-variant-numeric:normal;font-feature-settings:normal"
    )
    base_4 = f";text-align:start;letter-spacing:0px;word-spacing:0px;writing-mode:lr-tb;text-anchor:start;fill:#{main_text_color};fill-opacity:1;stroke:none;stroke-width:"
    base_5 = f"fill:#{md_logo_background_color};fill-rule:evenodd;stroke:none"

    i_style_1 = f"{base_1}0.342622"
    i_style_2 = (
        f"{base_2}2.11667px{base_3}0.264583;fill:#{main_text_color};fill-opacity:1"
    )
    i_style_3 = f"{base_1}0.353446"
    i_style_4 = f"fill:#{md_logo_background_color};fill-rule:nonzero;stroke:none"

    i_style_6 = f"fill:#{md_logo_text_color};fill-rule:evenodd;stroke:none"
    i_style_5 = i_style_6
    i_style_7 = f"fill:#{triangle_color};fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.366875"
    i_style_8 = (
        f"{base_2}2.11667px{base_3};text-align:center;letter-spacing:0px;word-spacing:0px;writing-mode:lr-tb;text-anchor:middle;"
        + f"fill:#{main_text_color};fill-opacity:1;stroke:none;stroke-width:0.264583"
    )
    i_style_9 = (
        f"{base_2}2.11667px;font-family:sans-serif;-inkscape-font-specification:'sans-serif, "
        + "Bold';font-variant-ligatures:normal;font-variant-caps:normal;font-variant-numeric:normal;"
        + "font-feature-settings:normal;text-align:center;writing-mode:lr-tb;text-anchor:middle;fill:"
        + f"#{insert_color};fill-opacity:1;stroke-width:0.264583"
    )

    ds_style_1 = (
        f"{base_2}2.11667px;line-height:1.25;font-family:sans-serif;-inkscape-font-specification:'sans-serif, Bold';font-variant-ligatures:normal;"
        + f"font-variant-caps:normal;font-variant-numeric:normal;font-feature-settings:normal0 0.264583;fill:#{main_text_color};fill-opacity:1"
    )

    ds_style_2 = f"fill:#{background_color};fill-opacity:1;stroke-width:0.151625"

    od_style_1 = f"{base_2}3.17502px{base_3}{base_4}0.396873"
    od_style_2 = f"{base_1}0.911969"
    od_style_3 = i_style_4
    od_style_4 = i_style_6
    od_style_5 = f"{base_1}0.533961"
    od_style_6 = i_style_6

    o_style_1 = od_style_5
    o_style_2 = i_style_4
    o_style_3 = i_style_6
    o_style_4 = i_style_6
    o_style_5 = f"{base_2}2.75167px{base_3}{base_4}0.343958"

    id_style_1 = f"{base_2}2.11879px{base_3}{base_4}0.264848"
    id_style_2 = f"{base_1}0.451224"
    id_style_3 = f"{base_5};stroke-width:0.0182128"
    id_style_4 = f"fill:#{triangle_color};fill-opacity:1{base_0}0.988099"
    id_style_5 = f"fill:#{md_logo_text_color}{base_0}:0.0182128"
    id_style_6 = f"{i_style_6};stroke-width:0.0182128"

    return {
        "i_styles": [
            i_style_1,
            i_style_2,
            i_style_3,
            i_style_4,
            i_style_5,
            i_style_6,
            i_style_7,
            i_style_8,
            i_style_9,
        ],
        "ds_styles": [ds_style_1, ds_style_2],
        "od_styles": [
            od_style_1,
            od_style_2,
            od_style_3,
            od_style_4,
            od_style_5,
            od_style_6,
        ],
        "o_styles": [o_style_1, o_style_2, o_style_3, o_style_4, o_style_5],
        "id_styles": [
            id_style_1,
            id_style_2,
            id_style_3,
            id_style_4,
            id_style_5,
            id_style_6,
        ],
    }


def get_information_dict_from_file_name(full_file_name):
    image_dict = {}
    file_name = full_file_name.replace(".jpg", "").replace(".png", "")

    if len(file_name.split("-")) == 1:
        image_dict["Album"] = file_name.split("-")[0].strip()
        image_dict["Album Artist"] = None
        image_dict["Album Year"] = None

    elif len(file_name.split("-")) == 2:

        image_dict["Album"] = file_name.split("-")[1].strip()
        image_dict["Album Artist"] = file_name.split("-")[0].strip()
        image_dict["Album Year"] = None
    elif len(file_name.split("-")) == 3:

        image_dict["Album"] = file_name.split("-")[1].strip()
        image_dict["Album Artist"] = file_name.split("-")[0].strip()
        image_dict["Album Year"] = file_name.split("-")[2].strip()
    else:
        print(f'Too many "-" in file {file_name}')
        pass

    return image_dict


def update_temp_svgs(substitution_dict, path_to_temp_files_folder):

    open(path_to_temp_files_folder / f"temp-0.svg", "w").write(
        open(path_to_temp_files_folder / f"temp-1.svg").read()
    )
    i = 1

    for key in substitution_dict.keys():

        open(path_to_temp_files_folder / f"temp-{i%2}.svg", "w").write(
            open(path_to_temp_files_folder / f"temp-{(i+1)%2}.svg")
            .read()
            .replace(key, substitution_dict[key])
        )
        i += 1
    open(path_to_temp_files_folder / f"temp-{(i)%2}.svg", "w").write(
        open(path_to_temp_files_folder / f"temp-{(i+1)%2}.svg").read()
    )


def is_valid_hexa_code(string):
    hexa_code = re.compile(r"^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$")
    return bool(re.match(hexa_code, string))


def get_theme(row):

    theme = {}

    for theme_item in ["background_color", "md_logo_background_color"]:
        if is_valid_hexa_code(str(row["background_color"])):
            theme[theme_item] = row["background_color"]
        else:
            theme[theme_item] = param.color_map.get(
                row["background_color"], param.background_default
            )

    for theme_item in [
        "main_text_color",
        "md_logo_text_color",
        "triangle_color",
        "insert_color",
    ]:
        if is_valid_hexa_code(str(row["text_color"])):
            theme[theme_item] = row["text_color"]
        else:
            theme[theme_item] = param.color_map.get(
                row["text_color"], param.text_default
            )

    return theme


def create_substitucion_dict(one_page_md_labels_df, image_dict):

    one_page_md_labels_df.reset_index(inplace=True)

    substitution_dict = {}

    for md_id, row in one_page_md_labels_df.iterrows():

        theme = get_theme(row)
        dict_of_styles = built_dict_of_styles(theme)

        substitution_dict = (
            substitution_dict
            | {  # f">id_artist_{md_id}-1<" :  f">{row['Album Artist']}<", #line 1
                f">id_artist_{md_id}<": f"> * {row['Display Album']}<",  # line 2
                # f">id_artist_{md_id}-2<" :  f"> * {row['album_2']}<", #line 3
                f">i_album_{md_id}<": f">{row['Display Album']}<",
                f">o_artist_{md_id}<": f">{row['Display Album Artist']}<",
                # f">od_artist_{md_id}-1<" :  f">{row['Album Artist']}<", #Line 1
                # f">od_album_{md_id}-1<" :  f"> * {row['Album']}<", #line 2
                # f">od_artist_{md_id}-2<" :  f"> * {row['album_2']}<", #Line 3
                # f">od_album_{md_id}-2<" :  f"> <", #Line 4
                # f">o_year_{md_id}" :  f"{row['Year']}",
            }
        )
        if str(row["Album Year"]) == "nan":
            substitution_dict = substitution_dict | {
                f">i_year_{md_id}<": f"> <",
                f">o_album_{md_id}-year_{md_id}<": f">{row['Display Album']}<",
            }
        else:
            substitution_dict = substitution_dict | {
                f">i_year_{md_id}<": f">{int(row['Album Year'])}<",
                f">o_album_{md_id}-year_{md_id}<": f">{row['Display Album']} - {int(row['Album Year'])}<",
            }

        if str(row["Display Album Artist"]) == "nan":
            substitution_dict = substitution_dict | {f">i_artist_{md_id}<": f"> <"}

        else:
            substitution_dict = substitution_dict | {
                f">i_artist_{md_id}<": f">{row['Display Album Artist']}<"
            }

        substitution_dict = substitution_dict | {
            f"i_style_{md_id}-{style_id}": dict_of_styles["i_styles"][style_id - 1]
            for style_id in range(1, 10)
        }
        substitution_dict = substitution_dict | {
            f"id_style_{style_id}-{md_id}": dict_of_styles["id_styles"][style_id - 1]
            for style_id in range(1, 7)
        }
        substitution_dict = substitution_dict | {
            f"o_style_{md_id}-{style_id}": dict_of_styles["o_styles"][style_id - 1]
            for style_id in range(1, 6)
        }
        substitution_dict = substitution_dict | {
            f"od_style_{style_id}-{md_id}": dict_of_styles["od_styles"][style_id - 1]
            for style_id in range(1, 7)
        }
        substitution_dict = substitution_dict | {
            f"sd_style_{md_id}-{style_id}": dict_of_styles["ds_styles"][style_id - 1]
            for style_id in range(1, 3)
        }
        substitution_dict = substitution_dict | {
            f"s_style_{md_id}-{style_id}": dict_of_styles["ds_styles"][style_id - 1]
            for style_id in range(1, 3)
        }

        # if str(row['album_2']) == 'nan':
        if f"{row['Album Artist']}-{row['Album']}" in image_dict.keys():
            substitution_dict[f"image_number_{md_id}-"] = image_dict[
                f"{row['Album Artist']}-{row['Album']}"
            ]

        # if f"{row['Album Artist']}-{row['Album']}" in image_dict.keys():
        #    substitution_dict[f"image_number_{md_id}-1"] =  image_dict[f"{row['Album Artist']}-{row['Album']}"]

        # if f"{row['artist_2']}-{row['album_2']}" in image_dict.keys():
        #    substitution_dict[f"image_number_{md_id}-2"] =  image_dict[f"{row['artist_2']}-{row['album_2']}"]

        # substitution_dict[f">sd_artist_album_{md_id}<"] = f">{row['Album Artist']} - {row['Album']} / {row['album_2']}<"
        substitution_dict[f">sd_artist_album_{md_id}<"] = (
            f">{row['Display Album Artist']} - {row['Display Album']}<"
        )

    return substitution_dict


class MiniDiscCovers:
    def __init__(
        self,
        path_to_music_folder=None,
    ):
        self.path_to_music_folder = Path(path_to_music_folder)

        if "MiniDisc-Labels" not in os.listdir(self.path_to_music_folder):
            os.mkdir(Path(self.path_to_music_folder) / "MiniDisc-Labels")
        self.path_to_dest_folder = (self.path_to_music_folder) / "MiniDisc-Labels"

    def create_mini_disc_df(self):

        mini_disc_playlists = [
            file
            for file in os.listdir(self.path_to_music_folder)
            if "minidisc"
            in file.lower().replace(" ", "").replace("_", "").replace("-", "")
            and file.endswith(".m3u8")
        ]

        if len(mini_disc_playlists) == 0:
            print(f"No minidisc playlist in location {self.path_to_music_folder}.")
            print(
                f'To run this script, you need a m3u8 playlist with "minidic" in the filename.'
            )
            return pd.DataFrame([]), pd.DataFrame([])

        mini_disc_playlist = mini_disc_playlists[0]

        if f"{mini_disc_playlist.replace('.m3u8','')}_songs.csv" in os.listdir(
            self.path_to_music_folder
        ):
            mini_disc_songs_df = pd.read_csv(
                self.path_to_music_folder
                / f"{mini_disc_playlist.replace('.m3u8','')}_songs.csv"
            )
        else:

            mini_disc_songs_df = m3u8_to_csv(
                path_to_playlist=self.path_to_music_folder,
                playlist_name=mini_disc_playlist,
            )
            os.remove(
                self.path_to_music_folder / mini_disc_playlist.replace("m3u8", "csv")
            )

            mini_disc_songs_df = loop_over_a_songs_df(mini_disc_songs_df)
            mini_disc_songs_df = format_df_to_iTunes_csv_format(mini_disc_songs_df)
            mini_disc_songs_df.to_csv(
                self.path_to_music_folder
                / f"{mini_disc_playlist.replace('.m3u8','')}_songs.csv"
            )

        if f"{mini_disc_playlist.replace('.m3u8','')}_albums.csv" in os.listdir(
            self.path_to_music_folder
        ):
            mini_disc_album_df = pd.read_csv(
                self.path_to_music_folder
                / f"{mini_disc_playlist.replace('.m3u8','')}_albums.csv"
            )
        else:

            library_processing = LibraryProcessing(
                df_lib=mini_disc_songs_df,
                path_to_playlist_folder=self.path_to_dest_folder,
            )

            mini_disc_album_df = library_processing.get_grouped_df(
                disc_or_album="Album", path_to_destination=self.path_to_dest_folder
            )
            os.remove(self.path_to_dest_folder / "Album.csv")
            mini_disc_album_df.loc[:, ["Album", "Album Artist"]] = (
                mini_disc_album_df.loc[:, ["Album", "Album Artist"]]
                .replace("/", "-", regex=True)
                .replace(":", "-", regex=True)
            )

            mini_disc_album_df.loc[:, "Display Album"] = mini_disc_album_df.loc[
                :, "Album"
            ]
            mini_disc_album_df.loc[:, "Display Album Artist"] = mini_disc_album_df.loc[
                :, "Album Artist"
            ]
            mini_disc_album_df.loc[:, "text_color"] = None
            mini_disc_album_df.loc[:, "background_color"] = None
            mini_disc_album_df.loc[:, "text_color"] = None

            odered_columns = [
                "Album",
                "Album Artist",
                "Display Album",
                "Display Album Artist",
                "background_color",
                "text_color",
                "Album Year",
                "Album Total Time",
                "Album Genre",
                "Num Tracks",
                "Album Has Multiple Locations",
                "Album Has Multiple Genre",
                "Album Location",
            ]

            mini_disc_album_df = mini_disc_album_df[odered_columns]
            mini_disc_album_df.to_csv(
                self.path_to_music_folder
                / f"{mini_disc_playlist.replace('.m3u8','')}_albums.csv"
            )

        return mini_disc_album_df, mini_disc_songs_df

    def copy_covers_to_dest_path(self):

        for _, row in self.mini_disc_album_df.iterrows():

            album_title = row["Album"]

            album_location = row["Album Location"]
            album_artist = row["Album Artist"]

            images_files = get_image_files_paths(Path(album_location))

            cover_files = [
                f
                for f in images_files
                if (
                    str(f.name).startswith("cover.")
                    or str(f.name).startswith(f"{album_title}.")
                )
            ]

            if len(cover_files) == 0:

                edit_cover_artwork = EditCoverArtwork(
                    self.mini_disc_songs_df[
                        self.mini_disc_songs_df.Album == album_title
                    ],
                    create_cover_jpg=True,
                )

                edit_cover_artwork.loop_over_albums_path()

            images_files = get_image_files_paths(Path(album_location))

            cover_files = [
                f
                for f in images_files
                if (
                    str(f.name).startswith("cover.")
                    or str(f.name).startswith(f"{album_title}.")
                )
            ]

            if len(cover_files) == 0:
                logging.warning(f"Cover artwork is missing for album {album_title}")
            else:
                cover_file = cover_files[0]

                shutil.copy2(
                    cover_file,
                    self.path_to_dest_folder
                    / f'{album_artist}-{album_title}.{cover_file.name.split(".")[-1]}',
                )

    def loop_over_images_files(
        self,
    ):
        list_of_images_dict = []
        images_files = get_image_files_paths(self.path_to_dest_folder)
        for full_file_name in images_files:

            try:
                image_dict = get_information_dict_from_file_name(full_file_name)

                list_of_images_dict.append(pd.DataFrame(image_dict))
            except:
                logging.warning(
                    f" File {full_file_name} is not respecting the format Album - Artist.jpg"
                )

        md_labels_df = pd.concat(list_of_images_dict)

        return md_labels_df

    def get_converted_images_dict(self):

        image_dict = {}

        for _, row in self.mini_disc_album_df.iterrows():
            album = row["Album"]
            artist = row["Album Artist"]

            images_files = get_image_files_paths(self.path_to_dest_folder)

            cover_file_1 = [
                f for f in images_files if (f.name.startswith(f"{artist}-{album}."))
            ]

            if len(cover_file_1) == 0:
                logging.warning(
                    f" ! Warning no cover file found for {artist}-{album} !"
                )
                break

            cover_file_1 = cover_file_1[0]

            with open(cover_file_1, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("ascii")
                image_dict[f"{artist}-{album}"] = encoded_string

        return image_dict

    def build_album_labels(self, double=False):

        # Strings to replace Inner (16)
        list_num_pages = [16, 32, 8]
        # list_num_pages = []#,32,8]
        template_names = [
            f"MD-Labels-Inner-Template.svg",
            f"MD-Labels-Side-Template.svg",
            f"MD-Labels-Outer-Template.svg",
        ]
        # template_names = []
        if double:
            list_num_pages = [16, 32, 8]
            template_names = [
                f"MD-Labels-Inner-Double-Template.svg",
                f"MD-Labels-Side-Double-Template.svg",
                f"MD-Labels-Outer-Double-Template.svg",
            ]
            # template_names = [f'MD-Labels-Inner-Double-Template.svg']

        for i in range(len(list_num_pages)):

            number_of_labels_per_page = list_num_pages[i] + 1

            template_name = template_names[i]
            path_to_templates = Path(__file__).parent.resolve() / "MiniDisc-Templates"

            total_number_of_pages = int(
                len(self.mini_disc_album_df) / number_of_labels_per_page
            )

            for page_id in range(0, total_number_of_pages + 1):

                one_page_md_labels_df = self.mini_disc_album_df.iloc[
                    (page_id * number_of_labels_per_page) : np.min(
                        [
                            (page_id + 1) * number_of_labels_per_page,
                            len(self.mini_disc_album_df),
                        ]
                    )
                ]

                one_page_md_labels_df = pd.concat(
                    [
                        one_page_md_labels_df,
                        pd.DataFrame(
                            {
                                col: ["0"]
                                * (
                                    number_of_labels_per_page
                                    - len(one_page_md_labels_df)
                                )
                                for col in one_page_md_labels_df.columns
                            }
                        ),
                    ]
                )

                substitution_dict = create_substitucion_dict(
                    one_page_md_labels_df, self.image_dict
                )

                open(self.path_to_dest_folder / "temp-1.svg", "w").write(
                    open(path_to_templates / template_name).read()
                )
                open(self.path_to_dest_folder / "temp-0.svg", "w").write(
                    open(path_to_templates / template_name).read()
                )

                update_temp_svgs(
                    substitution_dict,
                    path_to_temp_files_folder=self.path_to_dest_folder,
                )

                open(
                    self.path_to_dest_folder
                    / f"{template_name.replace('.svg','').replace('-Template','')}-page-{page_id+1}.svg",
                    "w",
                ).write(open(self.path_to_dest_folder / "temp-1.svg").read())

                os.remove(self.path_to_dest_folder / "temp-1.svg")
                os.remove(self.path_to_dest_folder / "temp-0.svg")

        return None

    def build_md_labels(self):
        self.mini_disc_album_df, self.mini_disc_songs_df = self.create_mini_disc_df()

        self.copy_covers_to_dest_path()

        if len(self.mini_disc_album_df) == 0:
            print(f" ! Warning no cover file found for mini_disc_album_df is empty !")
            logging.warning(
                f" ! Warning no cover file found for mini_disc_album_df is empty !"
            )
            self.mini_disc_album_df = self.loop_over_images_files()

        self.image_dict = self.get_converted_images_dict()

        self.build_album_labels()
