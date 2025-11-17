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
    'folder': None,
    'bookmark-missing': glyphs.half_star,
    #'folder-3dprint': glyphs._3dprint,
    'folder-activities': glyphs.activities,
    'folder-add': glyphs.add,
    'folder-android': glyphs.android,
    'folder-applications': glyphs.applications,
    'folder-arduino': glyphs.arduino,
    'folder-backup': glyphs.backup,
    'folder-books': glyphs.books,
    'folder-cd': glyphs.cd,
    'folder-copy-cloud': glyphs.copy_cloud,
    'folder-documents': glyphs.documents,
    'folder-download': glyphs.downloads,
    'folder-dropbox': glyphs.dropbox,
    'folder-favorites': glyphs.star,
    'folder-games': glyphs.games,
    'folder-gdrive': glyphs.google_drive,
    #'folder-go': glyphs.go,
    'folder-gnome': glyphs.gnome,
    'folder-git': glyphs.git,
    'folder-github': glyphs.github,
    'folder-gitlab': glyphs.gitlab,
    'folder-html': glyphs.globe,
    'folder-image': glyphs.image,
    'folder-image-people': glyphs.image_people,
    'folder-important': glyphs.important,
    'folder-kde': glyphs.kde,
    'folder-linux': glyphs.linux,
    'folder-locked': glyphs.locked,
    'folder-mail': glyphs.mail,
    'folder-meocloud': glyphs.cloud,
    'folder-mega': glyphs.mega,
    'folder-music': glyphs.music,
    'network-manager': glyphs.network,
    'folder-owncloud': glyphs.owncloud,
    'folder-pcloud': glyphs.pcloud,
    'folder-java': glyphs.java,
    'folder-print': glyphs._print,
    'folder-private': glyphs.private,
    'folder-publicshare': glyphs.publicshare,
    'folder-recent': glyphs.recent,
    'folder-remote': glyphs.remote,
    'folder-root': glyphs.root,
    'folder-saved-search': glyphs.saved_search,
    'folder-script': glyphs.script,
    'folder-snap': glyphs.snap,
    'folder-steam': glyphs.steam,
    'folder-sync': glyphs.sync,
    'folder-syncthing': glyphs.syncthing,
    'folder-system': glyphs.system,
    'folder-templates': glyphs.templates,
    'folder-text': glyphs.text,
    'folder-torrent': glyphs.torrent,
    'folder-unlocked': glyphs.unlocked,
    'folder-vbox': glyphs.vbox,
    'folder-wine': glyphs.wine,
    'folder-yandex-disk': glyphs.yandex_disk,
    'folder-projects': glyphs.projects,
    'user-home': glyphs.home,
    'folder-development': glyphs.development,
    'folder-videos': glyphs.videos,
    'folder-pictures': glyphs.pictures,
    'user-share': glyphs.user_share,
    'folder-tar': glyphs.tar,
    'folder-nextcloud': glyphs.nextcloud,
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
                output_directory=Path(f'/mnt/seagate/symlinks/kde-user-icons/copycat/reserved/folder-flavors/{label}'),
                #output_directory=Path(f'./output/{label}'),
                palette=palette,
                icon_name=icon_name,
                glyph=glyph
            )

main()