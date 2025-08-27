import re


def extract_markdown_images(text: str):
    """
    Extracts markdown images of the form ![alt text](url)
    Returns a list of tuples (alt_text, url).
    """
    pattern = r'!\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)


def extract_markdown_links(text: str):
    """
    Extracts markdown links of the form [anchor text](url)
    Returns a list of tuples (anchor_text, url).
    """
    pattern = r'(?<!!)\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)