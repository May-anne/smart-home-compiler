import pytest
from lark import Lark
from gramatica import GRAMATICA_COMPLETA


@pytest.fixture
def parser():
    return Lark(GRAMATICA_COMPLETA, parser="lalr")


def test_device_simples_parseia(parser):
    codigo = """
    device porta_frente {
        type FECHADURA;
    }
    """
    tree = parser.parse(codigo)
    assert tree.data == "start"


def test_device_com_campos_extra_parseia(parser):
    codigo = """
    device frigobar {
        type TERMOSTATO;
        bool ligada;
        int temperatura;
    }
    """
    tree = parser.parse(codigo)
    assert tree.data == "start"


def test_device_sem_campos_extra_parseia(parser):
    # "type" é obrigatório, mas campos extras (bool/int/...) são opcionais
    codigo = "device sensor1 { type INTDETECTOR; }"
    tree = parser.parse(codigo)
    assert tree.data == "start"


def test_device_sem_type_falha(parser):
    # "type" é obrigatório — sem ele, o parser deve rejeitar
    codigo = "device quebrado { bool ligada; }"
    with pytest.raises(Exception):
        parser.parse(codigo)


def test_device_com_tipo_de_dispositivo_invalido_falha(parser):
    # FORNO não está em TIPO_DEVICE
    codigo = """
    device quebrado {
        type FORNO;
    }
    """
    with pytest.raises(Exception):
        parser.parse(codigo)


def test_device_com_tipo_de_campo_invalido_falha(parser):
    # "cor" não está em TIPO_CAMPO (bool/int/string/float)
    codigo = """
    device quebrado {
        type FECHADURA;
        cor algumacoisa;
    }
    """
    with pytest.raises(Exception):
        parser.parse(codigo)