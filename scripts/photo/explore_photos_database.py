import sqlite3
import pandas as pd
from pathlib import Path


def explore_photos_database(photos_library_path):
    """
    Extract information from the Photos Library database
    """
    # Path to the Photos Library database (using Photos.sqlite)
    database_path = Path(photos_library_path) / "database" / "Photos.sqlite"

    if not database_path.exists():
        print(f"Database not found at {database_path}")
        # Try to find alternative database locations
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
        # Connect to the database
        conn = sqlite3.connect(
            f"file:{database_path}?mode=ro", uri=True
        )  # Read-only mode
        print("Successfully connected to database")

        # Get list of tables
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print(f"\nFound {len(tables)} tables in the database:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table[0]}")

        # Look for tables that might contain video information
        video_related_tables = []
        for table in tables:
            table_name = table[0]
            if (
                "VIDEO" in table_name.upper()
                or "MEDIA" in table_name.upper()
                or "ASSET" in table_name.upper()
            ):
                video_related_tables.append(table_name)

        print(f"\nPotential video-related tables: {video_related_tables}")

        # Examine video tables
        for table in video_related_tables[
            :5
        ]:  # Limit to first 5 to avoid overwhelming output
            try:
                print(f"\n--- Exploring table: {table} ---")
                # Get column information
                cursor.execute(f"PRAGMA table_info({table});")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]

                print(f"Columns in {table} ({len(column_names)}):")
                # Print columns in chunks to avoid overwhelming output
                for i in range(0, len(column_names), 5):
                    chunk = column_names[i : i + 5]
                    print(f"  {', '.join(chunk)}")

                # Look for size and path related columns
                size_cols = [col[1] for col in columns if "SIZE" in col[1].upper()]
                path_cols = [
                    col[1]
                    for col in columns
                    if "PATH" in col[1].upper() or "FILE" in col[1].upper()
                ]

                if size_cols:
                    print(f"Potential size columns: {size_cols}")
                if path_cols:
                    print(f"Potential path columns: {path_cols}")

                # Get record count
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                print(f"Records in {table}: {count}")

                # If the table looks promising, query for large videos
                if size_cols and count > 0:
                    size_col = size_cols[0]  # Use the first size column
                    try:
                        print(f"\nFinding largest items in {table} using {size_col}:")
                        query = (
                            f"SELECT * FROM {table} ORDER BY {size_col} DESC LIMIT 5;"
                        )
                        cursor.execute(query)
                        rows = cursor.fetchall()

                        if rows:
                            col_names = [
                                description[0] for description in cursor.description
                            ]
                            print(f"Column names: {col_names}")
                            df = pd.DataFrame(rows, columns=col_names)
                            print("\nLargest items:")
                            print(df.head())
                    except sqlite3.Error as e:
                        print(f"Error querying by size: {e}")
            except sqlite3.Error as e:
                print(f"Error exploring table {table}: {e}")

        # Find database views that might contain useful information
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view';")
        views = cursor.fetchall()

        if views:
            print(f"\nFound {len(views)} views in the database:")
            for i, view in enumerate(views, 1):
                print(f"{i}. {view[0]}")

        # Try to find large videos directly with a general query
        try:
            print("\n--- Attempting to find large video assets directly ---")
            # Look for tables with potential video information and size data
            for table in video_related_tables:
                cursor.execute(f"PRAGMA table_info({table});")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]

                # Check if this table might contain video data with size info
                has_size = any("SIZE" in col.upper() for col in column_names)
                has_media_type = any("TYPE" in col.upper() for col in column_names)

                if has_size and has_media_type:
                    print(f"\nAnalyzing {table} for video files...")
                    # Try different column name combinations
                    size_cols = [col for col in column_names if "SIZE" in col.upper()]
                    type_cols = [col for col in column_names if "TYPE" in col.upper()]

                    for size_col in size_cols:
                        for type_col in type_cols:
                            try:
                                query = f"""
                                SELECT * FROM {table} 
                                WHERE {size_col} > 50000000  -- Files larger than 50MB
                                ORDER BY {size_col} DESC 
                                LIMIT 10;
                                """
                                cursor.execute(query)
                                rows = cursor.fetchall()

                                if rows:
                                    col_names = [
                                        description[0]
                                        for description in cursor.description
                                    ]
                                    print(f"\nFound {len(rows)} large files in {table}")
                                    print(f"Using size column: {size_col}")
                                    df = pd.DataFrame(rows, columns=col_names)
                                    print(
                                        df[
                                            [size_col, type_col]
                                            + [
                                                c
                                                for c in col_names
                                                if "PATH" in c.upper()
                                                or "NAME" in c.upper()
                                            ][:3]
                                        ]
                                    )
                            except sqlite3.Error:
                                pass  # Silently try next combination
        except Exception as e:
            print(f"Error in direct query: {e}")

        conn.close()
        print("\nDatabase connection closed")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    photos_library_path = "/Users/lzwjava/Pictures/Photos Library.photoslibrary/"
    explore_photos_database(photos_library_path)
