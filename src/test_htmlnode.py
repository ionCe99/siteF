import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single(self):
        node = HTMLNode(tag="a", props={"href": "https://google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(tag="a", props={"href": "https://google.com", "target": "_blank"})
        # The order of attributes in the string may vary, so check for both
        result = node.props_to_html()
        self.assertTrue(
            result == ' href="https://google.com" target="_blank"' or
            result == ' target="_blank" href="https://google.com"'
        )

    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello", children=[], props={"class": "text"})
        expected = "HTMLNode(tag='p', value='Hello', children=[], props={'class': 'text'})"
        self.assertEqual(repr(node), expected)

    def test_props_empty(self):
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()
