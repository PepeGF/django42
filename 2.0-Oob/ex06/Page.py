from elem import Elem, Text
from elements import Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br

class Page:
    def __init__(self, elem: Elem):
        if not isinstance(elem, Elem):
            raise Elem.ValidationError("Error: Argument must be an Elem instance.")
        self.elem = elem
        self.valid = self.is_valid()
        # self.is_valid()
        # if self.valid:
        #     self.write_to_file('page.html')

    def write_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))

    def is_valid(self) -> bool:
        """
        A page is valid if its root element is an Html instance.
        """
        self.valid = True
        self._check_instances()
        self._check_tree()
        self._check_html()
        self._check_head()
        self._check_body_and_div()
        self._check_title_h1_h2_li_th_td()
        self._check_p()
        self._check_span()
        self._check_ul_ol()
        self._check_tr()
        self._check_table()
        return self.valid

    def _check_instances(self):
        if not isinstance(self.elem, Elem):
            self.valid = False
            raise Elem.ValidationError("Error: All content must be Elem instances.")

    def _check_html(self):
        if isinstance(self.elem, Html):
            if len(self.elem.content) != 2:
                self.valid = False
                raise Elem.ValidationError("Error: Html element must contain exactly two elements: a Head and a Body.")
            if not isinstance(self.elem.content[0], Head) or not isinstance(self.elem.content[1], Body):
                self.valid = False
                raise Elem.ValidationError("Error: Html element must contain a Head element followed by a Body element.")
            head_count = sum(1 for elem in self.elem.content if isinstance(elem, Head))
            body_count = sum(1 for elem in self.elem.content if isinstance(elem, Body))
            if head_count != 1 or body_count != 1:
                self.valid = False
                raise Elem.ValidationError("Error: Html element must contain exactly one Head and one Body element.")
            for content in self.elem.content:
                if not isinstance(content, (Head, Body)):
                    self.valid = False
                    raise Elem.ValidationError("Error: Html element can only contain Head and Body elements.")

    def _check_head(self):
        if isinstance(self.elem, Head):
            num_title = sum(1 for elem in self.elem.content if isinstance(elem, Title))
            if num_title != 1:
                self.valid = False
                raise Elem.ValidationError("Error: Head element must contain exactly one Title element.")
    
    def _check_body_and_div(self):
        if isinstance(self.elem, (Body, Div)):
            for content in self.elem.content:
                if not isinstance(content, (H1, H2, P, Div, Span, Hr, Br, Ul, Ol, Table)):
                    self.valid = False
                    raise Elem.ValidationError("Error: Body and Div elements can only contain H1, H2, P, Div, Span, Hr, Br, Ul, Ol, and Table elements.")

    def _check_title_h1_h2_li_th_td(self):
        if isinstance(self.elem, (Title, H1, H2, Li, Th, Td)):
            text_count = 0
            for content in self.elem.content:
                if not isinstance(content, Text):
                    self.valid = False
                    raise Elem.ValidationError("Error: Title, H1, H2, Li, Th, and Td elements can only contain Text elements.")
                text_count += 1
            if text_count != 1:
                self.valid = False
                raise Elem.ValidationError("Error: Title, H1, H2, Li, Th, and Td elements must contain one Text and only this Text.")

    def _check_p(self):
        if isinstance(self.elem, P):
            for content in self.elem.content:
                if not isinstance(content, Text):
                    self.valid = False
                    raise Elem.ValidationError("Error: P elements can only contain Text elements.")
                
    def _check_span(self):
        if isinstance(self.elem, Span):
            for content in self.elem.content:
                if not isinstance(content, (Text, P)):
                    self.valid = False
                    raise Elem.ValidationError("Error: Span elements can only contain Text and P elements.")
                
    def _check_ul_ol(self):
        if isinstance(self.elem, (Ul, Ol)):
            for content in self.elem.content:
                if not isinstance(content, Li):
                    self.valid = False
                    raise Elem.ValidationError("Error: Ul and Ol elements can only contain Li elements.")
                
    def _check_tr(self):
        if isinstance(self.elem, Tr):
            for content in self.elem.content:
                if not isinstance(content, (Th, Td)):
                    self.valid = False
                    raise Elem.ValidationError("Error: Tr elements can only contain Th and Td elements.")
            td_count = sum(1 for content in self.elem.content if isinstance(content, Td))
            th_count = sum(1 for content in self.elem.content if isinstance(content, Th))
            if td_count == 0 and th_count == 0:
                self.valid = False
                raise Elem.ValidationError("Error: Tr elements must contain at least one Th or Td element.")
            if td_count > 0 and th_count > 0:
                self.valid = False
                raise Elem.ValidationError("Error: Tr elements cannot contain both Th and Td elements.")
            
    def _check_table(self):
        if isinstance(self.elem, Table):
            for content in self.elem.content:
                if not isinstance(content, Tr):
                    self.valid = False
                    raise Elem.ValidationError("Error: Table elements can only contain Tr elements.")


    def __str__(self):
        """
        Here is a method to render the page as a string, by rendering its root
        element (and recursively all its content and embedded elements, if any
        """
        if isinstance(self.elem, Html):
            return "<!DOCTYPE html>\n" + str(self.elem)
        return str(self.elem)
    
