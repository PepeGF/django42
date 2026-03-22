from elem import Elem, Text

class Html(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='html', attr=attr, content=content, tag_type='double')


class Head(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='head', attr=attr, content=content, tag_type='double')


class Body(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='body', attr=attr, content=content, tag_type='double')


class Title(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='title', attr=attr, content=content, tag_type='double')


class Meta(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='meta', attr=attr, content=content, tag_type='simple')


class Img(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='img', attr=attr, content=content, tag_type='simple')


class Table(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='table', attr=attr, content=content, tag_type='double')


class Th(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='th', attr=attr, content=content, tag_type='double')


class Tr(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='tr', attr=attr, content=content, tag_type='double')


class Td(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='td', attr=attr, content=content, tag_type='double')


class Ul(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='ul', attr=attr, content=content, tag_type='double')


class Ol(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='ol', attr=attr, content=content, tag_type='double')


class Li(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='li', attr=attr, content=content, tag_type='double')


class H1(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='h1', attr=attr, content=content, tag_type='double')


class H2(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='h2', attr=attr, content=content, tag_type='double')


class P(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='p', attr=attr, content=content, tag_type='double')


class Div(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(attr=attr, content=content, tag_type='double')


class Span(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='span', attr=attr, content=content, tag_type='double')


class Hr(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='hr', attr=attr, content=content, tag_type='double')


class Br(Elem):
    def __init__(self, content=None, attr: dict = {}):
        super().__init__(tag='br', attr=attr, content=content, tag_type='double')



def test():
    print("Test 1: Empty HTML document")
    print(Html([Head(), Body()]))
    
    print("-"*80, "\nTest 2: HTML document with content")
    print(Html(
        [
            Head([Title(Text('Hello ground!'))]),
            Body([H1(Text('Oh no, not again!')), Img(attr={'src': 'http://i.imgur.com/pfp3T.jpg'})])
        ]
    ))

    print("-"*80, "\nTest 3: HTML document with table")
    print(
        Html(
            [Table(
                [Tr([Th(Text('Name')), Th(Text('Age'))]), Tr([Td(Text('Pepe')), Td(Text('25'))])]
                )
            ]
            )
        )
    
    print("-"*80, "\nTest 4: HTML document with list")
    print(
        Html(
            [Ul([Li(Text('Item 1')), Li(Text('Item 2')), Li(Text('Item 3'))])]
        )
    )

    print("-"*80, "\nTest 5: Test the other tags")
    wololo = str(
        Html(
            [
                Head([Title(Text('Test other tags'))]),
                Body([
                    H2(Text('This is a heading')),
                    P([
                        Text('This is a paragraph with a '), 
                        Span(Text('span'), attr={'style': 'color:blue'}), 
                        Text('.')
                        ]),
                    Hr(),
                    Br(),
                    Div([Text('This is a div with an image: '), Img(attr={'src': 'http://i.imgur.com/pfp3T.jpg'})])
                ])
            ]
        )
    )
    print(wololo)
    with open('test.html', 'w') as f:
        f.write(wololo)




if __name__ == '__main__':
    test()