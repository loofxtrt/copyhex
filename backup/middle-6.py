import xml.etree.ElementTree as ET
from xml.dom import minidom
from scour import scour
from copy import deepcopy
from pathlib import Path

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
            'y1': '48', # vai do bottom ao top do svg em linha reta
            'x2': '0',
            'y2': '0',
            'gradientUnits': 'userSpaceOnUse'
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
    stop_dark = ET.SubElement(
        gradient,
        f'{{{svg_ns}}}stop',
        {
            'offset': '0',
            'stop-color': '#0b4f94'
        }
    )

def draw_directory(base: Path, glyph: Path):
    glyph_group = get_glyph(glyph)
    if glyph_group is None:
        print(f'x > glyph group não encontrado para {glyph.name}')
        return
    else:
        print(f'o > glyph group encontrado para {glyph.name}')
    glyph_copy = deepcopy(glyph_group)




    for elem in glyph_copy.iter():
        if 'fill' in elem.attrib:
            del elem.attrib['fill']

        style = elem.get('style')
        if style:
            parts = []
            for part in style.split(';'):
                if not part.strip().startswith('fill:'):
                    parts.append(part)
            if parts:
                elem.set('style', ';'.join(parts))
            else:
                del elem.attrib['style']

        # agora sim aplica o gradiente
        elem.set('fill', 'url(#glyph-gradient)')


    tree = ET.parse(base)
    root = tree.getroot()

    root.append(glyph_copy)

    defs = root.find('svg:defs', namespace)
    declare_glyph_gradient(defs)

    ET.indent(tree, space='  ', level=0)
    
    tree.write(
        f'output/{glyph.name}',
        xml_declaration=True,
        encoding='UTF-8'
    )






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

for glyph in Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates/glyphs').rglob('*.svg'):
    draw_directory(
        Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates/folder.svg'),
        glyph
    )