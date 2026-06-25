import pytest
from gerador.gerador import gerar_programa


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

DECLARADOS = {
    "fechadura1":  "FECHADURA",
    "termostato1": "TERMOSTATO",
    "dimmer1":     "DIMMER",
    "detector1":   "INTDETECTOR",
    "agua1":       "MEDIDOR_AGUA",
    "energia1":    "MEDIDOR_ENERGIA",
}

# Nós de dispositivo agora carregam "tipo_original" (preenchido pelo transformer).
# A semântica sobrescreve "tipo" para "void"; o gerador lê "tipo_original".
NOS_DISPOSITIVOS = [
    {"acao": "dispositivo", "nome": "fechadura1",  "tipo": "void", "tipo_original": "FECHADURA",       "campos": []},
    {"acao": "dispositivo", "nome": "termostato1", "tipo": "void", "tipo_original": "TERMOSTATO",      "campos": []},
    {"acao": "dispositivo", "nome": "dimmer1",     "tipo": "void", "tipo_original": "DIMMER",          "campos": []},
    {"acao": "dispositivo", "nome": "detector1",   "tipo": "void", "tipo_original": "INTDETECTOR",     "campos": []},
    {"acao": "dispositivo", "nome": "agua1",       "tipo": "void", "tipo_original": "MEDIDOR_AGUA",    "campos": []},
    {"acao": "dispositivo", "nome": "energia1",    "tipo": "void", "tipo_original": "MEDIDOR_ENERGIA", "campos": []},
]


# ---------------------------------------------------------------------------
# Dispositivos
# ---------------------------------------------------------------------------

def test_gerar_dispositivo_fechadura():
    codigo = gerar_programa(
        [{"acao": "dispositivo", "nome": "porta", "tipo": "void", "tipo_original": "FECHADURA", "campos": []}],
        DECLARADOS,
    )
    assert "Fechadura porta;" in codigo


def test_gerar_dispositivo_termostato():
    codigo = gerar_programa(
        [{"acao": "dispositivo", "nome": "t1", "tipo": "void", "tipo_original": "TERMOSTATO", "campos": []}],
        DECLARADOS,
    )
    assert "Termostato t1;" in codigo


def test_gerar_dispositivo_dimmer():
    codigo = gerar_programa(
        [{"acao": "dispositivo", "nome": "d1", "tipo": "void", "tipo_original": "DIMMER", "campos": []}],
        DECLARADOS,
    )
    assert "Dimmer d1;" in codigo


def test_gerar_dispositivo_intdetector():
    codigo = gerar_programa(
        [{"acao": "dispositivo", "nome": "det1", "tipo": "void", "tipo_original": "INTDETECTOR", "campos": []}],
        DECLARADOS,
    )
    assert "DetectorIntrusao det1;" in codigo


def test_gerar_dispositivo_medidor_agua():
    codigo = gerar_programa(
        [{"acao": "dispositivo", "nome": "ag1", "tipo": "void", "tipo_original": "MEDIDOR_AGUA", "campos": []}],
        DECLARADOS,
    )
    assert "MedidorAgua ag1;" in codigo


def test_gerar_dispositivo_medidor_energia():
    codigo = gerar_programa(
        [{"acao": "dispositivo", "nome": "en1", "tipo": "void", "tipo_original": "MEDIDOR_ENERGIA", "campos": []}],
        DECLARADOS,
    )
    assert "MedidorEnergia en1;" in codigo


def test_gerar_dispositivo_sem_tipo_original_levanta_erro():
    # Sem "tipo_original" o gerador deve levantar ValueError explícito.
    with pytest.raises(ValueError, match="tipo_original"):
        gerar_programa(
            [{"acao": "dispositivo", "nome": "x", "tipo": "void", "campos": []}],
            DECLARADOS,
        )


def test_gerar_dispositivo_tipo_desconhecido_levanta_erro():
    with pytest.raises(ValueError, match="desconhecido"):
        gerar_programa(
            [{"acao": "dispositivo", "nome": "x", "tipo": "void", "tipo_original": "GELADEIRA", "campos": []}],
            DECLARADOS,
        )


# ---------------------------------------------------------------------------
# Fechadura
# ---------------------------------------------------------------------------

def test_gerar_informar_senha_fechadura():
    codigo = gerar_programa(
        [{"acao": "informar_senha_fechadura", "nome": "fechadura1", "senha": "1234"}],
        DECLARADOS,
    )
    assert 'fechadura1.informarSenha("1234");' in codigo


def test_gerar_trancar():
    codigo = gerar_programa(
        [{"acao": "trancar", "nome": "fechadura1"}],
        DECLARADOS,
    )
    assert "fechadura1.trancar();" in codigo


def test_gerar_destrancar():
    # "destrancar" não usa mais o campo "led" — apenas emite a chamada de método.
    codigo = gerar_programa(
        [{"acao": "destrancar", "nome": "fechadura1"}],
        DECLARADOS,
    )
    assert "fechadura1.destrancar();" in codigo


