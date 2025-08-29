from split_nodes import (
    TextNode, TextType,
    split_nodes_image, split_nodes_link, split_nodes_generic,
    extract_markdown_code, extract_markdown_bold, extract_markdown_italic
)

def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]

    # Apply splitters in order
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_generic(nodes, extract_markdown_code, TextType.CODE, lambda x: f"`{x}`")
    nodes = split_nodes_generic(nodes, extract_markdown_bold, TextType.BOLD, lambda x: f"**{x}**")
    nodes = split_nodes_generic(nodes, extract_markdown_italic, TextType.ITALIC, lambda x: f"_{x}_")

    return nodes
