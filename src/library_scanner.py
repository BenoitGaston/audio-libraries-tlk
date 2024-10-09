import os
import xml.etree.ElementTree as ET  ## XML parsing

from lib_scan import LibraryScan
from edit_cover_artwork import EditCoverArtwork
from processing_lib import LibraryProcessing
import numpy as np

from pathlib import Path


import requests

def library_scanner(url, dest_path=None):
    res = requests.get(url)
    res.raise_for_status()
    if dest_path is None: # grab the url basename
        dest_path = url.split("/")[-1]
    with open(dest_path, 'wb') as fhand:
        return fhand.write(res.content)