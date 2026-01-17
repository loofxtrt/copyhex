import xml.etree.ElementTree as ET
from copy import deepcopy
from pathlib import Path
from dataclasses import dataclass, fields

from scour import scour

svg_ns = 'http://www.w3.org/2000/svg'
inkscape_ns = 'http://www.inkscape.org/namespaces/inkscape'
namespace = {
    'svg': svg_ns,
    'ink': inkscape_ns
}

@dataclass
class Palette:
    background: str
    base_dark: str
    base_light: str
    glyph_dark: str
    glyph_light: str
    identifier: str = None

DEFAULT = Palette(
    background='#0083d5',
    base_light='#12c5ff',
    base_dark='#1075f6',
    glyph_light='#126c98',
    glyph_dark='#0b4f94',
    identifier='default'
)

# baseado no ícone winefile
yellow = Palette(
    background='#b37100',
    base_light='#edbb5f',
    base_dark='#ffa100',
    glyph_light='#b67100',
    glyph_dark='#9d6100',
    identifier='yellow'
)

def get_glyph(svg: Path):
    tree = ET.parse(svg)
    root = tree.getroot()

    glyph_group = root.find(".//svg:g[@id='glyph']", namespace)
    if glyph_group is not None:
        return glyph_group

    glyph_group = root.find(".//svg:g[@ink:label='glyph']", namespace)
    if glyph_group is not None:
        return glyph_group
        
    # glyph_group = root.find(".//svg:g[@id='g6']", namespace)
    # if glyph_group is not None:
    #     return glyph_group
    
    return None

def declare_glyph_gradient(defs, palette: Palette):
    # remover uma possível declaração já existente de um gradiente com o mesmo id
    existing = defs.find("svg:linearGradient[@id='glyph-gradient']", namespace)
    if existing is not None:
        defs.remove(existing)

    gradient = ET.SubElement(
        defs,
        f'{{{svg_ns}}}linearGradient',
        {
            'id': 'glyph-gradient',
            'x1': '0',
            'y1': '1',
            'x2': '0',
            'y2': '0',
            'gradientUnits': 'objectBoundingBox' # vai do bottom ao top do svg em linha reta
        }
    )
    
    # A ORDEM DE DECLARAÇÃO DESSES STOPS IMPORTA
    # o com offset 0 precisa ser declarado primeiro que o com offset 1
    stop_dark = ET.SubElement(
        gradient,
        f'{{{svg_ns}}}stop',
        {
            'offset': '0',
            'stop-color': palette.glyph_dark
        }
    )
    stop_light = ET.SubElement(
        gradient,
        f'{{{svg_ns}}}stop',
        {
            'offset': '1',
            'stop-color': palette.glyph_light
        }
    )

def find_and_replace_base_colors(svg_string: str, new_palette: Palette):
    for f in fields(DEFAULT):
        old = getattr(DEFAULT, f.name)
        new = getattr(new_palette, f.name)

        if new is None or old is None:
            continue
    
        svg_string = svg_string.replace(old, new)

    return svg_string

def draw_directory(base: Path, glyph: Path, output_directory: Path, palette: Palette = DEFAULT):
    output_directory.mkdir(exist_ok=True, parents=True)

    glyph_group = get_glyph(glyph)
    if glyph_group is None:
        print(f'x > glyph group não encontrado para {glyph.name}')
        return
    else:
        print(f'o > glyph group encontrado para {glyph.name}')

    tree = ET.parse(base)
    root = tree.getroot()
    
    glyph_copy = deepcopy(glyph_group)
    root.append(glyph_copy)

    # aplicar gradiente em todos os paths do glifo
    for path in glyph_copy.findall(".//svg:path", namespace):
        path.set("fill", "url(#glyph-gradient)")
        if "style" in path.attrib:
            # opcional: remover fill antigo do style
            styles = path.attrib["style"].split(";")
            styles = [s for s in styles if not s.startswith("fill:")]
            styles.append("fill:url(#glyph-gradient)")
            path.set("style", ";".join(styles))

    # declaração do gradiente do glifo nas defs
    defs = root.find('svg:defs', namespace)
    declare_glyph_gradient(defs, DEFAULT)
    
    # escritura do svg
    output_directory.mkdir(parents=True, exist_ok=True)
    output = output_directory / glyph.name
    tree.write(
        output,
        xml_declaration=True,
        encoding='UTF-8'
    )

    # formatação
    options = scour.sanitizeOptions()
    options.indent_spaces = 4
    options.remove_metadata = True

    svg_input = open(output, 'r').read() # transforma o svg em texto e logo depois altera as cores
    svg_input = find_and_replace_base_colors(svg_input, palette)

    svg_saida = scour.scourString(svg_input, options)

    with open(output, 'w') as f:
        f.write(svg_saida)

TEMPLATES = Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates')
OUTPUT = Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/output')
GLYPHS = TEMPLATES / 'glyphs'
BASES = [TEMPLATES / 'folder.svg', TEMPLATES / 'folder-outer.svg']

for glyph in GLYPHS.rglob('*.svg'):
    for base in BASES:
        for palette in [DEFAULT, yellow]:
            output = OUTPUT / base.stem
            if palette.identifier is not None:
                output = output / palette.identifier

            draw_directory(
                base=base,
                glyph=glyph,
                output_directory=output,
                palette=palette
            )

# for glyph in Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates/glyphs').rglob('*.svg'):
#     draw_directory(
#         Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates/folder.svg'),
#         glyph,
#         Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/output'),
#         yellow
#     )

# for glyph in Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates/glyphs').rglob('*.svg'):
#     draw_directory(
#         Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates/folder-outer.svg'),
#         glyph,
#         Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/output/outer')
#     )