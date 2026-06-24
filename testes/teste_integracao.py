import pytest
from lark import Lark
from gramatica import GRAMATICA_COMPLETA
from transformer import transformer
from semantica import semantica_base


def test_pipeline_completo_device_com_campos_extra():
    parser = Lark(GRAMATICA_COMPLETA, parser="lalr")
    codigo = """
    device frigobar {
        type TERMOSTATO;
        bool ligada;
        int temperatura;
    }
    """

    tree = parser.parse(codigo)
    nodes = transformer(tree)

    declarados = {}
    for node in nodes:
        semantica_base(node, declarados)

    assert declarados["frigobar"] == "TERMOSTATO"


def test_pipeline_completo_device_sem_campos_extra():
    parser = Lark(GRAMATICA_COMPLETA, parser="lalr")
    codigo = "device porta_frente { type FECHADURA; }"

    tree = parser.parse(codigo)
    nodes = transformer(tree)

    declarados = {}
    for node in nodes:
        semantica_base(node, declarados)

    assert declarados["porta_frente"] == "FECHADURA"


def test_pipeline_completo_falha_com_tipo_nao_conhecido():
    # GELADEIRA não está em TIPOS_FIXOS_CONHECIDOS / TIPO_DEVICE
    parser = Lark(GRAMATICA_COMPLETA, parser="lalr")
    codigo = "device frigobar { type GELADEIRA; }"

    with pytest.raises(Exception):
        parser.parse(codigo)  # já falha na gramática: GELADEIRA não é TIPO_DEVICE válido


def test_pipeline_completo_multiplos_devices():
    parser = Lark(GRAMATICA_COMPLETA, parser="lalr")
    codigo = """
    device porta_frente { type FECHADURA; }
    device frigobar { type TERMOSTATO; bool ligada; }
    device sensor1 { type INTDETECTOR; }
    """

    tree = parser.parse(codigo)
    nodes = transformer(tree)

    declarados = {}
    for node in nodes:
        semantica_base(node, declarados)

    assert declarados == {
        "porta_frente": "FECHADURA",
        "frigobar": "TERMOSTATO",
        "sensor1": "INTDETECTOR",
    }


def test_pipeline_completo_falha_com_dispositivo_duplicado():
    parser = Lark(GRAMATICA_COMPLETA, parser="lalr")
    codigo = """
    device porta_frente { type FECHADURA; }
    device porta_frente { type FECHADURA; }
    """

    tree = parser.parse(codigo)
    nodes = transformer(tree)

    declarados = {}
    with pytest.raises(Exception, match="já foi declarado"):
        for node in nodes:
            semantica_base(node, declarados)