import xml.etree.ElementTree as ET
from copy import deepcopy
from pathlib import Path
from dataclasses import dataclass

from scour import scour

#base_group = root.find(".//svg:g[@ink:label='base']", namespace)
#namespace = {'svg': svg_ns}
svg_ns = 'http://www.w3.org/2000/svg'
inkscape_ns = 'http://www.inkscape.org/namespaces/inkscape'
namespace = {
    'svg': svg_ns,
    'ink': inkscape_ns
}

# remover ns0:
#ET.register_namespace('', svg_ns)
#ET.register_namespace('ink', inkscape_ns)

# glyph_gradient = '''
# <linearGradient
#   id="glyph-gradient"
#   x1="0"
#   y1="0"
#   x2="1"
#   y2="0"
#   gradientUnits="userSpaceOnUse"
#   gradientTransform="matrix(2.54933e-15,-41.6338,41.6338,2.54933e-15,445.153,52.7218)">
#   <stop
#     style="stop-color:#0b4f94;stop-opacity:1;"
#     offset="0"
#     id="stop3" />
#   <stop
#     style="stop-color:#126c98;stop-opacity:1;"
#     offset="1"
#     id="stop4" />
# </linearGradient>
# '''

# options = scour.sanitizeOptions()
# options.indent_spaces = 4
# options.remove_metadata = True

# svg_input = open(f'output/{glyph.name}', 'r').read()
# svg_saida = scour.scourString(svg_input, options)

# with open(f'output/{glyph.name}', 'w') as f:
#     f.write(svg_saida)

# draw_directory(
#     Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates/folder.svg'),
#     Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates/glyphs/folder-games.svg') # pasta pega do copycat sem alterações
# )

#ET.indent(tree, space='  ', level=0)

@dataclass
class Palette:
    background: str
    base_dark: str
    base_light: str
    glyph_dark: str
    glyph_light: str

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

def declare_glyph_gradient(defs):
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
            'stop-color': '#0b4f94'
        }
    )
    stop_light = ET.SubElement(
        gradient,
        f'{{{svg_ns}}}stop',
        {
            'offset': '1',
            'stop-color': '#126c98'
        }
    )

def modify_base_colors(defs, palette: Palette):
    base_gradient = defs.find("svg:linearGradient[@id='base-gradient']", namespace)

    if base_gradient is None:
        print('    x > base gradient não encontrado')
        return
    else:
        print('    o > base gradient encontrado')

    stops = list(base_gradient.findall('svg:stop', namespace))
    stops[0].set('stop-color', palette.base_dark)
    stops[1].set('stop-color', palette.base_light)

def find_and_replace_base_colors(svg_string: str, default_palette: Palette, new_palette: Palette):
    svg_string = svg_string.replace(default_palette.base_dark, new_palette.base_dark)
    svg_string = svg_string.replace(default_palette.base_light, new_palette.base_light)
    svg_string = svg_string.replace(default_palette.background, new_palette.background)

    return svg_string


def draw_directory(base: Path, glyph: Path, output_directory: Path, palette: Palette = None):
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

    # declaração do gradiente do glifo e alteração do gradiente da base
    defs = root.find('svg:defs', namespace)
    
    declare_glyph_gradient(defs)
    
    # if palette is not None:
    #    modify_base_colors(defs, palette)
    
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

    svg_input = open(output, 'r').read()
    
    if palette is not None:
        svg_input = find_and_replace_base_colors(svg_input, default, palette)

    svg_saida = scour.scourString(svg_input, options)

    with open(output, 'w') as f:
        f.write(svg_saida)

default = Palette(
    background='#0083d5',
    base_light='#12c5ff',
    base_dark='#1075f6',
    glyph_light='#b67100',
    glyph_dark='#9d6100'
)

# baseado no ícone winefile
yellow = Palette(
    background='#b37100',
    base_light='#edbb5f',
    base_dark='#ffa100',
    glyph_light='#b67100',
    glyph_dark='#9d6100'
)

for glyph in Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates/glyphs').rglob('*.svg'):
    draw_directory(
        Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates/folder.svg'),
        glyph,
        Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/output'),
        yellow
    )

for glyph in Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates/glyphs').rglob('*.svg'):
    draw_directory(
        Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates/folder-outer.svg'),
        glyph,
        Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/output/outer')
    )