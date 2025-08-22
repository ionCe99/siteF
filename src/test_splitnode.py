import unittest
from textnode import TextNode, TextType
from spilt_node import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_code_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_split(self):
        node = TextNode("Make this **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Make this ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_italic_split(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters(self):
        node = TextNode("Mix `code` and **bold** text", TextType.TEXT)
        # First split code
        nodes_after_code = split_nodes_delimiter([node], "`", TextType.CODE)
        # Then split bold
        nodes_after_bold = split_nodes_delimiter(nodes_after_code, "**", TextType.BOLD)
        expected = [
            TextNode("Mix ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(nodes_after_bold, expected)

    def test_non_text_nodes_untouched(self):
        nodes = [
            TextNode("Some text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("Some text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_edge_cases_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("", TextType.TEXT)])

if __name__ == "__main__":
    unittest.main()
