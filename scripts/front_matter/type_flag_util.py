import os
import re
import frontmatter


def update_front_matter(file_path, post_type="post"):
    try:
        # Extract date from filename
        filename = os.path.basename(file_path)
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
        if not date_match:
            print(f"Could not extract date from filename: {filename}")
            return
        date_match.group(1)

        # Load the post using frontmatter library
        post = frontmatter.load(file_path)

        # Update the type field
        post.metadata["type"] = post_type

        # Write the updated post back to file
        frontmatter.dump(post, file_path)

        print(f"Updated front matter in {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
