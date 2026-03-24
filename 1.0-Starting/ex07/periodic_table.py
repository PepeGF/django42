import sys

def main():
    elements = read_and_parse_file()
    write_html_file(elements)

def read_and_parse_file():
    file_path = 'periodic_table.txt'
    try:
        with open(file_path, 'r') as file:
            raw_content = file.read()
    except FileNotFoundError:
        print("Error: The file 'periodic_table.txt' was not found.")
        sys.exit(1)

    elements = {}
    for line in raw_content.splitlines():
        if not line.strip():  # Skip empty lines
            continue
        parts = line.split(" = ")
        elemento = parts[0].strip()
        propiedades = parts[1].split(",")
        elements[parts[0].strip()] = {}
        for property in propiedades:
            key, value = property.split(":")
            elements[elemento][key.strip()] = value.strip()
        elements[elemento]['electron'] = elements[elemento]['electron'].split(" ")
    return elements

def write_html_file(elements):
    tabla_bruta = build_periodic_table(elements)
    css = build_style()
    html = build_html_document(tabla_bruta, css)
    output = 'periodic_table.html'
    with open(output, 'w') as f:
        f.write(html)

def build_periodic_table(elementos: dict):
    periodos = 7
    grupos = 18
    tabla = [[None for _ in range(grupos)] for _ in range(periodos)]

    for elemento, propiedades in elementos.items():
        fila = get_period_from_atomic_number(int(propiedades['number']))
        columna = int(propiedades['position'])
        tabla[fila][columna] = {
            'name': elemento,
            'number': propiedades['number'],
            'symbol': propiedades['small'],
            'molar': propiedades['molar'],
        }
    return tabla

def build_style():
    return """
      body {
      font-family: Arial, sans-serif;
      margin: 20px;
    }
    table {
      border-collapse: collapse;
    }
    td {
      width: 90px;
      height: 90px;
      border: 1px solid #000;
      vertical-align: top;
      padding: 6px;
    }
    td.empty {
      border: none;
    }
    .number {
      font-size: 12px;
    }
    .symbol {
      font-size: 24px;
      font-weight: bold;
      text-align: center;
      margin: 8px 0;
    }
    .name,
    .molar {
      font-size: 12px;
    }"""

def get_period_from_atomic_number(numero_atomico: int):
    if numero_atomico <= 2:
        return 0
    if numero_atomico <= 10:
        return 1
    if numero_atomico <= 18:
        return 2
    if numero_atomico <= 36:
        return 3
    if numero_atomico <= 54:
        return 4
    if numero_atomico <= 86:
        return 5
    return 6

def build_html_document(tabla: list[list], css: str):
    filas = []
    for fila in tabla:
        celda = []
        for elemento in fila:
            if elemento is None:
                celda.append('        <td class="empty"></td>')
            else:
                celda.append(build_element_cell(elemento))
        filas.append("    <tr>\n" + "\n".join(celda) + "\n    </tr>")

    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Periodic Table</title>
  <style>
    {css}
  </style>
</head>
<body>
  <table>
    {filas}
  </table>
</body>
</html>
""".format(filas="\n".join(filas), css=css)

def build_element_cell(element):
    return f"""      <td>
        <div class="number">{element['number']}</div>
        <div class="symbol">{element['symbol']}</div>
        <div class="name">{element['name']}</div>
        <div class="molar">{element['molar']}</div>
      </td>"""


if __name__ == "__main__":
    main()
