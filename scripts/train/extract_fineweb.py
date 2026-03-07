import pandas as pd
import glob

# Find all parquet files in the directory (000_00000 to 000_00010)
parquet_files = sorted(glob.glob("fineweb_test_dump/000_000*.parquet"))

if not parquet_files:
    print("Error: No parquet files found in fineweb_test_dump/000_000*.parquet")
    exit(1)

print(f"Found {len(parquet_files)} parquet files:")
for file in parquet_files:
    print(f"  - {file}")

# Extract text and save to file
output_file = "fineweb_test_dump/fineweb_extracted_all.txt"

print(f"Extracting text from all files to {output_file}...")

total_rows_processed = 0

try:
    with open(output_file, "w", encoding="utf-8") as f:
        for file_idx, parquet_file in enumerate(parquet_files):
            print(
                f"\n--- Processing file {file_idx + 1}/{len(parquet_files)}: {parquet_file} ---"
            )

            try:
                df = pd.read_parquet(parquet_file)
                print(f"Loaded {len(df)} rows")
                print(f"Columns: {list(df.columns)}")

                if file_idx == 0:
                    print("First few rows:")
                    print(df.head())

                # Extract text and save to file
                for i, row in df.iterrows():
                    # Try to find the text column (common names: text, content, article, etc.)
                    text_content = None

                    # Check common column names for text content
                    for col in ["text", "content", "article", "text_content", "body"]:
                        if col in df.columns:
                            text_content = str(row[col])
                            break

                    if text_content and text_content.strip():
                        f.write(
                            text_content.strip()
                            + "\n\n<|endoftext|><|endoftext|><|endoftext|>\n\n"
                        )

                    total_rows_processed += 1

                    # Progress reporting
                    if i % 10000 == 0:
                        print(
                            f"File {file_idx + 1} - Processed {i} rows, Total: {total_rows_processed}"
                        )

                print(f"Completed processing {parquet_file}")

            except Exception as e:
                print(f"Error loading parquet file {parquet_file}: {e}")
                continue

    print("\n\n🎉 EXTRACTION COMPLETE! 🎉")
    print(f"✅ Processed {len(parquet_files)} parquet files")
    print(f"✅ Total rows processed: {total_rows_processed:,}")
    print(f"✅ Output saved to: {output_file}")

except Exception as e:
    print(f"Error during extraction: {e}")
