import os
from PIL import Image, ImageFile
import io
import music_tag
import pandas as pd
import shutil

import parameters as param
from pathlib import Path



ImageFile.MAXBLOCK = 2**20



def exctract_artwork(song_path, song_tag, is_any_cover_image, songs_wo_artwork):

    # @todo understand why 'artwork' can be missing
    try:
        song_tag["artwork"]
        artwork = True
    except:

        artwork = False

    if not artwork:
        songs_wo_artwork.append(song_path)
    elif song_tag["artwork"] is None:
        songs_wo_artwork.append(song_path)
    elif song_tag["artwork"].first is None:
        songs_wo_artwork.append(song_path)

    else:
        if not is_any_cover_image:
            art_data = song_tag["artwork"].first.data
            image = Image.open(io.BytesIO(art_data))
            try:
                image.save(
                    song_path.parents[0]/"non_prog_temp.jpg",
                    "JPEG",
                    quality=80,
                    optimize=True,
                    progressive=False,
                )
            except:
                image = image.convert("RGB")
                image.save(
                    song_path.parents[0]/"non_prog_temp.jpg",
                    "JPEG",
                    quality=80,
                    optimize=True,
                    progressive=False,
                )
            is_any_cover_image = True

    return is_any_cover_image, songs_wo_artwork

def extension_files_paths(dir_path,extensions):

    files = os.listdir(dir_path)

    files = [
        f
        for f in files
        if (True in [f.lower().endswith(form) for form in extensions])
        and not f.startswith("._")
    ]

    paths = [dir_path/file for file in files]

    return paths

def get_music_files_paths(music_dir_path):

    return extension_files_paths(music_dir_path,param.music_extentions)


def get_image_files_paths(music_dir_path):

    return extension_files_paths(music_dir_path,param.image_extentions)




class EditCoverArtwork():
    def __init__(
        self,
        df_lib,
        create_cover_jpg=True,
        create_album_jpg=True,
        complete_missing_cover_art=True,
        convert_to_non_prog=True,
        ):
        self.df_lib = df_lib
        self.create_cover_jpg = create_cover_jpg
        self.create_album_jpg = create_album_jpg
        self.complete_missing_cover_art = complete_missing_cover_art
        self.convert_to_non_prog = convert_to_non_prog

    def loop_over_albums_path(self):

        paths_to_albums = self.f_lib.loc[:,'Album Location'].unique()


        for path_to_album in paths_to_albums:

            music_files_paths = get_music_files_paths(path_to_album)

            image_files_paths = get_image_files_paths(path_to_album)

            album_title_from_path = path_to_album.split("/")[-1]

            is_any_cover_image = len(image_files_paths) > 0

            if image_files_paths:
                image_file_path = image_files_paths[0]

                with open(image_file_path, "rb") as image:

                    image = image.read()
                    image = Image.open(io.BytesIO(image))
                    try:
                        image.save(
                            music_files_paths/"non_prog_temp.jpg",
                            "JPEG",
                            quality=80,
                            optimize=True,
                            progressive=False,
                        )
                    except:
                        image = image.convert("RGB")
                        image.save(
                            music_files_paths/"non_prog_temp.jpg",
                            "JPEG",
                            quality=80,
                            optimize=True,
                            progressive=False,
                        )

            songs_wo_artwork_paths = []


            if self.convert_to_non_prog and is_any_cover_image:

                assign_non_prog_artwork_to_song_list(paths_to_albums, music_files_paths)

            if is_any_cover_image and songs_wo_artwork_paths and self.complete_missing_cover_art:

                assign_non_prog_artwork_to_song_list(paths_to_albums, songs_wo_artwork_paths)


            image_files_paths = get_image_files_paths(paths_to_albums)

            if path_to_album/"non_prog_temp.jpg" in image_files_paths:
                if self.create_cover_jpg:
                    shutil.copyfile(
                        path_to_album/"non_prog_temp.jpg",
                        path_to_album/"cover.jpg",
                    )
                if self.create_album_jpg:

                    shutil.copyfile(
                        path_to_album/"non_prog_temp.jpg",
                        path_to_album/f"{album_title_from_path}.jpg",
                    )

                os.remove(path_to_album/"non_prog_temp.jpg")

            elif songs_wo_artwork_paths:
                print("**** Album wo artwork: ", path_to_album)













def extension_files_paths(dir_path,extensions):

    files = os.listdir(dir_path)

    files = [
        f
        for f in files
        if (True in [f.lower().endswith(form) for form in extensions])
        and not f.startswith("._")
    ]





def assign_artwork_to_song(song_path, image_path):

    song_tag = music_tag.load_file(song_path)

    with open(image_path, "rb") as image:
        song_tag["artwork"] = image.read()

    song_tag.save()


def assign_non_prog_artwork_to_song_list(music_dir, music_files_paths):

    image_files_paths = get_image_files_paths(music_dir)

    if music_dir/"non_prog_temp.jpg" in image_files_paths:
        image_path = music_dir/"non_prog_temp.jpg"

        for song_path in music_files_paths:
            assign_artwork_to_song(song_path, image_path)




