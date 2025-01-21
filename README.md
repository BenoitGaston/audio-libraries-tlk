# audio-libraries-tlk

A set of Python tools to explore and modify data contained in a music library such as playlists or album cover artwork. 

## Links to

* [PyPi package](https://pypi.org/project/audio-libraries-tlk/)
* [Source code](https://github.com/BenoitGaston/audio-libraries-tlk)
*  A[streamlit app](https://github.com/BenoitGaston/Audio-Libraries-Scan-App) using this package for exploring and modifying data contained in a music library. 
* A [streamlit app](https://github.com/BenoitGaston/MiniDisc-Labels-App) using this package to create MiniDisc Labels. 

## Acknowledgments

This project is heavily relying on, on the one hand Scholnicks' [itunesLibrary](https://pypi.org/project/iTunesLibrary/) (itself a port of Drew Stephen's [Mac-iTunes-Library](https://github.com/dinomite/Mac-iTunes-Library)), on the other hand on KristoforMaynard's [music-tag](https://pypi.org/project/music-tag/). The template used to create MiniDisc inner labels is coming from [MiniDisc Wiki](https://www.minidisc.wiki/resources/labels)

## Usecases

This project originates from the following needs:

1. Transferring playlists from different audio devices.
2. Convert cover artwork of songs to non-prog images.
3. Explore inconsistencies in a music library (incomplete albums, songs placed in the wrong location, etc).
4. These would be possible for both an iTunes or Apple Music managed library and a library managed by hand in folders.


## How to install

Through pip
```
python3 -m pip install audio-libraries-tlk
```


## Warnings

**In general:**

* You are using this script at your own risks. Make sure you try the script on a duplicated small sample of your library to verify that it is achieving what you want.

**In particular:**

* Running the playlists components of the script should be safe as these don't imply modifying your music library but just extract some playlists and create new ones.

* Running the cover artwork options is much more risky as the script will potentially modify the cover artworks inside your music files. If your music files are not properly split by album (two songs of different albums are present in the same folder) then you the cover artworks of the two albums will be mixed (one will replace the other). In other word, the script assumes that songs in the same location belong to the same album.  In case of doubt, you can start by running the script with all the cover artwork options set as `False` (the default case) and with the option `Create special playlists` option as True. This will produce a csv file showing all the locations containing songs of multiple albums.

* Again try the script on a small duplicated sample of your music files and check if the result pleases you.

## Be patient

Depending on the option you choose the script can take a long time to run: up to ~1 hour for 1 30k songs library on a mac mini M2.

**To save time in the case you need to run the script twice** and to avoid the full scan of the music files or of the .xml file twice, a .pickle and a .csv file are created by the first scan of the library. These will be reused in the the second call to significantly reduce the time of the second call. 

However, if your music files or .xml have changed between the first and the second call, you need to remove the existing .pickles and .csv are these wont reflect anymore the state of your music library.

## Outputs

* The `.m3u8`, `.csv` and `.pickle`files created by the script will be located inside the `PATH_TO_LIBRARY_DATA`. 
* Image files extracted from your music metadata will be located in the album folders.

## How to run

* To run the script from an iTunes or Apple Music, first go to `setting/Library/Export Library`. Save the `.xml` file in a folder and copy this path (for instance `/Users/user_name/Music/` where you have placed the file `My_Library.xml`).
* To run the script from a music library that is simply organised in folders (for instance `Artist/Album`). Simply copy the path pointing to our music directory (for instance `/Users/user_name/Music/Music/Media/Music`).

Then, for instance, to extract all the playlists contained in your music library, convert them into a format readable by a new audio device, and create a `cover.jpg` file for inside each album folder, run the command:

```
python3 -m audio-libs-tlk --path_to_library_data='/Users/user_name/Music/' --orginal_path_written_in_playlists='/Users/user_name/Music/' --updated_path_written_in_playlists='/home/Music/' --create_cover_jpg=True
```


#### To save time on the second run

To save time in the case you need to run the script twice and to avoide the full scan of the music files or of the `.xml`file twice, a `.pickle` and a `.csv` file are created by the first scan of the library. These will be reused in the the second call to significantly reduce the time of the second call. 

However, if your music files or `.xml` have changed between the fiorst and the second call, you need to remove the existing `.pickles` and `.csv` are these wont reflect anymore the state of your music library.

## Detailed options

```
options:
  -h, --help            show this help message and exit
  --path_to_library_data PATH_TO_LIBRARY_DATA
                        Path containing to a folder containing an iTunes library .xml file or all
                        a music library organized album folders.
  --orginal_path_written_in_playlists ORGINAL_PATH_WRITTEN_IN_PLAYLISTS default=None
                        Part of the path to be replaced in the original playlists (for instance
                        '/Users/UserName/Music/Music/Media/Music'). Open an m3u8 playlist with a
                        text editor to know what to use.
  --updated_path_written_in_playlists UPDATED_PATH_WRITTEN_IN_PLAYLISTS default=None
                        Part to be used in the new music location (for instance
                        '/home/sony/walkman/Music'). Open an m3u8 playlist with a text editor to
                        know what to use.
  --create_cover_jpg CREATE_COVER_JPG default=False
                        If True an image file called 'cover.jpg' will be created inside each
                        location containing some music files. Only 1 file will be created per
                        location. Even if two songs have distinct cover art
  --create_album_title_jpg CREATE_ALBUM_TITLE_JPG default=False
                        If True an image file called 'title of the album.jpg' will be created
                        inside each location containing some music files. Only 1 file will be
                        created per location. Even if two songs have distinct cover art
  --complete_missing_cover_art COMPLETE_MISSING_COVER_ART default=False
                        Use the cover art of a song (any arbitrary one) contained in the same
                        location to fil all the missing cover arts
  --convert_to_non_prog CONVERT_TO_NON_PROG default=False
                        Convert the cover arts to non-prog images.
  --create_special_playlists CREATE_SPECIAL_PLAYLISTS default=False
                        Create some playlists and csv file to underline some aspects of a music
                        library.
  "--create_minidisc_labels default=False
                        From an .m3u8 file, create some MiniDisc labels using the cover artwork 
                        present in the audio library.
```
