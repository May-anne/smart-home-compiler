import sys
import json
from lark import Lark

from gramatica import GRAMATICA_COMPLETA
from transformer import transformer
from semantica import semantica_base
from gerador.gerador import MAPA_TIPOS, MAPA_COMPARADORES, MAPA_METODOS


def gerar_cpp(node, nivel=0, declarados=None):
    ind  = "    " * nivel
    ind1 = "    " * (nivel + 1)

    match node["acao"]:

        case "dispositivo":
            tipo_orig = (declarados or {}).get(node["nome"], node["tipo"])
            tipo_cpp  = MAPA_TIPOS.get(tipo_orig, tipo_orig)
            return f"{ind}{tipo_cpp} {node['nome']};"

        case "definir_temperatura":
            return f"{ind}{node['alvo']}.setTemperatura({node['valor']});"
        case "ler_temperatura":
            return f"{ind}{node['alvo']}.lerTemperatura();"
        case "alerta_temperatura":
            return f'{ind}std::cout << "[TEMP] {node["mensagem"]}" << std::endl;'

        case "definir_luminosidade":
            return f"{ind}{node['alvo']}.setLuminosidade({node['valor']});"
        case "ler_luminosidade":
            return f"{ind}{node['alvo']}.lerLuminosidade();"
        case "alerta_luminosidade":
            return f'{ind}std::cout << "[LUZ] {node["mensagem"]}" << std::endl;'

        case "trancar":
            return f"{ind}{node['nome']}.trancar();"
        case "destrancar":
            return (
                f"{ind}{node['nome']}.destrancar();\n"
                f"{ind1}// LED: {node['led']}"
            )
        case "alerta":
            return f"{ind}// LED: {node['led']}"

        case "informar_senha":
            return f"{ind}{node['alvo']}.informarSenha(\"{node['senha']}\");"
        case "informar_senha_fechadura":
            return f"{ind}{node['nome']}.informarSenha(\"{node['senha']}\");"

        case "configurar_detector":
            return f"{ind}{node['alvo']}.configurar({node['timeout']}, \"{node['codigo']}\");"
        case "armar_detector":
            return f"{ind}{node['alvo']}.armar();"
        case "desarmar_detector":
            return f"{ind}{node['alvo']}.desarmar();"
        case "detectar_presenca":
            return f"{ind}{node['alvo']}.detectarPresenca();"
        case "timeout_expirado":
            return f"{ind}{node['alvo']}.timeoutExpirado();"
        case "disparar_alarme":
            return f"{ind}{node['alvo']}.dispararAlarme();"
        case "definir_hora_funcionamento":
            return (
                f"{ind}{node['alvo']}.setHorario"
                f"(\"{node['hora_inicio']}\", \"{node['hora_fim']}\");"
            )

        case "definir_limite_energia":
            return f"{ind}{node['alvo']}.setLimite({node['valor']});"
        case "registrar_consumo_energia":
            return f"{ind}{node['alvo']}.registrarConsumo({node['valor']});"
        case "ler_consumo_energia":
            return f"{ind}{node['alvo']}.lerConsumo();"
        case "resetar_consumo_energia":
            return f"{ind}{node['alvo']}.resetarConsumo();"
        case "alerta_energia":
            return f'{ind}std::cout << "[ENERGIA] {node["mensagem"]}" << std::endl;'

        case "definir_limite_agua":
            return f"{ind}{node['alvo']}.setLimite({node['valor']});"
        case "registrar_consumo_agua":
            return f"{ind}{node['alvo']}.registrarConsumo({node['valor']});"
        case "ler_consumo_agua":
            return f"{ind}{node['alvo']}.lerConsumo();"
        case "resetar_consumo_agua":
            return f"{ind}{node['alvo']}.resetarConsumo();"
        case "alerta_agua":
            return f'{ind}std::cout << "[AGUA] {node["mensagem"]}" << std::endl;'

        case "condicional":
            op     = MAPA_COMPARADORES[node["comparador"]]
            valor  = node["valor"]["valor"]
            if node["valor"]["tipo"] == "string":
                valor = f'"{valor}"'
            tipo   = (declarados or {}).get(node["alvo"], "")
            metodo = MAPA_METODOS.get(tipo, "getValor()")
            linhas_se    = "\n".join(
                gerar_cpp(i, nivel + 1, declarados) for i in node["se"]
            )
            linhas_senao = "\n".join(
                gerar_cpp(i, nivel + 1, declarados) for i in node["senao"]
            )
            return (
                f"{ind}if ({node['alvo']}.{metodo} {op} {valor}) {{\n"
                f"{linhas_se}\n{ind}}} else {{\n{linhas_senao}\n{ind}}}"
            )

        case _:
            raise ValueError(f"Nó desconhecido no gerador C++: '{node['acao']}'")


def gerar_programa(nos, declarados=None):
    linhas = [
        '#include "SmartHome.h"',
        "#include <iostream>\n",
        "int main() {",
    ]
    for no in nos:
        linhas.append(gerar_cpp(no, nivel=1, declarados=declarados))
    linhas += ["", "    return 0;", "}"]
    return "\n".join(linhas)


CODIGO_FONTE = """\
device fechadura1  { type FECHADURA; }
device termostato1 { type TERMOSTATO; }
device dimmer1     { type DIMMER; }
device detector1   { type INTDETECTOR; }
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
    parser = Lark(GRAMATICA_COMPLETA, parser="earley", start="start")
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
    declarados    = {}
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