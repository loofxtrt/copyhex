import d_contents as data
import colors
import xml_writer
from pathlib import Path

# definição de nomes de ícones, quais deles usam quais glifos
# e se alguma transformação especial deve ser aplicada a eles
#
# se assume que se requires-scale não for explicitamente false, é pq é true
# se um ícone do kora for repetido, só precisa referenciar a mesma var do data, não criar outro ícone idêntico
#
# transform-value = transform pro grupo inteiro do glifo
# gradient-transform = transform aplicado só ao gradiente do glifo
#
# esse mapa é sempre fixo
directories_rules = {
    'bookmark-missing': {
        'glyph': data.half_star
    },
    'folder-3dprint': {
        'glyph': data.cube_3d,
        'requires-scale': False
    },
    'folder-activities': {
        'glyph': data.three_dots,
        'transform-value': 'translate(0 .8933)'
    },
    'folder-add': {
        'glyph': data.plus
    },
    'folder-android': {
        'glyph': data.android,
        'requires-scale': False
    },
    'folder-applications': {
        'glyph': data.capital_a,
        'transform-value': 'matrix(1.32032,0,0,1.17497,-11.3269,-6.98679)'
    },
    'folder-arduino': {
        'glyph': data.arduino,
        'requires-scale': False
    },
    'folder-backup': {
        'glyph': data.arrow_cycle,
        'requires-scale': False
    },
    'folder-books': {
        'glyph': data.book,
        'requires-scale': False
    },
    'folder-cd': {
        'glyph': data.cd,
        'transform-value': 'translate(0 -4.10918)'
    },
    'folder-copy-cloud': {
        'glyph': data.copy_cloud,
        'transform-value': 'matrix(.562491 0 0 .562491 5.66523 5.12787)'
    },
    'folder-documents': {
        'glyph': data.document,
        'requires-scale': False
    },
    'folder-download': {
        'glyph': data.two_arrows_down
    },
    'folder-dropbox': {
        'glyph': data.dropbox
    },
    'folder-favorites': {
        'glyph': data.star
    },
    'folder-games': {
        'glyph': data.controller
    },
    'folder-gdrive': {
        'glyph': data.google_drive
    },
    'folder-go': {
        'glyph': data.go,
        'requires-scale': False
    },
    'folder-gnome': {
        'glyph': data.gnome
    },
    'folder-git': {
        'glyph': data.git    
    },
    'folder-github': {
        'glyph': data.github
    },
    'folder-gitlab': {
        'glyph': data.gitlab
    },
    'folder-html': {
        'glyph': data.globe
    },
    'folder-image': {
        'glyph': data.image
    },
    'folder-image-people': {
        'glyph': data.user
    },
    'folder-important': {
        'glyph': data.exclamation_mark
    },
    'folder-kde': {
        'glyph': data.kde,
        'requires-scale': False
    },
    'folder-linux': {
        'glyph': data.penguin_right
    },
    'folder-locked': {
        'glyph': data.padlock,
        'transform-value': 'matrix(1.1972,0,0,1.1972,14.4224,15.3118)',
        'gradient-transform': 'matrix(0 13.9999 -16.5009 0 -718.435 .999812)'
    },
    'folder-mail': {
        'glyph': data.at
    },
    'folder-meocloud': {
        'glyph': data.cloud,
    },
    'folder-mega': {
        'glyph': data.mega
    },
    'folder-music': {
        'glyph': data.musical_note
    },
    'network-manager': {
        'glyph': data.wifi
    },
    'folder-owncloud': {
        'glyph': data.owncloud
    },
    'folder-pcloud': {
        'glyph': data.pcloud
    },
    'folder-java': {
        'glyph': data.java
    },
    #'folder-pictures': {
    #    'glyph': data.camera
    #},
    'folder-print': {
        'glyph': data.printer
    },
    'folder-private': {
        'glyph': data.key
    },
    'folder-publicshare': {
        'glyph': data.stickman_walking,
        'requires-scale': False
    },
    'folder-recent': {
        'glyph': data.clock
    },
    'folder-remote': {
        'glyph': data.plug
    },
    'folder-root': {
        'glyph': data.slash
    },
    'folder-saved-search': {
        'glyph': data.cog
    },
    'folder-script': {
        'glyph': data.dollar
    },
    'folder-snap': {
        'glyph': data.snap,
        'requires-scale': False
    },
    'folder-steam': {
        'glyph': data.steam
    },
    'folder-sync': {
        'glyph': data.cycle,
        'transform-value': 'matrix(1.19103,0,0,1.19103,-4.58469,-9.17259)'
    },
    'folder-syncthing': {
        'glyph': data.syncthing,
        'requires-scale': False
    },
    'folder-system': {
        'glyph': data.penguin_left
    },
    'folder-templates': {
        'glyph': data.template_file,
        'requires-scale': False
    },
    'folder-text': {
        'glyph': data.text
    },
    'folder-torrent': {
        'glyph': data.torrent
    },
    'folder-unlocked': {
        'glyph': data.padlock_open,
        'transform-value': 'matrix(1.1972,0,0,1.1972,14.4224,15.3118)',
        'gradient-transform': 'matrix(0 13.9999 -16.5009 0 -718.435 .999812)'
    },
    'folder-vbox': {
        'glyph': data.vbox
    },
    'folder-wine': {
        'glyph': data.windows
    },
    'folder-yandex-disk': {
        'glyph': data.yandex_disk
    },
    'folder-projects': {
        'glyph': data.projects,
        'transform-value': 'matrix(0.82391613,0,0,0.82391613,-1.9533582,-6.4670396)', # decidido editando manualmente o svg
        'gradient-transform': 'matrix(0,29.0579,-29.0579,0,-583.701,19.4233)'
    },
    'user-home': {
        'glyph': data.home
    },
    'folder-development': {
        'glyph': data.development
    }
}

