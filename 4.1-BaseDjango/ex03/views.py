from django.shortcuts import render

# Create your views here.

def table_view(request):
    # Column names (generated here, not hard-coded in template)
    headers = ['noir', 'rouge', 'bleu', 'vert']

    # Base RGB colors for each column (dark-ish starts)
    bases = [
        (0, 0, 0),       # noir (black)
        (180, 10, 10),   # rouge (dark red)
        (20, 40, 200),   # bleu (dark blue)
        (10, 120, 10),   # vert (dark green)
    ]

    def _hex(rgb):
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def _interp(a, b, t):
        return (int(a[0] + (b[0] - a[0]) * t),
                int(a[1] + (b[1] - a[1]) * t),
                int(a[2] + (b[2] - a[2]) * t))

    lines = 50

    # For each base color generate `lines` shades interpolating towards white
    columns_shades = []
    white = (255, 255, 255)
    for base in bases:
        shades = []
        for i in range(lines):
            t = i / (lines - 1) if lines > 1 else 0
            rgb = _interp(base, white, t)
            shades.append(_hex(rgb))
        columns_shades.append(shades)

    # Build rows: list of 50 rows, each row is list of 4 hex colors
    rows = []
    for i in range(lines):
        row = [columns_shades[c][i] for c in range(len(columns_shades))]
        rows.append(row)

    return render(
        request,
        'ex03/table.html',
        context={
            'headers': headers,
            'rows': rows,
        }
    )