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

def sanitize_glyph_group(glyph_group):
    # glyph_group.attrib.clear() # limpa todos os atributos. fill, style, fill-opacity etc.
    # glyph_group.set("id", "glyph")
    # glyph_group.set(f"{{{inkscape_ns}}}label", "glyph")

    # limpa todos os atributos. fill, style, fill-opacity etc.
    for k in list(glyph_group.attrib.keys()):
        if not k.endswith("id") and not k.endswith("label"):
            glyph_group.attrib.pop(k)

    for elem in glyph_group.iter():
        # remove classes (ColorScheme-Text, etc)
        elem.attrib.pop("class", None)

        # remove atributos de apresentação direta
        for attr in [
            "fill",
            "stroke",
            "color",
            "opacity",
            "mix-blend-mode",
            "fill-opacity",
            "stroke-opacity"
        ]:
            elem.attrib.pop(attr, None)

        # limpa style completamente
        if "style" in elem.attrib:
            elem.attrib.pop("style")

def prune_unused_gradients(defs):
    for grad in list(defs):
        if grad.tag.endswith("linearGradient") or grad.tag.endswith("radialGradient"):
            if grad.attrib.get("id") not in {
                "front-gradient",
                "base-gradient",
                "glyph-gradient"
            }:
                defs.remove(grad)

# def prune_all_gradients(defs):
#     for grad in list(defs):
#         if grad.tag.endswith("linearGradient") or grad.tag.endswith("radialGradient"):
#             defs.remove(grad)

def get_glyph(svg: Path):
    """
    isso espera que o svg passado tenha um grupo com um label ou id específico
    o que estiver dentro desse grupo vai ser considerado como parte do glifo
    """

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
    glyph: Path,
    output_directory: Path,
    palette: Palette = DEFAULT,
    prettify: bool = True
    ):
    output_directory.mkdir(exist_ok=True, parents=True)

    glyph_group = get_glyph(glyph)
    if glyph_group is None:
        error(f'glyph group não encontrado para {glyph.name}')
        return
    else:
        success(f'glyph group encontrado para {glyph.name}')

    tree = ET.parse(base)
    root = tree.getroot()
    
    glyph_copy = deepcopy(glyph_group)
    sanitize_glyph_group(glyph_copy)

    if glyph_copy is None:
        error(f'erro ao copiar o glifo {glyph.name}')
        return

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
    declare_glyph_gradient(defs, palette)
    
    # escritura do svg
    output_directory.mkdir(parents=True, exist_ok=True)
    output = output_directory / glyph.name
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

TEMPLATES = Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates')
OUTPUT = Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/output')
GLYPHS = TEMPLATES / 'glyphs'
BASES = TEMPLATES.glob('*.svg')

for glyph in list(GLYPHS.rglob('*.svg')):
    print(f'processando o glifo {glyph.name}')
    
    for base in BASES:
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
                glyph=glyph,
                output_directory=output,
                palette=palette,
                prettify=False
            )

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