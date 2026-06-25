import pytest
from lark import Lark
from gramatica import GRAMATICA_COMPLETA
from transformer import transformer
from semantica import semantica_base


# Helpers
def pipeline(codigo):
    """Parse → transform → analyse; retorna (ast, declarados, senha_validada)."""
    parser = Lark(GRAMATICA_COMPLETA, parser="lalr")
    tree = parser.parse(codigo)
    nodes = transformer(tree)
    declarados = {}
    senha_validada = {}
    for node in nodes:
        semantica_base(node, declarados, senha_validada)
    return nodes, declarados, senha_validada


def test_pipeline_device_com_campos_extra():
    nodes, declarados, _ = pipeline("""
    device frigobar {
        type TERMOSTATO;
        bool ligada;
        int temperatura;
    }
    """)
    assert declarados["frigobar"] == "TERMOSTATO"


def test_pipeline_device_sem_campos_extra():
    nodes, declarados, _ = pipeline("device porta_frente { type FECHADURA; }")
    assert declarados["porta_frente"] == "FECHADURA"


def test_pipeline_falha_tipo_dispositivo_invalido():
    parser = Lark(GRAMATICA_COMPLETA, parser="lalr")
    with pytest.raises(Exception):
        parser.parse("device frigobar { type GELADEIRA; }")


def test_pipeline_falha_tipo_campo_invalido():
    parser = Lark(GRAMATICA_COMPLETA, parser="lalr")
    with pytest.raises(Exception):
        parser.parse("device d { type TERMOSTATO; cor algumacoisa; }")


def test_pipeline_falha_campo_duplicado():
    with pytest.raises(Exception, match="duplicado"):
        pipeline("""
        device d {
            type TERMOSTATO;
            int temp;
            int temp;
        }
        """)


def test_pipeline_multiplos_devices():
    _, declarados, _ = pipeline("""
    device porta_frente { type FECHADURA; }
    device frigobar { type TERMOSTATO; bool ligada; }
    device sensor1 { type INTDETECTOR; }
    """)
    assert declarados == {
        "porta_frente": "FECHADURA",
        "frigobar": "TERMOSTATO",
        "sensor1": "INTDETECTOR",
    }


def test_pipeline_falha_dispositivo_duplicado():
    with pytest.raises(Exception, match="já foi declarado"):
        pipeline("""
        device porta_frente { type FECHADURA; }
        device porta_frente { type FECHADURA; }
        """)


# Intdetector
def test_pipeline_intdetector_comandos_basicos():
    nodes, declarados, _ = pipeline("""
    device alarme { type INTDETECTOR; }
    CONFIGURAR alarme COM TIMEOUT 30 SEGUNDOS E CODIGO "4321"
    ARMAR alarme
    alarme DETECTOU PRESENCA
    DISPARAR_ALARME alarme
    INFORMAR_SENHA alarme COM "4321"
    DESARMAR alarme
    """)
    assert declarados["alarme"] == "INTDETECTOR"
    assert all(n["tipo"] == "void" for n in nodes)

def test_pipeline_intdetector_falha_horario_igual():
    with pytest.raises(Exception, match="devem ser diferentes"):
        pipeline("""
        device alarme { type INTDETECTOR; }
        DEFINIR_HORA_FUNCIONAMENTO alarme DAS 10:00 AS 10:00
        """)


def test_pipeline_intdetector_falha_timeout_zero():
    with pytest.raises(Exception, match="maior que zero"):
        pipeline("""
        device alarme { type INTDETECTOR; }
        CONFIGURAR alarme COM TIMEOUT 0 SEGUNDOS E CODIGO "1111"
        """)


def test_pipeline_intdetector_falha_dispositivo_errado():
    with pytest.raises(Exception, match="INTDETECTOR"):
        pipeline("""
        device porta { type FECHADURA; }
        ARMAR porta
        """)


# Temperatura
def test_pipeline_temperatura_definir():
    nodes, declarados, _ = pipeline("""
    device frig { type TERMOSTATO; }
    DEFINIR_TEMPERATURA frig PARA 22
    """)
    assert declarados["frig"] == "TERMOSTATO"
    assert nodes[-1]["valor"] == 22.0


