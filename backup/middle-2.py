import xml.etree.ElementTree as ET
from xml.dom import minidom
# from lxml import etree as ET
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
    glyph_group = root.find(".//svg:g[@ink:label='glyph']", namespace)

    return glyph_group

def declare_glyph_gradient(defs):
    existing = defs.find("svg:linearGradient[@id='glyph-gradient']", namespace)
    if existing is not None:
        defs.remove(existing)

    gradient = ET.SubElement(
        defs,
        f'{{{svg_ns}}}linearGradient',
        {
            'id': 'glyph-gradient',
            'x1': '0',
            'y1': '0',
            'x2': '1',
            'y2': '0',
            'gradientUnits': 'userSpaceOnUse'
        }
    )
    stop_1 = ET.SubElement(
        gradient,
        f'{{{svg_ns}}}stop',
        {
            'offset': '0'
        }
    )
    stop_2 = ET.SubElement(
        gradient,
        f'{{{svg_ns}}}stop',
        {
            'offset': '1'
        }
    )

def draw_directory(base: Path, glyph: Path):
    glyph_group = get_glyph(glyph)
    glyph_copy = deepcopy(glyph_group)

    tree = ET.parse(base)
    root = tree.getroot()

    root.append(glyph_copy)

    defs = root.find('svg:defs', namespace)
    declare_glyph_gradient(defs)

    ET.indent(tree, space='  ', level=0)

    # remover ns0:
    #ET.register_namespace('', svg_ns)
    #ET.register_namespace('ink', inkscape_ns)
    
    tree.write(
        'output/test.svg',
        xml_declaration=True,
        encoding='UTF-8'
    )
    
    options = scour.sanitizeOptions()
    options.indent_spaces = 4
    options.remove_metadata = True
    #options.shorten_ids = True

    svg_input = open("output/test.svg", "r").read()
    svg_saida = scour.scourString(svg_input, options)

    with open("output/test-clear.svg", "w") as f:
        f.write(svg_saida)

    # xml_str = ET.tostring(root, encoding='utf-8')
    # pretty = minidom.parseString(xml_str).toprettyxml(indent='  ')
    # with open('output/test.svg', 'w', encoding='utf-8') as f:
    #     f.write(pretty)

    
draw_directory(
    Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates/folder.svg'),
    Path('/mnt/seagate/workspace/coding/projects/scripts/copyhex/templates/glyphs/folder-games.svg')
)