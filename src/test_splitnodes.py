import unittest
from split_nodes import *

class TestSplitNodes(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "Check this [site](https://example.com) and [docs](https://docs.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check this ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://example.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("docs", TextType.LINK, "https://docs.com"),
            ],
            new_nodes,
        )

    def test_non_text_nodes_untouched(self):
        node = TextNode("bold text", TextType.BOLD)
        self.assertListEqual([node], split_nodes_image([node]))
        self.assertListEqual([node], split_nodes_link([node]))

    def test_no_matches_returns_original(self):
        node = TextNode("just plain text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))
        self.assertListEqual([node], split_nodes_link([node]))


if __name__ == "__main__":
    unittest.main()