def test_pipeline_temperatura_ler():
    nodes, _, _ = pipeline("""
    device frig { type TERMOSTATO; }
    LER_TEMPERATURA frig
    """)
    assert nodes[-1]["acao"] == "ler_temperatura"
    assert nodes[-1]["tipo"] == "void"


def test_pipeline_temperatura_alerta():
    nodes, _, _ = pipeline("""
    ALERTA_TEMP "temperatura critica"
    """)
    assert nodes[-1]["mensagem"] == "temperatura critica"


def test_pipeline_temperatura_falha_fora_do_intervalo():
    with pytest.raises(Exception, match="intervalo"):
        pipeline("""
        device frig { type TERMOSTATO; }
        DEFINIR_TEMPERATURA frig PARA 200
        """)


def test_pipeline_temperatura_falha_dispositivo_errado():
    with pytest.raises(Exception, match="TERMOSTATO"):
        pipeline("""
        device porta { type FECHADURA; }
        DEFINIR_TEMPERATURA porta PARA 20
        """)


# Luminosidade
def test_pipeline_luminosidade_definir():
    nodes, declarados, _ = pipeline("""
    device luz { type DIMMER; }
    DEFINIR_LUMINOSIDADE luz PARA 75
    """)
    assert declarados["luz"] == "DIMMER"
    assert nodes[-1]["valor"] == 75.0


def test_pipeline_luminosidade_ler():
    nodes, _, _ = pipeline("""
    device luz { type DIMMER; }
    LER_LUMINOSIDADE luz
    """)
    assert nodes[-1]["acao"] == "ler_luminosidade"


def test_pipeline_luminosidade_alerta():
    nodes, _, _ = pipeline("""
    ALERTA_LUZ "luz muito forte"
    """)
    assert nodes[-1]["mensagem"] == "luz muito forte"


def test_pipeline_luminosidade_falha_fora_do_intervalo():
    with pytest.raises(Exception, match="intervalo"):
        pipeline("""
        device luz { type DIMMER; }
        DEFINIR_LUMINOSIDADE luz PARA 150
        """)


def test_pipeline_luminosidade_falha_valor_negativo():
    with pytest.raises(Exception, match="intervalo"):
        pipeline("""
        device luz { type DIMMER; }
        DEFINIR_LUMINOSIDADE luz PARA -1
        """)


# Fechadura
def test_pipeline_fechadura_fluxo_trancar():
    nodes, declarados, _ = pipeline("""
    device porta { type FECHADURA; }
    INFORMAR_SENHA_FECHADURA porta COM SENHA "segredo"
    TRANCAR porta
    """)
    assert declarados["porta"] == "FECHADURA"
    assert all(n["tipo"] == "void" for n in nodes)


def test_pipeline_fechadura_fluxo_destrancar():
    nodes, _, _ = pipeline("""
    device porta { type FECHADURA; }
    INFORMAR_SENHA_FECHADURA porta COM SENHA "abc123"
    DESTRANCAR porta
    """)
    assert nodes[-1]["acao"] == "destrancar"


def test_pipeline_fechadura_alerta():
    nodes, _, _ = pipeline("""
    ALERTA
    """)
    assert nodes[-1]["acao"] == "alerta"


def test_pipeline_fechadura_falha_trancar_sem_senha():
    with pytest.raises(Exception, match="senha"):
        pipeline("""
        device porta { type FECHADURA; }
        TRANCAR porta
        """)


def test_pipeline_fechadura_falha_destrancar_sem_senha():
    with pytest.raises(Exception, match="senha"):
        pipeline("""
        device porta { type FECHADURA; }
        DESTRANCAR porta
        """)


def test_pipeline_fechadura_falha_dispositivo_errado():
    with pytest.raises(Exception, match="FECHADURA"):
        pipeline("""
        device t { type TERMOSTATO; }
        INFORMAR_SENHA_FECHADURA t COM SENHA "x"
        """)


