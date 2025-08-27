import unittest
from extract_text import extract_markdown_images,extract_markdown_links


class TestMarkdownExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches
        )

    def test_extract_multiple_images(self):
        text = "![one](https://a.com/1.png) and ![two](https://a.com/2.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("one", "https://a.com/1.png"), ("two", "https://a.com/2.png")],
            matches
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This has a [link](https://example.com)"
        )
        self.assertListEqual(
            [("link", "https://example.com")],
            matches
        )

    def test_extract_multiple_links(self):
        text = "[google](https://google.com) and [openai](https://openai.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("google", "https://google.com"), ("openai", "https://openai.com")],
            matches
        )

    def test_no_false_image_matches_in_links(self):
        text = "[not image](https://notimage.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_no_false_link_matches_in_images(self):
        text = "![pic](https://example.com/pic.jpg)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)


if __name__ == "__main__":
    unittest.main()