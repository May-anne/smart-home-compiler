import pytest
from semantica import semantica_base, validar_campos_extra, TIPOS_FIXOS_CONHECIDOS


def test_campo_duplicado_falha():
    node = {
        "acao": "dispositivo",
        "nome": "frigobar",
        "tipo": "TERMOSTATO",
        "campos": [
            {"tipo": "bool", "nome": "ligada"},
            {"tipo": "int", "nome": "ligada"},  # repetido!
        ],
    }
    with pytest.raises(Exception, match="duplicado"):
        validar_campos_extra(node)


def test_tipo_de_campo_invalido_falha():
    node = {
        "acao": "dispositivo",
        "nome": "frigobar",
        "tipo": "TERMOSTATO",
        "campos": [{"tipo": "cor", "nome": "algumacoisa"}],
    }
    with pytest.raises(Exception, match="desconhecido"):
        validar_campos_extra(node)


def test_dispositivo_de_tipo_nao_conhecido_falha():
    declarados = {}
    node = {"acao": "dispositivo", "nome": "frigobar", "tipo": "GELADEIRA", "campos": []}

    with pytest.raises(Exception, match="desconhecido"):
        semantica_base(node, declarados)


def test_dispositivo_de_tipo_fixo_funciona():
    declarados = {}
    node = {"acao": "dispositivo", "nome": "porta1", "tipo": "FECHADURA", "campos": []}

    semantica_base(node, declarados)

    assert declarados["porta1"] == "FECHADURA"


def test_dispositivo_com_campos_extra_funciona():
    declarados = {}
    node = {
        "acao": "dispositivo",
        "nome": "frigobar",
        "tipo": "TERMOSTATO",
        "campos": [
            {"tipo": "bool", "nome": "ligada"},
            {"tipo": "int", "nome": "temperatura"},
        ],
    }

    semantica_base(node, declarados)

    assert declarados["frigobar"] == "TERMOSTATO"


def test_dispositivo_duplicado_falha():
    declarados = {"porta1": "FECHADURA"}
    node = {"acao": "dispositivo", "nome": "porta1", "tipo": "FECHADURA", "campos": []}

    with pytest.raises(Exception, match="já foi declarado"):
        semantica_base(node, declarados)