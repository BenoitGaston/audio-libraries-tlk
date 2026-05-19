def test_package_imports():
    import audio_libs_tlk
    from audio_libs_tlk.convertion_functions import (
        m3u8_to_csv,
        df_to_m3u8,
        convert_a_playlist,
    )
    from audio_libs_tlk.models import iTunesDataFrameSchema
    from audio_libs_tlk.folder_lib_scan import extract_tags

    assert audio_libs_tlk is not None
    assert callable(m3u8_to_csv)
    assert callable(df_to_m3u8)
    assert callable(convert_a_playlist)
    assert callable(extract_tags)
    assert isinstance(iTunesDataFrameSchema().get_dtype_dict(), dict)
