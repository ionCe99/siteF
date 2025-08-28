import re
from enum import Enum


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
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type}, {self.url!r})"


def extract_markdown_images(text: str):
    pattern = r'!\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)


def extract_markdown_links(text: str):
    pattern = r'(?<!!)\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)


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
            # Split once around this image
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