def main():
    """
    função que importa as paletas e organiza as regras em variáveis acessíveis
    as labels das paletas definem o caminho onde uma variação de diretórios vai ser criada
    """

    palettes = {
        'kora/blue': colors.blue,
        'kora/yellow': colors.yellow,
        'papirus/breeze': colors.breeze,
        'papirus/brown': colors.brown,
        #'papirus/carmine': colors.carmine,
        'papirus/violet': colors.violet,
        'papirus/red': colors.red,
        'papirus/indigo': colors.indigo,
        'papirus/yellow': colors.papirus_yellow,
        'papirus/pale-brown': colors.pale_brown,
        'papirus/yaru': colors.yaru,
    }

    # label é o nome que o diretório de output vai ter
    # ex:
    #   output/blue/<ícones de pastas azuis>
    #   output/papirus/blue/<ícones de pastas azuis>
    #
    # p são os mapas de cores em si
    for label, palette in palettes.items():
        # obter o nome da chave (que vai ser o mesmo do arquivo)
        # e o dicionário atrelado a esse nome com as propriedades necessárias pra criação de um ícone
        for name, properties in directories_rules.items():
            glyph_data         = properties.get('glyph')
            requires_scale     = properties.get('requires-scale', True) # assumir que a princípio tudo precisa de scale
            transform_value    = properties.get('transform-value', xml_writer.DEFAULT_TRANSFORM_VALUE)
            gradient_transform = properties.get('gradient-transform', xml_writer.DEFAULT_GLYPH_GRADIENT_TRANSFORM)

            # os dados do glifo podem conter apenas um path (str)
            # ou múltiplos paths que formam um glifo (list)
            # mesmo se for único, deve ser passado pras outras funções como lista
            if isinstance(glyph_data, str):
                glyph_data = [glyph_data]

            xml_writer.handle_palette(
                output_directory=Path(f'./output/{label}'),
                palette=palette,
                icon_name=name,
                glyph_d_contents=glyph_data,
                glyph_requires_scale=requires_scale,
                glyph_transform_value=transform_value,
                glyph_gradient_transform=gradient_transform
            )

main()