import xml.etree.ElementTree as ET
import d_contents as data
import colors
from pathlib import Path

color_directory_background = '#0083d5'
color_directory_light = '#12c5ff'
color_directory_dark = '#1075f6'
color_glyph_light = '#126c98'
color_glyph_dark = '#0b4f94'

id_gradient_directory = 'directory-gradient'
id_gradient_glyph = 'glyph-gradient'

DEFAULT_TRANSFORM_VALUE = 'scale(.75)'
DEFAULT_GLYPH_GRADIENT_TRANSFORM = 'matrix(1.77928e-15,29.0579,-29.0579,1.77928e-15,-583.701,19.4233)'

def normalized_svg_file(file: Path) -> Path:
    if not file.name.endswith('.svg'):
        stringfied = str(file)
        stringfied += '.svg'
        file = Path(stringfied)
    
    return file

def normalize_hex_value(color_hex: str) -> str | None:
    # evitar possíveis valores nulos, pq hex deve sempre ser string
    # se não for, é melhor deixar claro que é um valor inválido
    if not isinstance(color_hex, str):
        return None
    
    # adiciona # na frente do valor hex se ele já não tiver
    if not color_hex.startswith('#'):
        color_hex = f'#{color_hex}'
    
    # se tiver mais de 7 dígitos no hex (contando com a # no começo)
    # obtendo apenas do índice 0 até o 7, removendo os últimos 2 (ou mais) dígitos que indicam a opacidade da cor
    # a opacidade pode fazer a cor quebrar no svg se estiver presente. ela deve ser definida com fill-opacity
    if len(color_hex) > 7:
        color_hex = color_hex[:7]

    return color_hex

def draw_directory(
    svg: ET.Element,
    back_fill: str,
    front_fill: str,
    group_id: str = 'directory-group'
    ):
    """
    args:
        svg:
            o elemento svg principal a qual o grupo gerado por essa função deve ser adicionado
        
        back_fill:
            preenchimento da parte de trás da pasta, geralmente é uma cor sólida
            se for um gradiente, deve ser passado com a formatação #(id-do-gradiente)

        front_fill:
            preenchimento da parte da frente da pasta, geralmente é um gradiente
            a mesma regra de formatação vale do argumento anterior também vale pra esse
        
        group_id:
            nome/id que o grupo gerado por essa função vai ter
    """

    group = ET.SubElement(svg, 'g', {
        'id': group_id,
        'transform': 'scale(.75)'
    })

    # background do diretório, um retangulo com cor sólida
    ET.SubElement(group, 'path', {
        'd': 'm61.122 15.88c0-2.762-2.239-5-5-5h-48.244c-2.761 0-5 2.238-5 5v32.246c0 2.761 2.239 5 5 5h48.244c2.761 0 5-2.239 5-5v-32.246z',
        'style': f'fill:{back_fill}; fill-opacity:1',
    })

    # parte da frente do diretório, com curvas e gradiente
    ET.SubElement(group, 'path', {
        'd': 'm61.122 20.652c0-1.326-0.527-2.598-1.465-3.536-0.938-0.937-2.209-1.464-3.535-1.464h-25.58c-1.232 0-2.42-0.455-3.337-1.277-0.768-0.689-1.713-1.535-2.481-2.224-0.917-0.822-2.105-1.277-3.337-1.277h-13.509c-1.326 0-2.597 0.527-3.535 1.465-0.938 0.937-1.465 2.209-1.465 3.535v32.252c0 2.761 2.239 5 5 5h48.244c2.761 0 5-2.239 5-5v-27.474z',
        'style': f'fill:{front_fill}; fill-opacity:1'
    })