def test_gerar_alerta_fechadura():
    # "alerta" não usa mais o campo "led" — emite std::cout com mensagem fixa.
    codigo = gerar_programa(
        [{"acao": "alerta"}],
        DECLARADOS,
    )
    assert "[FECHADURA]" in codigo


# ---------------------------------------------------------------------------
# Temperatura
# ---------------------------------------------------------------------------

def test_gerar_definir_temperatura():
    codigo = gerar_programa(
        [{"acao": "definir_temperatura", "alvo": "termostato1", "valor": 22}],
        DECLARADOS,
    )
    assert "termostato1.setTemperatura(22);" in codigo


def test_gerar_ler_temperatura():
    codigo = gerar_programa(
        [{"acao": "ler_temperatura", "alvo": "termostato1"}],
        DECLARADOS,
    )
    assert "termostato1.lerTemperatura();" in codigo


def test_gerar_alerta_temperatura():
    codigo = gerar_programa(
        [{"acao": "alerta_temperatura", "mensagem": "Temp alta"}],
        DECLARADOS,
    )
    assert "[TEMP]" in codigo
    assert "Temp alta" in codigo


# ---------------------------------------------------------------------------
# Luminosidade
# ---------------------------------------------------------------------------

def test_gerar_definir_luminosidade():
    codigo = gerar_programa(
        [{"acao": "definir_luminosidade", "alvo": "dimmer1", "valor": 75}],
        DECLARADOS,
    )
    assert "dimmer1.setLuminosidade(75);" in codigo


def test_gerar_ler_luminosidade():
    codigo = gerar_programa(
        [{"acao": "ler_luminosidade", "alvo": "dimmer1"}],
        DECLARADOS,
    )
    assert "dimmer1.lerLuminosidade();" in codigo


def test_gerar_alerta_luminosidade():
    codigo = gerar_programa(
        [{"acao": "alerta_luminosidade", "mensagem": "Luz baixa"}],
        DECLARADOS,
    )
    assert "[LUZ]" in codigo
    assert "Luz baixa" in codigo


# ---------------------------------------------------------------------------
# Detector de intrusão
# ---------------------------------------------------------------------------

def test_gerar_configurar_detector():
    codigo = gerar_programa(
        [{"acao": "configurar_detector", "alvo": "detector1", "timeout": 30, "codigo": "ABC123"}],
        DECLARADOS,
    )
    assert 'detector1.configurar(30, "ABC123");' in codigo


def test_gerar_armar_detector():
    codigo = gerar_programa(
        [{"acao": "armar_detector", "alvo": "detector1"}],
        DECLARADOS,
    )
    assert "detector1.armar();" in codigo


def test_gerar_desarmar_detector():
    codigo = gerar_programa(
        [{"acao": "desarmar_detector", "alvo": "detector1"}],
        DECLARADOS,
    )
    assert "detector1.desarmar();" in codigo


def test_gerar_detectar_presenca():
    codigo = gerar_programa(
        [{"acao": "detectar_presenca", "alvo": "detector1"}],
        DECLARADOS,
    )
    assert "detector1.detectarPresenca();" in codigo


def test_gerar_informar_senha_intdetector():
    codigo = gerar_programa(
        [{"acao": "informar_senha", "alvo": "detector1", "senha": "9999"}],
        DECLARADOS,
    )
    assert 'detector1.informarSenha("9999");' in codigo


def test_gerar_timeout_expirado():
    codigo = gerar_programa(
        [{"acao": "timeout_expirado", "alvo": "detector1"}],
        DECLARADOS,
    )
    assert "detector1.timeoutExpirado();" in codigo


def test_gerar_disparar_alarme():
    codigo = gerar_programa(
        [{"acao": "disparar_alarme", "alvo": "detector1"}],
        DECLARADOS,
    )
    assert "detector1.dispararAlarme();" in codigo


def test_gerar_definir_hora_funcionamento():
    codigo = gerar_programa(
        [{"acao": "definir_hora_funcionamento", "alvo": "detector1",
          "hora_inicio": "08:00", "hora_fim": "18:00"}],
        DECLARADOS,
    )
    assert 'detector1.setHorario("08:00", "18:00");' in codigo


# ---------------------------------------------------------------------------
# Energia
# ---------------------------------------------------------------------------

def test_gerar_definir_limite_energia():
    codigo = gerar_programa(
        [{"acao": "definir_limite_energia", "alvo": "energia1", "valor": 500}],
        DECLARADOS,
    )
    assert "energia1.setLimite(500);" in codigo


def test_gerar_registrar_consumo_energia():
    codigo = gerar_programa(
        [{"acao": "registrar_consumo_energia", "alvo": "energia1", "valor": 120}],
        DECLARADOS,
    )
    assert "energia1.registrarConsumo(120);" in codigo


def test_gerar_ler_consumo_energia():
    codigo = gerar_programa(
        [{"acao": "ler_consumo_energia", "alvo": "energia1"}],
        DECLARADOS,
    )
    assert "energia1.lerConsumo();" in codigo


