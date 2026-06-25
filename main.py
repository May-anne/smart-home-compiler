import sys
import json
from lark import Lark

from gramatica import GRAMATICA_COMPLETA
from transformer import transformer
from semantica import semantica_base
from gerador.gerador import gerar_programa


CODIGO_FONTE = """\
device fechadura1  { type FECHADURA; }
device termostato1 { type TERMOSTATO; }
device dimmer1     { type DIMMER; }
device detector1   { type INTDETECTOR; int timeout_alerta; string start_time; string end_time; bool person_detected;}
device agua1       { type MEDIDOR_AGUA; }
device energia1    { type MEDIDOR_ENERGIA; }

INFORMAR_SENHA_FECHADURA fechadura1 COM SENHA "1234"
TRANCAR fechadura1
INFORMAR_SENHA_FECHADURA fechadura1 COM SENHA "1234"
DESTRANCAR fechadura1
ALERTA

DEFINIR_TEMPERATURA termostato1 PARA 22
LER_TEMPERATURA termostato1
ALERTA_TEMP "Temperatura muito alta"

DEFINIR_LUMINOSIDADE dimmer1 PARA 75
LER_LUMINOSIDADE dimmer1
ALERTA_LUZ "Luz baixa"

CONFIGURAR detector1 COM TIMEOUT 30 SEGUNDOS E CODIGO "ABC123"
ARMAR detector1
DESARMAR detector1
detector1 DETECTOU PRESENCA
INFORMAR_SENHA detector1 COM "9999"
TIMEOUT detector1 EXPIRADO
DISPARAR_ALARME detector1
DEFINIR_HORA_FUNCIONAMENTO detector1 DAS 08:00 AS 18:00

DEFINIR_LIMITE_ENERGIA energia1 PARA 500 KWH
REGISTRAR_CONSUMO_ENERGIA energia1 PARA 120 KWH
LER_CONSUMO_ENERGIA energia1
RESETAR_CONSUMO_ENERGIA energia1
ALERTA_ENERGIA "Limite proximo"

DEFINIR_LIMITE_AGUA agua1 PARA 300 LITROS
REGISTRAR_CONSUMO_AGUA agua1 PARA 80 LITROS
LER_CONSUMO_AGUA agua1
RESETAR_CONSUMO_AGUA agua1
ALERTA_AGUA "Consumo alto"

SE termostato1 > 30 ENTAO
    ALERTA_TEMP "Muito quente"
    DEFINIR_TEMPERATURA termostato1 PARA 20
SENAO
    DEFINIR_TEMPERATURA termostato1 PARA 25
FIM
"""


def sep(titulo):
    print(f"\n{'='*60}\n  {titulo}\n{'='*60}")


def main():
    sep("1. PARSE")
    parser = Lark(GRAMATICA_COMPLETA, parser="lalr", start="start")
    try:
        tree = parser.parse(CODIGO_FONTE)
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
    declarados     = {}
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