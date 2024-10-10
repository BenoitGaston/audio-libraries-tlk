music_extentions = [
    ".aac",
    ".aiff",
    ".dsf",
    ".flac",
    ".m4a",
    ".mp3",
    ".ogg",
    ".opus",
    ".wav",
    ".wv",
]

image_extentions = [".jpg", ".jpeg", ".png"]

playlist_extensions = [".m3u8"]

tag_keys = [
    "Album",
    "Album Artist",
    "Artist",
    "Artwork",
    "Comment",
    "Compilation",
    "Composer",
    "Disc Number",
    "Genre",
    "Lyrics",
    "Total Discs",
    "Total Tracks",
    "Track Number",
    "Track Title",
    "Year",
    "Isrc",
    "#Bit Rate",
    "#Codec",
    "#Length",
    "#Channels",
    "#Bits Per Sample",
    "#Sample Rate",
]

important_cols = [
    "Name",
    "Album",
    "Album Artist",
    "Artist",
    "Artwork Count",
    "Comment",
    "Compilation",
    "Composer",
    "Disc Number",
    "Genre",
    "Disc Count",
    "Track Count",
    "Track Number",
    "Year",
    "Persistent ID",
    "Bit Rate",
    "Kind",
    "Total Time",
    "Sample Rate",
]


tags_to_itunes_cols_dict = {
    "Total Discs": "Disc Count",
    "Total Tracks": "Track Count",
    "Track Title": "Name",
    "#Length": "Total Time",
    "#Codec": "Kind",
}


itunes_cols = [
    "Track ID",
    "Name",
    "Artist",
    "Album",
    "Genre",
    "Kind",
    "Size",
    "Total Time",
    "Disc Number",
    "Disc Count",
    "Year",
    "Date Modified",
    "Date Added",
    "Bit Rate",
    "Sample Rate",
    "Artwork Count",
    "Persistent ID",
    "Track Type",
    "Location",
    "File Folder Count",
    "Library Folder Count",
    "Album Artist",
    "Album Rating",
    "Compilation",
    "Composer",
    "Normalization",
    "Play Count",
    "Play Date",
    "Play Date UTC",
    "Podcast",
    "Rating",
    "Sort Album",
    "Sort Album Artist",
    "Sort Artist",
    "Sort Composer",
    "Sort Name",
    "Track Count",
    "Track Number",
    "Album Rating Computed",
    "BPM",
    "Clean",
    "Comments",
    "Content Rating",
    "Episode",
    "Episode Order",
    "Explicit",
    "Grouping",
    "HD",
    "Has Video",
    "Movement Count",
    "Movement Name",
    "Movement Number",
    "Part Of Gapless Album",
    "Purchased",
    "Release Date",
    "Season",
    "Series",
    "Skip Count",
    "Skip Date",
    "TV Show",
    "Unplayed",
    "Video Height",
    "Video Width",
    "Work",
]


itunes_numeric_columns = [
            "Album Rating",
            "Artwork Count",
            "Bit Rate",
            "Disc Count",
            "Disc Number",
            "Movement Count",
            "Movement Number",
            "Play Count",
            "Play Date",
            "Rating",
            "Sample Rate",
            "Size",
            "Skip Count",
            "Track Count",
            "Track ID",
            "Track Number",
            "Year",
            "Total Time",
        ]




itunes_date_columns = [
            "Date Added",
            "Date Modified",
            "Play Date UTC",
            "Release Date",
            "Skip Date",
        ]


itunes_bool_columns = [
            "Album Loved",
            "Apple Music",
            "Clean",
            "Compilation",
            "Explicit",
            "HD",
            "Has Video",
            "Loved",
            "Matched",
            "Music Video",
            "Part Of Gapless Album",
            "Playlist Only",
        ]


itunes_usefull_cols = [
            "Track ID",
            "Name",
            "Artist",
            "Album Artist",
            "Composer",
            "Album",
            "Genre",
            "Kind",
            "Size",
            "Total Time",
            "Disc Number",
            "Disc Count",
            "Track Number",
            "Track Count",
            "Year",
            "Date Modified",
            "Date Added",
            "Bit Rate",
            "Sample Rate",
            "Normalization",
            "Compilation",
            "Album Rating",
            "Artwork Count",
            "File Type",
            "Play Count",
            "Play Date",
            "Play Date UTC",
            "Rating",
            "Sort Album",
            "Sort Album Artist",
            "Sort Composer",
            "Sort Artist",
            "Sort Name",
            "Persistent ID",
            "Track Type",
            "Location",
            "File Folder Count",
            "Library Folder Count",
            "Podcast",
        ]