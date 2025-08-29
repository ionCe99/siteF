import re
from enum import Enum

# --- Enum and Node Class ---
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            isinstance(other, TextNode) and
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type}, {self.url!r})"


# --- Extractor Functions ---
def extract_markdown_images(text: str):
    pattern = r'!\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def extract_markdown_links(text: str):
    pattern = r'(?<!!)\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def extract_markdown_code(text: str):
    pattern = r'`([^`]+)`'
    return re.findall(pattern, text)

def extract_markdown_bold(text: str):
    pattern = r'\*\*([^\*]+)\*\*'
    return re.findall(pattern, text)

def extract_markdown_italic(text: str):
    pattern = r'_([^_]+)_'
    return re.findall(pattern, text)


# --- Splitter Functions ---
def split_nodes_generic(old_nodes, extract_func, text_type, wrapper=None):
    """Generic splitter for code, bold, italic"""
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_func(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        text_to_process = node.text
        for match in matches:
            pattern_text = wrapper(match) if wrapper else match
            sections = text_to_process.split(pattern_text, 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(match, text_type))
            text_to_process = sections[1]
        if text_to_process:
            new_nodes.append(TextNode(text_to_process, TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        text_to_process = node.text
        for alt, url in images:
            sections = text_to_process.split(f"![{alt}]({url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text_to_process = sections[1]
        if text_to_process:
            new_nodes.append(TextNode(text_to_process, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        text_to_process = node.text
        for anchor, url in links:
            sections = text_to_process.split(f"[{anchor}]({url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            text_to_process = sections[1]
        if text_to_process:
            new_nodes.append(TextNode(text_to_process, TextType.TEXT))
    return new_nodes


