from pydantic import BaseModel
from typing import Dict, Any
import pandas as pd
from datetime import datetime


class iTunesDataFrameSchema(BaseModel):
    """Schema definition for iTunes dataframe columns and their types."""

    # Numeric columns (int or float)
    numeric_columns: Dict[str, str] = {
        "Album Rating": "Int64",  # Nullable integer
        "Artwork Count": "Int64",
        "Bit Rate": "Int64",
        "Disc Count": "Int64",
        "Disc Number": "Int64",
        "Movement Count": "Int64",
        "Movement Number": "Int64",
        "Play Count": "Int64",
        "Play Date": "Int64",  # Unix timestamp
        "Rating": "Int64",
        "Sample Rate": "Int64",
        "Size": "Int64",
        "Skip Count": "Int64",
        "Track Count": "Int64",
        "Track ID": "Int64",
        "Track Number": "Int64",
        "Year": "Int64",
        "Total Time": "Int64",  # Duration in milliseconds
    }

    # Date columns
    date_columns: Dict[str, str] = {
        "Date Added": "datetime64[ns]",
        "Date Modified": "datetime64[ns]",
        "Play Date UTC": "datetime64[ns]",
        "Release Date": "datetime64[ns]",
        "Skip Date": "datetime64[ns]",
    }

    # Boolean columns
    bool_columns: Dict[str, str] = {
        "Album Loved": "boolean",
        "Apple Music": "boolean",
        "Clean": "boolean",
        "Compilation": "boolean",
        "Explicit": "boolean",
        "HD": "boolean",
        "Has Video": "boolean",
        "Loved": "boolean",
        "Matched": "boolean",
        "Music Video": "boolean",
        "Part Of Gapless Album": "boolean",
        "Playlist Only": "boolean",
    }

    @property
    def all_columns(self) -> Dict[str, str]:
        """Get all columns with their types."""
        return {**self.numeric_columns, **self.date_columns, **self.bool_columns}

    def get_dtype_dict(self) -> Dict[str, str]:
        """Get pandas dtype mapping for all columns."""
        return self.all_columns

    def validate_dataframe(self, df: pd.DataFrame) -> bool:
        """Validate that dataframe has correct column types."""
        expected_dtypes = self.get_dtype_dict()
        for col, expected_dtype in expected_dtypes.items():
            if col in df.columns:
                # For nullable dtypes, check the underlying type
                actual_dtype = str(df[col].dtype)
                if expected_dtype == "Int64" and actual_dtype not in [
                    "Int64",
                    "int64",
                    "float64",
                ]:
                    return False
                elif expected_dtype == "boolean" and actual_dtype not in [
                    "boolean",
                    "bool",
                ]:
                    return False
                elif (
                    expected_dtype == "datetime64[ns]"
                    and not pd.api.types.is_datetime64_any_dtype(df[col])
                ):
                    return False
        return True

    def apply_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the schema to a dataframe, converting types where possible."""
        df = df.copy()
        dtype_dict = self.get_dtype_dict()

        for col, dtype in dtype_dict.items():
            if col in df.columns:
                if dtype == "Int64":
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
                elif dtype == "boolean":
                    df[col] = df[col].astype("boolean")
                elif dtype == "datetime64[ns]":
                    df[col] = pd.to_datetime(df[col], errors="coerce")

        return df


# Default schema instance
itunes_schema = iTunesDataFrameSchema()
