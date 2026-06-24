import pytest
from io import StringIO
import sys
from gerador.energia import gerar_codigo_energia


def capturar(node):
    """Captura o print do gerador e devolve lista de linhas."""
    saida = StringIO()
    sys.stdout = saida
    gerar_codigo_energia(node)
    sys.stdout = sys.__stdout__
    return [l for l in saida.getvalue().splitlines()]


class TestEnergia:
    def test_definir_limite(self):
        no = {"acao": "definir_limite_energia", "alvo": "e1", "valor": 500.0}
        assert capturar(no) == ["e1.definir_limite(500.0);"]

    def test_registrar(self):
        no = {"acao": "registrar_consumo_energia", "alvo": "e1", "valor": 10.5}
        assert capturar(no) == ["e1.registrar_consumo(10.5);"]

    def test_ler(self):
        no = {"acao": "ler_consumo_energia", "alvo": "e1"}
        assert capturar(no) == ["e1.ler_consumo();"]

    def test_resetar(self):
        no = {"acao": "resetar_consumo_energia", "alvo": "e1"}
        assert capturar(no) == ["e1.resetar_consumo();"]

    def test_alerta(self):
        no = {"acao": "alerta_energia", "mensagem": "Consumo alto"}
        assert capturar(no) == ['std::cout << "[ALERTA] Consumo alto" << std::endl;']

    def test_condicional(self):
        no = {
            "acao": "condicional_energia",
            "alvo": "e1",
            "operador": ">",
            "valor": 400.0,
            "se_verdadeiro": {"acao": "alerta_energia", "mensagem": "Limite!"},
            "se_falso":      {"acao": "resetar_consumo_energia", "alvo": "e1"},
        }
        resultado = capturar(no)
        assert resultado[0] == "if (e1.ler_consumo() > 400.0) {"
        assert resultado[1] == 'std::cout << "[ALERTA] Limite!" << std::endl;'
        assert resultado[2] == "} else {"
        assert resultado[3] == "e1.resetar_consumo();"
        assert resultado[4] == "}"

    def test_no_desconhecido(self):
        with pytest.raises(Exception, match="desconhecido"):
            gerar_codigo_energia({"acao": "inventado"})