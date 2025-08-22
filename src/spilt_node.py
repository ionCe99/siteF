from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits TEXT nodes in old_nodes by the delimiter and returns a new list of nodes.
    Text outside delimiters stays as TextType.TEXT.
    Text inside delimiters becomes the specified text_type.
    """
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # Keep non-plain-text nodes as they are
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if part:
                # Alternate between TEXT and the target type
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
            else:
                # Handle consecutive delimiters producing empty strings
                new_nodes.append(TextNode('', TextType.TEXT))

    return new_nodes