# Energia
def test_pipeline_energia_comandos():
    nodes, declarados, _ = pipeline("""
    device medidor { type MEDIDOR_ENERGIA; }
    DEFINIR_LIMITE_ENERGIA medidor PARA 500 KWH
    REGISTRAR_CONSUMO_ENERGIA medidor PARA 50 KWH
    LER_CONSUMO_ENERGIA medidor
    RESETAR_CONSUMO_ENERGIA medidor
    """)
    assert declarados["medidor"] == "MEDIDOR_ENERGIA"
    assert all(n["tipo"] == "void" for n in nodes)


def test_pipeline_energia_alerta():
    nodes, _, _ = pipeline('ALERTA_ENERGIA "consumo alto"')
    assert nodes[-1]["mensagem"] == "consumo alto"


def test_pipeline_energia_falha_valor_negativo():
    with pytest.raises(Exception, match="negativo"):
        pipeline("""
        device medidor { type MEDIDOR_ENERGIA; }
        DEFINIR_LIMITE_ENERGIA medidor PARA -10 KWH
        """)


def test_pipeline_energia_falha_dispositivo_errado():
    with pytest.raises(Exception, match="MEDIDOR_ENERGIA"):
        pipeline("""
        device porta { type FECHADURA; }
        LER_CONSUMO_ENERGIA porta
        """)


# Água
def test_pipeline_agua_comandos():
    nodes, declarados, _ = pipeline("""
    device hidrometro { type MEDIDOR_AGUA; }
    DEFINIR_LIMITE_AGUA hidrometro PARA 1000 LITROS
    REGISTRAR_CONSUMO_AGUA hidrometro PARA 200 LITROS
    LER_CONSUMO_AGUA hidrometro
    RESETAR_CONSUMO_AGUA hidrometro
    """)
    assert declarados["hidrometro"] == "MEDIDOR_AGUA"
    assert all(n["tipo"] == "void" for n in nodes)


def test_pipeline_agua_alerta():
    nodes, _, _ = pipeline('ALERTA_AGUA "vazamento detectado"')
    assert nodes[-1]["mensagem"] == "vazamento detectado"


def test_pipeline_agua_falha_valor_negativo():
    with pytest.raises(Exception, match="negativo"):
        pipeline("""
        device hidrometro { type MEDIDOR_AGUA; }
        REGISTRAR_CONSUMO_AGUA hidrometro PARA -5 LITROS
        """)


def test_pipeline_agua_falha_dispositivo_errado():
    with pytest.raises(Exception, match="MEDIDOR_AGUA"):
        pipeline("""
        device luz { type DIMMER; }
        LER_CONSUMO_AGUA luz
        """)


# Condicional
def test_pipeline_condicional_temperatura():
    nodes, _, _ = pipeline("""
    device frig { type TERMOSTATO; }
    SE frig > 30 ENTAO
        ALERTA_TEMP "quente demais"
    SENAO
        DEFINIR_TEMPERATURA frig PARA 20
    FIM
    """)
    cond = nodes[-1]
    assert cond["acao"] == "condicional"
    assert cond["tipo"] == "bool"
    assert cond["comparador"] == ">"


def test_pipeline_condicional_luminosidade():
    nodes, _, _ = pipeline("""
    device luz { type DIMMER; }
    SE luz < 10 ENTAO
        DEFINIR_LUMINOSIDADE luz PARA 50
    SENAO
        ALERTA_LUZ "ok"
    FIM
    """)
    assert nodes[-1]["acao"] == "condicional"


def test_pipeline_condicional_falha_valor_fora_intervalo():
    with pytest.raises(Exception, match="intervalo"):
        pipeline("""
        device frig { type TERMOSTATO; }
        SE frig > 200 ENTAO
            ALERTA_TEMP "erro"
        SENAO
            ALERTA_TEMP "ok"
        FIM
        """)


def test_pipeline_condicional_falha_dispositivo_nao_declarado():
    with pytest.raises(Exception, match="não foi declarado"):
        pipeline("""
        SE fantasma > 10 ENTAO
            ALERTA_TEMP "ops"
        SENAO
            ALERTA_TEMP "ok"
        FIM
        """)


def test_pipeline_condicional_falha_comparador_invalido_fechadura():
    with pytest.raises(Exception, match="comparador"):
        pipeline("""
        device porta { type FECHADURA; }
        SE porta > 0 ENTAO
            ALERTA
        SENAO
            ALERTA
        FIM
        """)