def draw_glyph(
    svg: ET.Element,
    d_contents: list[str],
    fill: str,
    requires_scale: bool,
    transform_value: str,
    gradient_transform: str,
    group_id:str = 'glyph-group'
    ):
    """
    desenha um glifo em um grupo, que deve ser posto em cima do ícone de diretório vazio
    pra isso acontecer, deve se chamar essa função APÓS a draw_directory()

    args:
        svg:
            o elemento svg principal a qual o grupo gerado por essa função deve ser adicionado
        
        d_contents:
            dados que formam o desenho do glifo, presentes no <path> que o define
            pra cada path, deve haver um d=, se for só um path, é só passar um item único pro array

        fill:
            o que deve ser usado pra preencher o glifo
            se for um gradiente deve ser passado com a formatação #(id-do-gradiente)

        group_id:
            nome/id que o grupo gerado por essa função vai ter
    """
    
    # os atributos aqui são definidos separadamente pra poder aplicar o transform só se necessário
    attributes = {
        'id': group_id,
    }
    if requires_scale:
        attributes['transform'] = transform_value
    
    group = ET.SubElement(svg, 'g', attributes)

    for d in d_contents:
        ET.SubElement(group, 'path', {
            'd': d,
            'style': f'fill:{fill}; fill-opacity:1'
        })

def handle_fill(
    hex_map: dict,
    defs: ET.SubElement,
    gradient_id: str,
    gradient_transform: str | None = None,
    gradient_units: str = 'userSpaceOnUse', # faz o gradiente ser relativo ao tamanho do documento
    first_stop_offset: float = 0, # controlam onde cadas top fica
    second_stop_offset: float = 1
    ):
    """
    define um gradiente dentro do elemento defs
    e retorna a forma certa de referenciar o mesmo
    
    args:
        hex_map:
            duas cores, já parseadas da paleta, que devem ser usadas pra criar o gradiente
            se não forem duas cores, vai ser considerado uma cor solida
            que não precisa ser realmente declarada, então só retorna a referencia certa e ela
        
        defs:
            subelemento, <defs>, onde as definições feitas por essa função devem ficar
        
        gradient_id:
            id que o gradiente gerado deve ter. isso é usado pra referenciar ele
        
        gradient_transform:
            transformações específicas (tamanho, posição etc.) pro gradiente
        
        gradient_units:
            não sei, mas funciona na maioria das vezes
        
        first_stop_offset:
            posição da primeira cor
        
        second_stop_offset:
            posição da segunda cor
    """

    # obter as cores a partir das chaves esperadas do mapa e normalizar elas
    top = hex_map.get('top')
    bottom = hex_map.get('bottom')

    top = normalize_hex_value(top)
    bottom = normalize_hex_value(bottom)

    fill = None # até o final da func deve parar de ser nulo
    if top and bottom:
        # converter os valores pra string pra não dar erro
        first_stop_offset = str(first_stop_offset)
        second_stop_offset = str(second_stop_offset)

        # definir os atributos do gradiente, adicionando o transform
        # apenas caso ele esteja presente, já que não é tão comum
        attributes = {
            'id': gradient_id,
            'x2': '1',
            'gradientUnits': gradient_units
        }
        if gradient_transform is not None:
            attributes['gradientTransform'] = gradient_transform

        # criar o gradiente e os tops que ele deve ter
        gradient = ET.SubElement(defs, 'linearGradient', attributes)
        
        ET.SubElement(gradient, 'stop', {
            'style': f'stop-color:{top}',
            'offset': first_stop_offset
        })
        
        ET.SubElement(gradient, 'stop', {
            'style': f'stop-color:{bottom}',
            'offset': second_stop_offset
        })
        
        # gradientes devem ser referenciados assim no svg
        fill = f'url(#{gradient_id})'
    elif top:
        # usa a cor pura se não tiver mais de duas
        # se assume que isso significa que não deve ser um gradiente
        fill = top
    elif bottom:
        fill = bottom

    return fill

