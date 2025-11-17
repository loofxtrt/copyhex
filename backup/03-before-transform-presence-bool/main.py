import glyphs
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
    # 'bookmark-missing': glyphs.half_star,
    # 'folder-3dprint': glyphs.cube_3d,
    # 'folder-activities': glyphs.three_dots,
    # 'folder-add': glyphs.plus,
    # 'folder-android': glyphs.android,
    # 'folder-applications': glyphs.capital_a,
    # 'folder-arduino': glyphs.arduino,
    # 'folder-backup': glyphs.arrow_cycle,
    # 'folder-books': glyphs.book,
    # 'folder-cd': glyphs.cd,
    # 'folder-copy-cloud': glyphs.copy_cloud,
    # 'folder-documents': glyphs.document,
    # 'folder-download': glyphs.two_arrows_down,
    # 'folder-dropbox': glyphs.dropbox,
    # 'folder-favorites': glyphs.star,
    # 'folder-games': glyphs.controller,
    # 'folder-gdrive': glyphs.google_drive,
    # 'folder-go': glyphs.go,
    # 'folder-gnome': glyphs.gnome,
    # 'folder-git': glyphs.git,
    # 'folder-github': glyphs.github,
    # 'folder-gitlab': glyphs.gitlab,
    # 'folder-html': glyphs.globe,
    # 'folder-image': glyphs.image,
    # 'folder-image-people': glyphs.user,
    # 'folder-important': glyphs.exclamation_mark,
    # 'folder-kde': glyphs.kde,
    # 'folder-linux': glyphs.penguin_right,
    # 'folder-locked': glyphs.padlock,
    # 'folder-mail': glyphs.at,
    # 'folder-meocloud': glyphs.cloud,
    # 'folder-mega': glyphs.mega,
    # 'folder-music': glyphs.musical_note,
    # 'network-manager': glyphs.wifi,
    # 'folder-owncloud': glyphs.owncloud,
    # 'folder-pcloud': glyphs.pcloud,
    # 'folder-java': glyphs.java,
    # 'folder-print': glyphs.printer,
    # 'folder-private': glyphs.key,
    # 'folder-publicshare': glyphs.stickman_walking,
    # 'folder-recent': glyphs.clock,
    # 'folder-remote': glyphs.plug,
    # 'folder-root': glyphs.slash,
    # 'folder-saved-search': glyphs.cog,
    # 'folder-script': glyphs.dollar,
    # 'folder-snap': glyphs.snap,
    # 'folder-steam': glyphs.steam,
    # 'folder-sync': glyphs.cycle,
    # 'folder-syncthing': glyphs.syncthing,
    # 'folder-system': glyphs.penguin_left,
    # 'folder-templates': glyphs.template_file,
    # 'folder-text': glyphs.text,
    # 'folder-torrent': glyphs.torrent,
    # 'folder-unlocked': glyphs.padlock_open,
    'folder-vbox': glyphs.vbox,
    # 'folder-wine': glyphs.windows,
    # 'folder-yandex-disk': glyphs.yandex_disk,
    # 'folder-projects': glyphs.projects,
    # 'user-home': glyphs.home,
    # 'folder-development': glyphs.development,
    'folder-videos': glyphs.video_roll
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
        for icon_name, glyph in directories_rules.items():
            xml_writer.handle_palette(
                #output_directory=Path(f'/mnt/seagate/symlinks/kde-user-icons/copycat/reserved/folder-flavors/{label}'),
                output_directory=Path(f'./output/{label}'),
                palette=palette,
                icon_name=icon_name,
                glyph=glyph
            )

main()