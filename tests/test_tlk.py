import pytest
import sys

sys.path.append("../src")

import src.audio-libs-tlk.lib_scan as ls


class TestTLK:

    def test_init(self):

        library_scan = ls.LibraryScan()

        assert isinstance(library_scan, ls.LibraryScan)
