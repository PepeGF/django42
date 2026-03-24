from Page import Page
from elem import Elem, Text
from elements import (
    Body,
    Br,
    Div,
    H1,
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

def test_valid_page():
    page = Page(
        Html(
            [
                Head([Title(Text("My page")), Meta(attr={"charset": "UTF-8"})]),
                Body(
                    [
                        H1(Text("Welcome")),
                        P([Text("inline "), Span(Text("content")), Br(), Text("ok")]),
                        Div([Text("image: "), Img(attr={"src": "cat.png"})]),
                        Ul([Li(Text("one")), Li(Text("two"))]),
                        Ol([Li(Text("first"))]),
                        Table(
                            [
                                Tr([Th(Text("Name")), Th(Text("Age"))]),
                                Tr([Td(Text("Alice")), Td(Text("42"))]),
                            ]
                        ),
                        Hr(),
                    ]
                ),
            ]
        )
    )
    print(page)
    with open("test2.html", "w") as f:
        f.write(str(page))

if __name__ == "__main__":
    test_valid_page()