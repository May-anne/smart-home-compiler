from semantica.semantica_fechadura import semantica_fechadura
from semantica.semantica_intdetector import semantica_intdetector
from semantica.semantica_temperatura import semantica_temperatura
from semantica.semantica_luminosidade import semantica_luminosidade
from semantica.semantica_energia import semantica_energia
from semantica.semantica_agua import semantica_agua
from copy import copy

COMPARADORES_POR_TIPO = {
    "FECHADURA": {"=="},
    "TERMOSTATO": {">", "<", ">=", "<=", "=="},
    "DIMMER": {">", "<", ">=", "<=", "=="},
    "INTDETECTOR": {"=="},
    "MEDIDOR_AGUA": {">", "<", ">=", "<=", "=="},
    "MEDIDOR_ENERGIA": {">", "<", ">=", "<=", "=="},
}

TIPOS_FIXOS_CONHECIDOS = {
    "FECHADURA", "TERMOSTATO", "INTDETECTOR",
    "MEDIDOR_AGUA", "DIMMER", "MEDIDOR_ENERGIA",
}

TIPOS_DE_CAMPO_VALIDOS = {"bool", "int", "string", "float"}


def validar_campos_extra(node):
    campos_por_nome = {}
    for campo in node.get("campos", []):
        tipo_campo = campo["tipo"]
        nome_campo = campo["nome"]
        if tipo_campo not in TIPOS_DE_CAMPO_VALIDOS:
            raise Exception(f"Tipo de campo desconhecido: '{tipo_campo}'.")
        if nome_campo in campos_por_nome:
            raise Exception(f"Campo '{nome_campo}' duplicado no device '{node['nome']}'.")
        campos_por_nome[nome_campo] = tipo_campo


def validar_comparador(tipo_dispositivo, comparador):
    permitidos = COMPARADORES_POR_TIPO.get(tipo_dispositivo)
    if permitidos is None:
        raise Exception(
            f"Tipo '{tipo_dispositivo}' não tem regras de comparação definidas."
        )
    if comparador not in permitidos:
        raise Exception(f"{tipo_dispositivo} não aceita comparador '{comparador}'.")


def semantica_device(node, declarados):
    nome = node["nome"]
    tipo_device = node["tipo"]

    if nome in declarados:
        raise Exception(f"Dispositivo '{nome}' já foi declarado.")
    if tipo_device not in TIPOS_FIXOS_CONHECIDOS:
        raise Exception(f"Tipo de dispositivo desconhecido: '{tipo_device}'.")

    validar_campos_extra(node)

    declarados[nome] = tipo_device
    node["tipo"] = "void"


def _validar_valor_condicional(tipo_alvo, valor):
    match tipo_alvo:
        case "TERMOSTATO":
            if not (-50 <= valor <= 100):
                raise Exception(
                    f"Valor '{valor}' fora do intervalo de temperatura [-50, 100]."
                )
        case "DIMMER":
            if not (0 <= valor <= 100):
                raise Exception(
                    f"Valor '{valor}' fora do intervalo de luminosidade [0, 100]."
                )
        case "MEDIDOR_AGUA":
            if valor < 0:
                raise Exception(
                    f"Valor '{valor}' de referência para água não pode ser negativo."
                )
        case "MEDIDOR_ENERGIA":
            if valor < 0:
                raise Exception(
                    f"Valor '{valor}' de referência para energia não pode ser negativo."
                )


def semantica_base(node, declarados, senha_validada=None):
    if senha_validada is None:
        senha_validada = {}

    match node["acao"]:
        case "dispositivo":
            semantica_device(node, declarados)

        case "informar_senha_fechadura" | "trancar" | "destrancar" | "alerta":
            semantica_fechadura(node, declarados, senha_validada)

        case (
            "definir_temperatura"
            | "ler_temperatura"
            | "alerta_temperatura"
        ):
            semantica_temperatura(node, declarados)

        case (
            "definir_luminosidade"
            | "ler_luminosidade"
            | "alerta_luminosidade"
        ):
            semantica_luminosidade(node, declarados)

        case (
            "configurar_detector"
            | "armar_detector"
            | "desarmar_detector"
            | "detectar_presenca"
            | "informar_senha"
            | "timeout_expirado"
            | "disparar_alarme"
            | "definir_hora_funcionamento"
        ):
            semantica_intdetector(node, declarados)

        case (
            "definir_limite_energia"
            | "registrar_consumo_energia"
            | "ler_consumo_energia"
            | "resetar_consumo_energia"
            | "alerta_energia"
        ):
            semantica_energia(node, declarados)

        case (
            "definir_limite_agua"
            | "registrar_consumo_agua"
            | "ler_consumo_agua"
            | "resetar_consumo_agua"
            | "alerta_agua"
        ):
            semantica_agua(node, declarados)

        case "condicional":
            if node["alvo"] not in declarados:
                raise Exception(f"'{node['alvo']}' não foi declarado.")

            tipo_alvo = declarados[node["alvo"]]
            validar_comparador(tipo_alvo, node["comparador"])

            if node["valor"]["tipo"] == "string" and node["comparador"] != "==":
                raise Exception("Comparação com string só aceita '=='.")

            if node["valor"]["tipo"] == "numero":
                _validar_valor_condicional(tipo_alvo, node["valor"]["valor"])

            for item in node["se"]:
                semantica_base(item, declarados, copy(senha_validada))
            for item in node["senao"]:
                semantica_base(item, declarados, copy(senha_validada))

            node["tipo"] = "bool"

        case _:
            raise Exception(f"Nó desconhecido: '{node['acao']}'")
