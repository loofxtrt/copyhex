import xml.etree.ElementTree as ET
import json
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

def error(text):
    print(f"\033[31m{text}\033[0m")

def success(text):
    print(f"\033[32m{text}\033[0m")

def normalize_hex_value(value: str):
    if not value.startswith('#'):
        value = f'#{value}'

    # 6 + 1 pq a hashtag conta como caractere,
    # então no total um código comum de hex tem 7 chars
    if len(value) > 7 and value.endswith('ff'):
        value = value.removesuffix('ff')

    print(f'valor normalizado: {value}')
    return value

@dataclass
class Palette:
    background: str
    base_dark: str
    base_light: str
    glyph_dark: str
    glyph_light: str
    identifier: str = None

    def __post_init__(self):
        for f in fields(self):
            if f.name == 'identifier':
                continue

            value = getattr(self, f.name)
            normalized = normalize_hex_value(value)
            setattr(self, f.name, normalized)

DEFAULT = Palette(
    background='#0083d5',
    base_light='#12c5ff',
    base_dark='#1075f6',
    glyph_light='#126c98',
    glyph_dark='#0b4f94',
    identifier='default'
)

# baseado na default
PRISM = Palette(
    background='#0083d5',
    base_light='#12c5ff',
    base_dark='#1075f6',
    glyph_light='#146ab3ff',
    glyph_dark='#06314eff',
    identifier='prism'
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

# baseado no win 11
yellow_win = Palette(
    background='#f4b61fff',
    base_light='#fce798',
    base_dark='#ffc937ff',
    glyph_dark='#a57001ff',
    glyph_light='#be900dff',
    identifier='yellow-win'
)

def draw_glyph(root, data: dict):
    group = ET.SubElement(
        root,
        'g',
        {
            'id': 'glyph'
        }
    )

    for p in data.get('paths'):
        el = ET.SubElement(
            group,
            'path',
            {
                'd': p,
                'fill': 'url(#glyph-gradient)'
            }
        )

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
            'y1': '48',
            'x2': '0',
            'y2': '0',
            'gradientUnits': 'userSpaceOnUse' # vai do bottom ao top do svg em linha reta
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
    # obter todos as propriedades presentes na classe da paleta,
    # pegar a paleta base padrão e substituir as cores antigas pelas novas
    for f in fields(DEFAULT):
        old = getattr(DEFAULT, f.name)
        new = getattr(new_palette, f.name)

        if new is None or old is None:
            continue
    
        svg_string = svg_string.replace(old, new)

    return svg_string

def draw_directory(
    base: Path,
    glyph_data: dict,
    output_directory: Path,
    palette: Palette = DEFAULT,
    prettify: bool = True
    ):
    output_directory.mkdir(exist_ok=True, parents=True)

    tree = ET.parse(base)
    root = tree.getroot()

    # declaração do gradiente do glifo nas defs
    defs = root.find('svg:defs', namespace)
    declare_glyph_gradient(defs, palette)

    draw_glyph(root, glyph_data)
    
    # escritura do svg
    output_directory.mkdir(parents=True, exist_ok=True)
    output = output_directory / (glyph_data.get('label') + '.svg')
    tree.write(
        output,
        xml_declaration=True,
        encoding='UTF-8'
    )

    # transformar o svg em texto e alterar as cores de acordo com a paleta
    svg_input = open(output, 'r').read()
    svg_input = find_and_replace_base_colors(svg_input, palette)
    svg_output = svg_input

    # formatação
    if prettify:
        options = scour.sanitizeOptions()
        options.indent_spaces = 4
        options.remove_metadata = True
        options.shorten_ids = False # mantém os ids iguais

        # converter de volta pra uma string scour e escrever como svg
        svg_output = scour.scourString(svg_input, options)

    with open(output, 'w') as f:
        f.write(svg_output)

def main():
    TEMPLATES = Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates')
    OUTPUT = Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/output')

    json_glyphs = TEMPLATES / 'glyphs.json'
    with json_glyphs.open('r', encoding='utf-8') as f:
        glyphs = json.load(f)

    for g in glyphs:
        print(f'processando o glifo {g.get('label')}')

        for base in TEMPLATES.glob('*.svg'):
            for palette in [
                DEFAULT,
                PRISM,
                yellow,
                yellow_win
                ]:
                output = OUTPUT / base.stem

                if palette.identifier is not None:
                    output = output / palette.identifier

                draw_directory(
                    base=base,
                    glyph_data=g,
                    output_directory=output,
                    palette=palette,
                    #prettify=False
                )

main()

# - [ ] documentar como o gradiente foi obtido

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