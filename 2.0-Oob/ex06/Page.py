from elem import Elem, Text
from elements import (
    Body,
    Br,
    Div,
    H1,
    H2,
    Head,
    Hr,
    Html,
    Img,
    Li,
    Meta,
    Ol,
    P,
    Span,
    Table,
    Td,
    Th,
    Title,
    Tr,
    Ul,
)


class Page:
    def __init__(self, elem: Elem):
        if not isinstance(elem, Elem):
            raise Elem.ValidationError("Error: Argument must be an Elem instance.")
        self.elem = elem
        self.valid = self.is_valid()

    def is_valid(self) -> bool:
        """
        A page is valid if its root element is an Html instance and every node
        in the tree respects the allowed content model.
        """
        self._check_instances(self.elem)
        self._check_tree(self.elem)
        return True

    def _check_tree(self, node=None):
        if node is None:
            node = self.elem
        if node is self.elem and not isinstance(node, Html):
            self._raise_validation("Error: Page root element must be an Html instance.")

        self._check_instances(node)
        if isinstance(node, Text):
            return

        self._check_html(node)
        self._check_head(node)
        self._check_body_and_div(node)
        self._check_title_h1_h2_li_th_td(node)
        self._check_p(node)
        self._check_span(node)
        self._check_ul_ol(node)
        self._check_tr(node)
        self._check_table(node)
        self._check_empty_simple_content(node)

        for child in node.content:
            self._check_instances(child)
            self._check_tree(child)

    def write_to_file(self, filename):
        with open(filename, "w") as f:
            f.write(str(self))

    def _raise_validation(self, message: str):
        self.valid = False
        raise Elem.ValidationError(message)

    def _check_instances(self, node):
        if not isinstance(node, (Elem, Text)):
            self._raise_validation("Error: All content must be Elem or Text instances.")

    def _check_html(self, node):
        if not isinstance(node, Html):
            return
        if len(node.content) != 2:
            self._raise_validation(
                "Error: Html element must contain exactly two elements: a Head and a Body."
            )
        if not isinstance(node.content[0], Head) or not isinstance(node.content[1], Body):
            self._raise_validation(
                "Error: Html element must contain a Head element followed by a Body element."
            )

    def _check_head(self, node):
        if not isinstance(node, Head):
            return
        if sum(isinstance(content, Title) for content in node.content) != 1:
            self._raise_validation(
                "Error: Head element must contain exactly one Title element."
            )
        for content in node.content:
            if not isinstance(content, (Title, Meta)):
                self._raise_validation(
                    "Error: Head element can only contain Title and Meta elements."
                )

    def _check_body_and_div(self, node):
        if not isinstance(node, (Body, Div)):
            return
        allowed = (H1, H2, Div, Table, Ul, Ol, Span, Img, P, Hr, Br, Text)
        for content in node.content:
            if not isinstance(content, allowed):
                self._raise_validation(
                    "Error: Body and Div elements contain an invalid child element."
                )

    def _check_title_h1_h2_li_th_td(self, node):
        if not isinstance(node, (Title, H1, H2, Li, Th, Td)):
            return
        if len(node.content) != 1 or type(node.content[0]) is not Text:
            self._raise_validation(
                "Error: Title, H1, H2, Li, Th, and Td elements must contain one Text and only this Text."
            )

    def _check_p(self, node):
        if not isinstance(node, P):
            return
        allowed = (Text, Span, Img, Br)
        for content in node.content:
            if not isinstance(content, allowed):
                self._raise_validation(
                    "Error: P elements can only contain Text, Span, Img, and Br elements."
                )

    def _check_span(self, node):
        if not isinstance(node, Span):
            return
        allowed = (Text, Img, Br)
        for content in node.content:
            if not isinstance(content, allowed):
                self._raise_validation(
                    "Error: Span elements can only contain Text, Img, and Br elements."
                )

    def _check_ul_ol(self, node):
        if not isinstance(node, (Ul, Ol)):
            return
        if len(node.content) == 0:
            self._raise_validation("Error: Ul and Ol elements must contain at least one Li element.")
        for content in node.content:
            if not isinstance(content, Li):
                self._raise_validation("Error: Ul and Ol elements can only contain Li elements.")

    def _check_tr(self, node):
        if not isinstance(node, Tr):
            return
        if len(node.content) == 0:
            self._raise_validation("Error: Tr elements must contain at least one Th or Td element.")
        if not all(isinstance(content, (Th, Td)) for content in node.content):
            self._raise_validation("Error: Tr elements can only contain Th and Td elements.")
        has_th = any(isinstance(content, Th) for content in node.content)
        has_td = any(isinstance(content, Td) for content in node.content)
        if has_th and has_td:
            self._raise_validation("Error: Tr elements cannot contain both Th and Td elements.")

    def _check_table(self, node):
        if not isinstance(node, Table):
            return
        if len(node.content) == 0:
            self._raise_validation("Error: Table elements must contain at least one Tr element.")
        for content in node.content:
            if not isinstance(content, Tr):
                self._raise_validation("Error: Table elements can only contain Tr elements.")

    def _check_empty_simple_content(self, node):
        if isinstance(node, (Meta, Img, Hr, Br)) and len(node.content) != 0:
            self._raise_validation(
                "Error: Meta, Img, Hr, and Br elements cannot contain child elements."
            )

    def __str__(self):
        if isinstance(self.elem, Html):
            return "<!DOCTYPE html>\n" + str(self.elem)
        return str(self.elem)
