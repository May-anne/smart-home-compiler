import pytest
from pathlib import Path
from lark import Lark
from lark.exceptions import UnexpectedInput

from gramatica import GRAMATICA_COMPLETA
from semantica import semantica_base
from transformer import transformer


PASTA_EXEMPLOS = Path(__file__).parents[1] / "exemplos"


def analisar(caminho):
    codigo = caminho.read_text(encoding="utf-8")
    parser = Lark(GRAMATICA_COMPLETA, parser="lalr", start="start")
    arvore = parser.parse(codigo)
    nos = transformer(arvore)

    declarados = {}
    senha_validada = {}
    for no in nos:
        semantica_base(no, declarados, senha_validada)


def test_exemplo_valido_passa_por_todas_as_analises():
    analisar(PASTA_EXEMPLOS / "exemplo_valido.shc")


def test_exemplo_de_erro_sintatico_falha_no_parse():
    caminho = PASTA_EXEMPLOS / "exemplo_erro_sintatico.shc"

    with pytest.raises(UnexpectedInput):
        analisar(caminho)


def test_exemplo_de_erro_semantico_passa_no_parse_e_falha_na_semantica():
    caminho = PASTA_EXEMPLOS / "exemplo_erro_semantico.shc"

    with pytest.raises(Exception, match="esperado"):
        analisar(caminho)
