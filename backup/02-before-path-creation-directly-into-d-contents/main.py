import d_contents as data
import colors
import xml_writer
from pathlib import Path

# definição de nomes de ícones, quais deles usam quais glifos
# esse mapa é sempre fixo
#
# de onde essas variáveis associadas às chaves vêm, elas já incluem os transforms
# e outras configurações necessárias pra cada ícone
# e se alguma transformação especial deve ser aplicada a eles
directories_rules = {
    'bookmark-missing': data.half_star,
    'folder-3dprint': data.cube_3d,
    'folder-activities': data.three_dots,
    'folder-add': data.plus,
    'folder-android': data.android,
    'folder-applications': data.capital_a,
    'folder-arduino': data.arduino,
    'folder-backup': data.arrow_cycle,
    'folder-books': data.book,
    'folder-cd': data.cd,
    'folder-copy-cloud': data.copy_cloud,
    'folder-documents': data.document,
    'folder-download': data.two_arrows_down,
    'folder-dropbox': data.dropbox,
    'folder-favorites': data.star,
    'folder-games': data.controller,
    'folder-gdrive': data.google_drive,
    'folder-go': data.go,
    'folder-gnome': data.gnome,
    'folder-git': data.git,
    'folder-github': data.github,
    'folder-gitlab': data.gitlab,
    'folder-html': data.globe,
    'folder-image': data.image,
    'folder-image-people': data.user,
    'folder-important': data.exclamation_mark,
    'folder-kde': data.kde,
    'folder-linux': data.penguin_right,
    'folder-locked': data.padlock,
    'folder-mail': data.at,
    'folder-meocloud': data.cloud,
    'folder-mega': data.mega,
    'folder-music': data.musical_note,
    'network-manager': data.wifi,
    'folder-owncloud': data.owncloud,
    'folder-pcloud': data.pcloud,
    'folder-java': data.java,
    'folder-print': data.printer,
    'folder-private': data.key,
    'folder-publicshare': data.stickman_walking,
    'folder-recent': data.clock,
    'folder-remote': data.plug,
    'folder-root': data.slash,
    'folder-saved-search': data.cog,
    'folder-script': data.dollar,
    'folder-snap': data.snap,
    'folder-steam': data.steam,
    'folder-sync': data.cycle,
    'folder-syncthing': data.syncthing,
    'folder-system': data.penguin_left,
    'folder-templates': data.template_file,
    'folder-text': data.text,
    'folder-torrent': data.torrent,
    'folder-unlocked': data.padlock_open,
    'folder-vbox': data.vbox,
    'folder-wine': data.windows,
    'folder-yandex-disk': data.yandex_disk,
    'folder-projects': data.projects,
    'user-home': data.home,
    'folder-development': data.development,
    'folder-videos': data.video_roll
}

# associa cada paleta de cor a um label
# os labels são os diretórios de output pros ícones devem ter
# ex: output/papirus/blue/<ícones de pastas azuis>
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

def main():
    """
    função que importa as paletas e organiza as regras em variáveis acessíveis
    as labels das paletas definem o caminho onde uma variação de diretórios vai ser criada
    """

    # fazer a criação dos ícones pra cada paleta definida
    for label, palette in palettes.items():
        # nas regras, obter o nome da chave (que vai ser o mesmo nome do ícone)
        # e o dicionário atrelado a esse nome, que deve ter as propriedades necessárias pra criação de um ícone
        for icon_name, properties in directories_rules.items():
            data               = properties.get('d')
            requires_scale     = properties.get('requires-scale', True) # assumir que a princípio tudo precisa de scale
            transform_value    = properties.get('transform-value', xml_writer.DEFAULT_TRANSFORM_VALUE)
            gradient_transform = properties.get('gradient-transform', xml_writer.DEFAULT_GLYPH_GRADIENT_TRANSFORM)

            # os dados do glifo (d=) podem conter apenas um path (str)
            # ou múltiplos paths que formam um glifo (list)
            # mesmo se for único, deve ser passado pras outras funções como lista
            if isinstance(data, str):
                data = [data]

            xml_writer.handle_palette(
                output_directory=Path(f'/mnt/seagate/symlinks/kde-user-icons/copycat/reserved/folder-flavors/{label}'),
                palette=palette,
                icon_name=icon_name,
                glyph_d_contents=data,
                glyph_requires_scale=requires_scale,
                glyph_transform_value=transform_value,
                glyph_gradient_transform=gradient_transform
            )

main()