"""
Breve revisión de Page.py (Page.py) — puntos principales a corregir o mejorar:

Constructor: ahora escribe page.html inmediatamente porque self.valid se inicializa True y self.is_valid() está comentado; mover write_to_file para que se ejecute sólo después de una validación exitosa y no en el constructor por defecto.
is_valid(): no devuelve nada (debe devolver True/False). Actualmente lanza excepciones y cambia self.valid, pero la firma debería ser clara y consistente (p.ej. devolver bool y opcionalmente lanzar excepciones para errores graves).
Validación recursiva: tus _check_* sólo comprueban self.elem (la raíz) con isinstance(self.elem, X). Necesitas recorrer recursivamente todo el árbol (nodos hijos) y aplicar las reglas en cada nodo, no sólo en la raíz.
Acceso seguro a hijos en _check_html: haces self.elem.content[0]/[1] antes de comprobar len → posible IndexError. Comprobar longitud antes de indexar.
Reglas incompletas/incorrectas:
No compruebas que todos los nodos tengan tags permitidos (lista de tipos + Text).
_check_head sólo verifica número de Title pero no impide otros tipos de hijo en Head.
_check_ul_ol y _check_table no verifican la presencia de al menos un hijo (Ul/Ol/Table deben tener ≥1 hijo).
_check_body_and_div permite P pero la regla original exige que Body/Div sólo contengan H1,H2,Div,Table,Ul,Ol,Span o Text (revisar lista exacta y permitir Text).
_check_title_h1_h2_li_th_td y _check_p usan isinstance con Text (esto suele funcionar) pero deben garantizar "exactamente un Text y sólo ese" (comprobar nº de hijos == 1).
_check_span debería permitir Text o uno o más P; si contiene P, validar cada P.
_check_tr correctamente evita mezcla Th/Td, pero asegúrate de aplicar la comprobación recursiva a cada Th/Td.
Manejo de Text('') y listas vacías: considerar que Elem.add_content filtra Text(''); tu validador debe tratar textos vacíos como contenido vacío según convenga.
Salida y fichero: __str__ ya añade doctype si la raíz es Html — eso está bien; write_to_file debe escribir lo mismo que str(self) y sólo llamarse tras is_valid() positiva.
Errores/Excepciones vs booleanos: decide política (p.ej. is_valid() devuelve bool y métodos internos pueden devolver causas/paths inválidos; lanzar excepciones sólo para entradas mal formadas).
Siguientes pasos recomendados (breve):

Implementar una función recursiva _walk(node) que visite todos los nodos y aplique las reglas por tipo.
Consolidar las reglas en conjuntos (allowed_types, body_allowed, leaf_text_only, etc.) y usarlas durante el recorrido.
Hacer que is_valid() devuelva True/False (y opcionalmente recoja errores en self.errors).
Quitar la escritura automática en __init__ y llamar a write_to_file externamente tras validar.
Añadir tests que cubran los casos límite (Html correcto/incorrecto, Head con >1 Title, Ul vacío, Tr mixto, nodos no permitidos, escritura con/ sin doctype).
¿Quieres que te proponga el esquema de la función recursiva _walk y los conjuntos de reglas listos para implementar?

"""