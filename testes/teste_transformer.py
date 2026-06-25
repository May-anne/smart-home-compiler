from lark import Lark
from gramatica import GRAMATICA_COMPLETA
from transformer import transformer


def test_transformer_device_gera_dict_correto():
    parser = Lark(GRAMATICA_COMPLETA, parser="lalr")
    codigo = """
    device frigobar {
        type TERMOSTATO;
        bool ligada;
        int temperatura;
    }
    """
    tree = parser.parse(codigo)
    resultado = transformer(tree)

    assert resultado == [
        {
            "acao": "dispositivo",
            "nome": "frigobar",
            "tipo": "TERMOSTATO",
            "tipo_original": "TERMOSTATO",
            "campos": [
                {"tipo": "bool", "nome": "ligada"},
                {"tipo": "int", "nome": "temperatura"},
            ],
        }
    ]


def test_transformer_device_sem_campos_extra():
    parser = Lark(GRAMATICA_COMPLETA, parser="lalr")
    codigo = "device porta_frente { type FECHADURA; }"

    tree = parser.parse(codigo)
    resultado = transformer(tree)

    assert resultado == [
        {
            "acao": "dispositivo",
            "nome": "porta_frente",
            "tipo": "FECHADURA",
            "tipo_original": "FECHADURA",
            "campos": [],
        }
    ]