def test_gerar_resetar_consumo_energia():
    codigo = gerar_programa(
        [{"acao": "resetar_consumo_energia", "alvo": "energia1"}],
        DECLARADOS,
    )
    assert "energia1.resetarConsumo();" in codigo


def test_gerar_alerta_energia():
    codigo = gerar_programa(
        [{"acao": "alerta_energia", "mensagem": "Limite proximo"}],
        DECLARADOS,
    )
    assert "[ENERGIA]" in codigo
    assert "Limite proximo" in codigo


# ---------------------------------------------------------------------------
# Água
# ---------------------------------------------------------------------------

def test_gerar_definir_limite_agua():
    codigo = gerar_programa(
        [{"acao": "definir_limite_agua", "alvo": "agua1", "valor": 300}],
        DECLARADOS,
    )
    assert "agua1.setLimite(300);" in codigo


def test_gerar_registrar_consumo_agua():
    codigo = gerar_programa(
        [{"acao": "registrar_consumo_agua", "alvo": "agua1", "valor": 80}],
        DECLARADOS,
    )
    assert "agua1.registrarConsumo(80);" in codigo


def test_gerar_ler_consumo_agua():
    codigo = gerar_programa(
        [{"acao": "ler_consumo_agua", "alvo": "agua1"}],
        DECLARADOS,
    )
    assert "agua1.lerConsumo();" in codigo


def test_gerar_resetar_consumo_agua():
    codigo = gerar_programa(
        [{"acao": "resetar_consumo_agua", "alvo": "agua1"}],
        DECLARADOS,
    )
    assert "agua1.resetarConsumo();" in codigo


def test_gerar_alerta_agua():
    codigo = gerar_programa(
        [{"acao": "alerta_agua", "mensagem": "Consumo alto"}],
        DECLARADOS,
    )
    assert "[AGUA]" in codigo
    assert "Consumo alto" in codigo


# ---------------------------------------------------------------------------
# Condicional
# ---------------------------------------------------------------------------

def test_gerar_condicional_numerica_temperatura():
    no = {
        "acao": "condicional",
        "alvo": "termostato1",
        "comparador": ">",
        "valor": {"tipo": "numero", "valor": 30},
        "se": [
            {"acao": "alerta_temperatura", "mensagem": "Muito quente"},
            {"acao": "definir_temperatura", "alvo": "termostato1", "valor": 20},
        ],
        "senao": [
            {"acao": "definir_temperatura", "alvo": "termostato1", "valor": 25},
        ],
    }
    codigo = gerar_programa([no], DECLARADOS)
    assert "termostato1.getTemperatura() > 30" in codigo
    assert "setTemperatura(20)" in codigo
    assert "setTemperatura(25)" in codigo


def test_gerar_condicional_numerica_energia():
    no = {
        "acao": "condicional",
        "alvo": "energia1",
        "comparador": ">=",
        "valor": {"tipo": "numero", "valor": 400},
        "se":    [{"acao": "alerta_energia", "mensagem": "Limite de energia proximo"}],
        "senao": [{"acao": "ler_consumo_energia", "alvo": "energia1"}],
    }
    codigo = gerar_programa([no], DECLARADOS)
    assert "energia1.getConsumo() >= 400" in codigo


def test_gerar_condicional_string_fechadura():
    no = {
        "acao": "condicional",
        "alvo": "fechadura1",
        "comparador": "==",
        "valor": {"tipo": "string", "valor": "fechado"},
        "se":    [{"acao": "alerta"}],
        "senao": [{"acao": "trancar", "nome": "fechadura1"}],
    }
    codigo = gerar_programa([no], DECLARADOS)
    assert 'fechadura1.getEstado() == "fechado"' in codigo


def test_gerar_condicional_sem_declarados_levanta_erro():
    # Sem declarados o gerador não consegue resolver o método do alvo.
    no = {
        "acao": "condicional",
        "alvo": "termostato1",
        "comparador": ">",
        "valor": {"tipo": "numero", "valor": 30},
        "se":    [{"acao": "alerta_temperatura", "mensagem": "quente"}],
        "senao": [{"acao": "alerta_temperatura", "mensagem": "ok"}],
    }
    with pytest.raises(ValueError, match="declarados"):
        gerar_programa([no], declarados=None)


# ---------------------------------------------------------------------------
# Nó desconhecido
# ---------------------------------------------------------------------------

def test_gerar_no_desconhecido_levanta_erro():
    with pytest.raises(ValueError, match="desconhecido"):
        gerar_programa([{"acao": "acao_inexistente"}], DECLARADOS)


# ---------------------------------------------------------------------------
# Estrutura do programa gerado
# ---------------------------------------------------------------------------

def test_gerar_programa_inclui_cabecalho():
    codigo = gerar_programa([], DECLARADOS)
    assert '#include "SmartHome.h"' in codigo
    assert "#include <iostream>" in codigo
    assert "int main()" in codigo
    assert "return 0;" in codigo
