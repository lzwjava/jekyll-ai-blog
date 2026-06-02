import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.merge.merge_posts import (
    get_post_date,
    merge_post_contents,
    process_post_content,
)


class TestMergePosts(unittest.TestCase):
    def create_post_content(self, title, date, content):
        return f"""---
title: {title}
date: {date}
---
{content}"""

    def test_get_post_date(self):
        content = """---
title: Test Post
date: 2024-01-01
---
Test content"""
        self.assertEqual(get_post_date(content), "2024-01-01")

        # Test with no front matter
        self.assertIsNone(get_post_date("Just content"))

        # Test with no date
        content = """---
title: Test Post
---
Content"""
        self.assertIsNone(get_post_date(content))

    def test_merge_post_contents_basic(self):
        # Create test posts
        main_post = self.create_post_content("Main Post", "2024-03-01", "Main content")
        sub_post1 = self.create_post_content(
            "Sub Post 1", "2024-02-01", "Sub content 1"
        )
        sub_post2 = self.create_post_content(
            "Sub Post 2", "2024-01-01", "Sub content 2"
        )

        # Merge posts
        result = merge_post_contents([main_post, sub_post1, sub_post2])

        # Main post should be first (it has the latest date)
        self.assertTrue(result.startswith("---\ntitle: Main Post"))

        # Check if sub posts are properly formatted with titles and dates
        self.assertIn("## Sub Post 1, 2024-02-01", result)
        self.assertIn("## Sub Post 2, 2024-01-01", result)

    def test_merge_post_contents_validation(self):
        # Test with single post
        post = self.create_post_content("Single Post", "2024-01-01", "Content")
        result = merge_post_contents([post])
        self.assertIsNone(result)  # Should return None for single post

        # Test with too many posts
        posts = [
            self.create_post_content(f"Post {i}", "2024-01-01", "Content")
            for i in range(11)
        ]
        result = merge_post_contents(posts)
        self.assertIsNone(result)  # Should return None for too many posts

    def test_merge_post_contents_no_frontmatter(self):
        # Create post with front matter
        main_post = self.create_post_content("Main Post", "2024-03-01", "Main content")

        # Create content without front matter
        no_front_content = "Just content without front matter"

        result = merge_post_contents([main_post, no_front_content])

        # Check if content was properly merged
        self.assertIn("Just content without front matter", result)

    def test_process_post_content(self):
        # Test with complete front matter
        content = self.create_post_content("Test Post", "2024-01-01", "Test content")
        result = process_post_content(content)
        self.assertEqual(result["title"], "Test Post")
        self.assertEqual(result["date"], "2024-01-01")
        self.assertTrue(result["body"].strip() == "Test content")

        # Test without front matter
        content = "Just content"
        result = process_post_content(content)
        self.assertIsNone(result["title"])
        self.assertIsNone(result["date"])
        self.assertEqual(result["body"], "Just content")


if __name__ == "__main__":
    unittest.main()