def structure_svg(
    output_file: Path,
    hex_front: dict,
    hex_back: dict,
    hex_glyph: dict,
    glyph_d_contents: list[str] | None = None,
    glyph_requires_scale: bool = True,
    glyph_transform_value: str = DEFAULT_TRANSFORM_VALUE,
    glyph_gradient_transform: str = DEFAULT_GLYPH_GRADIENT_TRANSFORM
    ):
    """
    args:
        output_file:
            caminho completo, já construído, de onde o svg criado por essa função deve parar

        hex_front:
            paleta de cores que a frente do diretório deve ter
            ex: directory-top, directory-bottom
        
        hex_back:
            paleta de cores que o fundo do diretório deve ter
            no kora geralmente o background é sólido, mas se passar duas cores, vira gradiente
            ex: background, background-secondary
            ex: background
        
        hex_glyph:
            paleta de cores que o glifo (desenho em cima do diretório) deve ter

        glyph_d_contents:
            os conteúdos dentro da propriedade 'd=' que os <path> têm
            isso é o que define a forma do path
        
        glyph_requires_scale:
            alguns glifos do kora podem precisar de um 'transform=' no <g> que contém o glifo
            isso acontece no glifo da folder-add.svg, onde o ícone quebra se não tiver o transform aplicado
            alguns precisam, se não ficam muito pequenos, enquanto outros não precisam, se não ficam muito grandes

            se assume que a maioria que precisa disso, deve ter o valor do transform como scale(.75)
            mas podem haver casos onde o valor pode ser diferente, como o folder-locked, que usa matrix(...)

            nos ícones originais, geralmente fica no próprio glifo/o grupo que o comporta

            na maioria das vezes, scale(.75) já resolve, mas pode haver situações que um transform customizado deve ser passado
            o jeito de saber quais precisam ou não é: gerar os svgs com todos os glifos e olhar manualmente

            TODO: trocar o nome cabuloso desse argumento que dá a entender que só o scale é passável no transform

        glyph_transform_value:
            o valor que é usado quando o transform é aplicado
            pode variar de glifo pra glifo, mas a maioria, quando usa, é scale(.75)
            
            pra saber o transform apropriado pra um glifo problemático,
            se deve olhar o conteúdo de texto do svg original. lá vai ter algo como:
            <g
                transform="matrix(...)" <- esse valor é o que deve ser usado
                <path d=... style=... id=.../>
            </g>

            se o transform não estiver presente ou for simplesmente scale(0.75),
            não precisa passar nada pra esse argumento, já assume isso como valor padrão

        glyph_gradient_transform:
            se a posição/tamanho do gradiente do glifo precisar ser mudado
            geralmente acontece quando o ícone não é tão grande, o que faz o gradiente ser difícil de ver
            nos ícones originais, geralmente fica na definição do gradiente
    """
    
    # elemento <svg> principal que contém todo o conteúdo
    # todo elemento (exceto o <xml>, se presente) deve ser um subelemento daqui
    #
    # esses valores nele são o que geralmente já tem no ícone base de diretório do kora
    # ex: <svg style=x viewBox=y xmlns=z</svg>
    svg = ET.Element('svg', {
        'xmlns': 'http://www.w3.org/2000/svg',
        'viewBox': '0 0 48 48',
        'style': 'clip-rule:evenodd;fill-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2'
    })

    # definições de gradientes
    # os ids definidos aqui são os que serão passados como argumentos pras outras funções auxiliares
    defs = ET.SubElement(svg, 'defs')
    
    front_fill = handle_fill(
        hex_map=hex_front, defs=defs, gradient_id='front-gradient',
        gradient_transform='matrix(2.54933e-15,-41.6338,41.6338,2.54933e-15,445.153,52.7218)'
    )
    back_fill = handle_fill(
        hex_map=hex_back, defs=defs,
        gradient_id='back-gradient',
        gradient_units='objectBoundingBox', # usa 0-100% do objeto. sem isso, o gradiente fica muito comprimido
        first_stop_offset=0.5,              # só faz diferença nos que de fato usam gradientes como background
        second_stop_offset=1
    )
    glyph_fill = handle_fill(
        hex_map=hex_glyph, defs=defs, gradient_id='glyph-gradient',
        gradient_transform=glyph_gradient_transform,
    )
    
    # desenhar de fato os elementos, usando sempre um diretório padrão como base
    # o glifo por cima do ícone de diretório só vai ser desenhado se ele tiver sido passado
    draw_directory(
        svg=svg,
        back_fill=back_fill,
        front_fill=front_fill
    )
    
    if glyph_d_contents is not None and len(glyph_d_contents):
        draw_glyph(
            svg=svg,
            fill=glyph_fill,
            d_contents=glyph_d_contents,
            requires_scale=glyph_requires_scale,
            transform_value=glyph_transform_value,
            gradient_transform=glyph_gradient_transform
        )

    # indentar os conteúdos com x espaços, se não eles ficam todos numa linha só
    ET.indent(svg, space='  ', level=0)

    # converter pra string e escrever o xml gerado em um arquivo svg
    xml_str = ET.tostring(svg, encoding='utf-8', xml_declaration=True).decode('utf-8')
    with output_file.open('w') as f:
        f.write(xml_str)

