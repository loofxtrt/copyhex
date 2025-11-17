import ast
import pathlib
import json

def indent(text, level=1):
    pad = " " * 4 * level
    return "".join(pad + linha if linha.strip() else linha
                   for linha in text.splitlines(True))


def dict_to_code(d, level=0):
    if isinstance(d, dict):
        itens = []
        for k, v in d.items():
            itens.append(f"'{k}': {dict_to_code(v, level+1)}")
        inner = ",\n".join(indent(i, 1) for i in itens)
        return "{\n" + inner + "\n" + " " * 4 * level + "}"
    elif isinstance(d, list):
        itens = []
        for v in d:
            itens.append(dict_to_code(v, level+1))
        inner = ",\n".join(indent(i, 1) for i in itens)
        return "[\n" + inner + "\n" + " " * 4 * level + "]"
    else:
        return repr(d)


def converter_glifo(valor):
    if not isinstance(valor, dict):
        return None

    novo = {}
    paths = [{}]

    if 'd' in valor:
        paths[0]['d'] = valor['d']
    else:
        return None

    if 'transform-value' in valor:
        novo['transform'] = valor['transform-value']

    if 'gradient-transform' in valor:
        novo['gradient-transform'] = valor['gradient-transform']

    novo['paths'] = paths
    return novo


def processar_arquivo(caminho):
    caminho = pathlib.Path(caminho)
    codigo = caminho.read_text(encoding='utf-8')

    modulo = ast.parse(codigo)
    novos = {}

    for node in modulo.body:
        if isinstance(node, ast.Assign):
            for alvo in node.targets:
                if isinstance(alvo, ast.Name):
                    nome = alvo.id
                    try:
                        valor = ast.literal_eval(node.value)
                        convertido = converter_glifo(valor)
                        if convertido is not None:
                            novos[nome] = convertido
                    except Exception:
                        pass

    linhas = []
    linhas.append("import xml.etree.ElementTree as ET\n\n")

    for nome, dic in novos.items():
        linhas.append(f"{nome} = {dict_to_code(dic)}\n\n")

    novo_arquivo = caminho.with_name(caminho.stem + "_converted.py")
    novo_arquivo.write_text("".join(linhas), encoding='utf-8')
    print("arquivo gerado:", novo_arquivo)


if __name__ == "__main__":
    processar_arquivo("d_contents_old.py")
