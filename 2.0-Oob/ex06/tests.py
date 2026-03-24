#!/usr/bin/env python3
# coding: utf-8

import traceback

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


def expect_validation_error(factory):
    try:
        factory()
        raise AssertionError("Elem.ValidationError was expected.")
    except Elem.ValidationError:
        pass


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
    assert page.is_valid() is True
    assert str(page).startswith("<!DOCTYPE html>\n<html>")
    print("Valid page: OK.")


def test_invalid_root():
    expect_validation_error(lambda: Page(Body()))
    print("Invalid root: OK.")


def test_invalid_html_children():
    expect_validation_error(lambda: Page(Html([Body(), Head()])))
    expect_validation_error(lambda: Page(Html([Head(), Body(), Body()])))
    print("Html children: OK.")


def test_invalid_head():
    expect_validation_error(lambda: Page(Html([Head(), Body()])))
    expect_validation_error(
        lambda: Page(Html([Head([Title(Text("a")), Title(Text("b"))]), Body()]))
    )
    expect_validation_error(
        lambda: Page(Html([Head([Title(Text("a")), H1(Text("bad"))]), Body()]))
    )
    print("Head rules: OK.")


def test_body_and_div_rules():
    expect_validation_error(
        lambda: Page(Html([Head([Title(Text("a"))]), Body([Li(Text("bad"))])]))
    )
    expect_validation_error(
        lambda: Page(
            Html(
                [
                    Head([Title(Text("a"))]),
                    Body([Div([Table([Tr([Td(Text("ok"))])]), Head([Title(Text("x"))])])]),
                ]
            )
        )
    )
    print("Body and Div rules: OK.")


def test_text_only_rules():
    expect_validation_error(
        lambda: Page(Html([Head([Title([Text("a"), Text("b")])]), Body()]))
    )
    expect_validation_error(
        lambda: Page(Html([Head([Title(Text("a"))]), Body([H1([Text("a"), Text("b")])])]))
    )
    expect_validation_error(
        lambda: Page(Html([Head([Title(Text("a"))]), Body([Ul([Li(Span(Text("x")))])])]))
    )
    print("Text-only nodes: OK.")


def test_p_and_span_rules():
    valid = Page(
        Html([Head([Title(Text("a"))]), Body([P([Text("a"), Span(Text("b")), Img(attr={"src": "x"})])])])
    )
    assert valid.is_valid() is True

    expect_validation_error(
        lambda: Page(Html([Head([Title(Text("a"))]), Body([P([Div()])])]))
    )
    expect_validation_error(
        lambda: Page(Html([Head([Title(Text("a"))]), Body([Span(P(Text("bad")))])]))
    )
    print("P and Span rules: OK.")


def test_list_rules():
    expect_validation_error(lambda: Page(Html([Head([Title(Text("a"))]), Body([Ul()])])))
    expect_validation_error(
        lambda: Page(Html([Head([Title(Text("a"))]), Body([Ol([Li(Text("ok")), P(Text("bad"))])])]))
    )
    print("List rules: OK.")


def test_table_rules():
    expect_validation_error(
        lambda: Page(Html([Head([Title(Text("a"))]), Body([Table()])]))
    )
    expect_validation_error(
        lambda: Page(Html([Head([Title(Text("a"))]), Body([Table([Td(Text("bad"))])])]))
    )
    expect_validation_error(
        lambda: Page(
            Html([Head([Title(Text("a"))]), Body([Table([Tr([Th(Text("h")), Td(Text("d"))])])])])
        )
    )
    print("Table rules: OK.")


def test_simple_tags_cannot_have_children():
    expect_validation_error(
        lambda: Page(Html([Head([Title(Text("a")), Meta(Text("bad"))]), Body()]))
    )
    expect_validation_error(
        lambda: Page(Html([Head([Title(Text("a"))]), Body([Img(Text("bad"))])]))
    )
    print("Simple tags: OK.")


def test():
    test_valid_page()
    test_invalid_root()
    test_invalid_html_children()
    test_invalid_head()
    test_body_and_div_rules()
    test_text_only_rules()
    test_p_and_span_rules()
    test_list_rules()
    test_table_rules()
    test_simple_tags_cannot_have_children()


if __name__ == "__main__":
    try:
        test()
        print("Tests succeeded!")
    except AssertionError as e:
        traceback.print_exc()
        print(e)
        print("Tests failed!")
