import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )
            
    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    
    def test_parent_node_with_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected_html)
        
    def test_nested_parent_nodes(self):
            node = ParentNode(
                "div",
                [
                    ParentNode(
                        "p",
                        [
                            LeafNode("b", "Bold text"),
                            LeafNode(None, "Normal text"),
                        ],
                    ),
                    LeafNode("i", "italic text"),
                ],
            )
            expected_html = (
                "<div><p><b>Bold text</b>Normal text</p><i>italic text</i></div>"
            )
            self.assertEqual(node.to_html(), expected_html)

    def test_deeply_nested_structure(self):
        node = ParentNode(
            "section",
            [
                ParentNode(
                    "article",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                            ],
                        ),
                        LeafNode("i", "italic text"),
                    ],
                ),
                LeafNode(None, "Standalone text"),
            ],
        )
        expected_html = (
            "<section><article><p><b>Bold text</b>Normal text</p>"
            "<i>italic text</i></article>Standalone text</section>"
        )
        self.assertEqual(node.to_html(), expected_html)


    def test_empty_leaf_node(self):
        node = LeafNode(None, "")
        self.assertEqual(node.to_html(), "")

    def test_parent_with_mixed_empty_and_non_empty_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, ""),
                LeafNode("b", "Bold text"),
                LeafNode(None, ""),
                LeafNode("i", "italic text"),
                LeafNode(None, ""),
            ],
        )
        expected_html = "<p><b>Bold text</b><i>italic text</i></p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_parent_with_special_characters(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold & text"),
                LeafNode(None, "<Normal text>"),
                LeafNode("i", 'italic "text"'),
            ],
        )
        expected_html = "<p><b>Bold & text</b><Normal text><i>italic \"text\"</i></p>"
        self.assertEqual(node.to_html(), expected_html)
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()

