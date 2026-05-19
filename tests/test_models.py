import pandas as pd

from audio_libs_tlk.models import itunes_schema


def test_itunes_schema_apply_schema_converts_types():
    df = pd.DataFrame(
        {
            "Total Time": ["123", "456"],
            "Album Rating": ["5", "7"],
            "Album Loved": [True, False],
            "Date Added": ["2025-01-01", "2025-02-01"],
        }
    )

    result = itunes_schema.apply_schema(df)

    assert str(result["Total Time"].dtype) == "Int64"
    assert str(result["Album Rating"].dtype) == "Int64"
    assert str(result["Album Loved"].dtype) == "boolean"
    assert pd.api.types.is_datetime64_any_dtype(result["Date Added"])


def test_itunes_schema_validate_dataframe():
    df = pd.DataFrame(
        {
            "Total Time": ["123", "456"],
            "Album Rating": ["5", "7"],
            "Album Loved": [True, False],
            "Date Added": ["2025-01-01", "2025-02-01"],
        }
    )

    result = itunes_schema.apply_schema(df)

    assert itunes_schema.validate_dataframe(result)
