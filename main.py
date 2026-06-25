import json
import sys
from pathlib import Path

from lark import Lark

from gerador.gerador import gerar_programa
from gramatica import GRAMATICA_COMPLETA
from semantica import semantica_base
from transformer import transformer


# Altere este valor para: "valido", "erro_sintatico" ou "erro_semantico".
EXEMPLO_ATIVO = "valido"

ARQUIVOS_EXEMPLO = {
    "valido": "exemplo_valido.shc",
    "erro_sintatico": "exemplo_erro_sintatico.shc",
    "erro_semantico": "exemplo_erro_semantico.shc",
}


def carregar_codigo_fonte():
    if EXEMPLO_ATIVO not in ARQUIVOS_EXEMPLO:
        opcoes = ", ".join(ARQUIVOS_EXEMPLO)
        raise ValueError(
            f"Exemplo '{EXEMPLO_ATIVO}' desconhecido. Opções: {opcoes}."
        )

    caminho = Path(__file__).parent / "exemplos" / ARQUIVOS_EXEMPLO[EXEMPLO_ATIVO]
    return caminho, caminho.read_text(encoding="utf-8")


def sep(titulo):
    print(f"\n{'='*60}\n  {titulo}\n{'='*60}")


def main():
    try:
        caminho_fonte, codigo_fonte = carregar_codigo_fonte()
    except (OSError, ValueError) as e:
        print(f"[ERRO - Código fonte] {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Exemplo selecionado: {EXEMPLO_ATIVO}")
    print(f"Arquivo: {caminho_fonte}")

    sep("1. PARSE")
    parser = Lark(GRAMATICA_COMPLETA, parser="lalr", start="start")
    try:
        tree = parser.parse(codigo_fonte)
    except Exception as e:
        print(f"[ERRO - Parse] {e}", file=sys.stderr)
        sys.exit(1)
    print(tree.pretty())

    sep("2. AST (após transformer)")
    try:
        nos = transformer(tree)
    except Exception as e:
        print(f"[ERRO - Transformer] {e}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(nos, indent=2, ensure_ascii=False))

    sep("3. ANÁLISE SEMÂNTICA")
    declarados = {}
    senha_validada = {}
    try:
        for no in nos:
            semantica_base(no, declarados, senha_validada)
    except Exception as e:
        print(f"[ERRO - Semântica] {e}", file=sys.stderr)
        sys.exit(1)
    print("Dispositivos declarados:")
    for nome, tipo in declarados.items():
        print(f"  {nome}: {tipo}")

    sep("4. CÓDIGO C++ GERADO")
    try:
        codigo_cpp = gerar_programa(nos, declarados)
    except Exception as e:
        print(f"[ERRO - Gerador] {e}", file=sys.stderr)
        sys.exit(1)
    print(codigo_cpp)


if __name__ == "__main__":
    main()
