import pytest
from lark import Lark
from gramatica.base import GRAMATICA_COMPLETA


linhas = GRAMATICA_COMPLETA.split("\n")
for i, linha in enumerate(linhas, start=1):
    if 58 <= i <= 68:
        print(f"{i}: {linha}")

@pytest.fixture
def parser():
    return Lark(GRAMATICA_COMPLETA, parser="lalr")


def test_device_simples_parseia(parser):
    codigo = """
    device Fechadura {
        bool ligada;
        int temperatura;
    }
    """
    tree = parser.parse(codigo)
    assert tree.data == "start"


def test_device_sem_campos_parseia(parser):
    codigo = "device Vazio { }"
    tree = parser.parse(codigo)
    assert tree.data == "start"


def test_device_com_tipo_invalido_falha(parser):
    codigo = """
    device Quebrado {
        cor algumacoisa;
    }
    """
    with pytest.raises(Exception):
        parser.parse(codigo)