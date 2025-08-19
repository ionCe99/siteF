import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        # Original equality test
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        self.assertEqual(node, node2)

    def test_neq_text(self):
        # Different text should not be equal
        node1 = TextNode("Text 1", TextType.PLAIN)
        node2 = TextNode("Text 2", TextType.PLAIN)
        self.assertNotEqual(node1, node2)

    def test_neq_type(self):
        # Different text_type should not be equal
        node1 = TextNode("Same text", TextType.PLAIN)
        node2 = TextNode("Same text", TextType.LINK)
        self.assertNotEqual(node1, node2)

    def test_neq_url(self):
        # Different url should not be equal
        node1 = TextNode("Link text", TextType.LINK, url="https://example.com")
        node2 = TextNode("Link text", TextType.LINK, url="https://another.com")
        self.assertNotEqual(node1, node2)

    def test_default_url_none(self):
        # url defaults to None
        node = TextNode("Text without url", TextType.PLAIN)
        self.assertIsNone(node.url)

    def test_repr_format(self):
        # Ensure __repr__ returns the expected format
        node = TextNode("Hello", TextType.IMAGE, url="https://img.com")
        expected = "TextNode(Hello, image, https://img.com)"
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()