def handle_palette(
    output_directory: Path,
    palette: dict,
    icon_name: str,
    glyph_d_contents: list[str] | None,
    glyph_requires_scale: bool,
    glyph_transform_value: str,
    glyph_gradient_transform: str
    ):
    """
    a partir de uma paleta de cores, organiza os valores dela em variáveis e os normaliza
    depois, monta os dicts/mapas de possíveis gradientes

    se duas cores do mesmo tipo (ex: glyph_top e glyph_bottom) forem localizadas,
    e se as duas NÃO forem nulas, se assume que elas devam virar um gradiente,
    mas isso é responsabilidade da handle_fill, essa é só a definição dos mapas

    após isso, constrói o caminho final do arquivo, garantindo que os diretórios existam

    args:
        output_directory:
            diretório onde o arquivo svg deve ficar, SEM O NOME DO ARQUIVO INCLUÍDO
        
        palette:
            um dicionário que contém múltiplas chaves específicas
            chaves essas que determinam cores dentro do arquivo
            ex: directory-bottom representa a cor mais escura do gradiente do ícone de diretório
        
        icon_name:
            nome do arquivo svg final

        glyph_d_contents:
            os conteúdos dentro da propriedade 'd=' que os <path> têm
            isso é o que define a forma do path. cada um deve ter um d_content
    """

    # obter os valores do mapa
    # também junta todas elas num array depois pra ficar mais fácil de normalizar
    background = palette.get('background')
    background_secondary = palette.get('background-secondary')
    directory_top = palette.get('directory-top')
    directory_bottom = palette.get('directory-bottom')
    glyph_top = palette.get('glyph-top')
    glyph_bottom = palette.get('glyph-bottom')

    variables = [background, background_secondary, directory_top, directory_bottom, glyph_top, glyph_bottom]
    for v in variables:
        v = normalize_hex_value(v)

    # organizar as cores em dicts que a função de estruturação do svg entenda
    hex_front = { 'top': directory_top, 'bottom': directory_bottom }
    hex_back =  { 'top': background,    'bottom': background_secondary }
    hex_glyph = { 'top': glyph_top,     'bottom': glyph_bottom }

    # construir + normalizar o caminho final e gerar o svg
    output_directory.mkdir(parents=True, exist_ok=True)
    final = output_directory / icon_name
    final = normalized_svg_file(final)

    structure_svg(
        output_file=final,
        hex_front=hex_front,
        hex_back=hex_back,
        hex_glyph=hex_glyph,
        glyph_d_contents=glyph_d_contents,
        glyph_requires_scale=glyph_requires_scale,
        glyph_transform_value=glyph_transform_value,
        glyph_gradient_transform=glyph_gradient_transform
    )