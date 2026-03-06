import os
import sqlite3
import pandas as pd
from pathlib import Path


def explore_photos_database(photos_library_path):
    """
    Extract information from the Photos Library database, including large video files and their creation times.
    """
    pd.set_option("display.max_columns", None)  # Show all columns
    pd.set_option("display.width", 200)  # Adjust width to prevent truncation
    pd.set_option("display.max_colwidth", None)  # Prevent text truncation

    database_path = Path(photos_library_path) / "database" / "Photos.sqlite"

    if not database_path.exists():
        print(f"Database not found at {database_path}")
        alternatives = list(Path(photos_library_path).glob("**/Photos.sqlite"))
        if alternatives:
            print(f"Found alternative database locations: {alternatives}")
            database_path = alternatives[0]
        else:
            print(
                "Could not find Photos database. It might be in a different location or format."
            )
            return

    print(f"Opening database: {database_path}")

    try:
        conn = sqlite3.connect(f"file:{database_path}?mode=ro", uri=True)
        print("Successfully connected to database")
        cursor = conn.cursor()

        # Find potential video-related tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        video_related_tables = [
            table
            for table in tables
            if "VIDEO" in table.upper() or "ASSET" in table.upper()
        ]

        print(f"\nPotential video-related tables: {video_related_tables}")

        if "ZADDITIONALASSETATTRIBUTES" in video_related_tables:
            table_name = "ZADDITIONALASSETATTRIBUTES"
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [col[1] for col in cursor.fetchall()]

            time_columns = [
                col
                for col in columns
                if "DATE" in col.upper() or "CREATION" in col.upper()
            ]

            print(f"\nColumns related to time: {time_columns}")

            query = f"""
            SELECT ZORIGINALFILESIZE, ZMEDIAMETADATATYPE, ZIMPORTEDBYDISPLAYNAME, 
                   ZORIGINALFILENAME, ZTIMEZONENAME, {", ".join(time_columns)} 
            FROM {table_name}
            ORDER BY ZORIGINALFILESIZE DESC
            LIMIT 10;
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            if rows:
                col_names = [description[0] for description in cursor.description]
                df = pd.DataFrame(rows, columns=col_names)
                print("\nLargest video files with creation time:")
                print(df)
            else:
                print("No large video files found.")

        conn.close()
        print("\nDatabase connection closed")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    photos_library_path = "/Users/lzwjava/Pictures/Photos Library.photoslibrary/"
    explore_photos_database(photos_library_path)
