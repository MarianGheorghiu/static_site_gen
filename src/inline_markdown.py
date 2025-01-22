import re

from textnode import TextNode, TextType

# put all together
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '*', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

# used to split delimiters from markdown text     
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

# more usefull markdown functions
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_link(old_nodes):
    result = []
    for old_node in old_nodes:
        # Only process TEXT nodes
        if old_node.text_type == TextType.TEXT:
            result.extend(extract_img_or_link(old_node, 'link'))
        else:
            result.append(old_node)
    return result

def split_nodes_image(old_nodes):
    result = []
    for old_node in old_nodes:
        # Only process TEXT nodes
        if old_node.text_type == TextType.TEXT:
            result.extend(extract_img_or_link(old_node, 'img'))
        else:
            result.append(old_node)
    return result


def get_markdown_pattern(type, alt_text, url):
    if type == 'img':
        return f"![{alt_text}]({url})"
    return f"[{alt_text}]({url})"

def extract_text_by_type(type, text):
    if type == 'img':
        return extract_markdown_images(text)
    return extract_markdown_links(text)
    
def extract_img_or_link(old_node, type):
    new_nodes = []
    while True:
        extract_by_type = extract_text_by_type(type, old_node.text)
        if len(extract_by_type) == 0:
            if len(old_node.text) > 0:
                new_nodes.append(TextNode(old_node.text, TextType.TEXT))
            break
        param1, param2 = extract_by_type[0]
        markdown = get_markdown_pattern(type, param1, param2)
        if len(markdown) == 0:
            break
        sections = old_node.text.split(markdown, 1)
        if len(sections[0]) > 0:
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        if type == 'img':
            new_nodes.append(TextNode(param1, TextType.IMAGE, param2))
        else:
            new_nodes.append(TextNode(param1, TextType.LINK, param2))
        old_node.text = sections[1]
    return new_nodes
