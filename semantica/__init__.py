from semantica.semantica_fechadura import semantica_fechadura
from semantica.semantica_intdetector import semantica_intdetector
from semantica.temperatura import semantica_temperatura
from semantica.luminosidade import semantica_luminosidade
from semantica.energia import semantica_energia
from semantica.agua import semantica_agua

COMPARADORES_POR_TIPO = {
    "FECHADURA": {"=="},
    "TERMOSTATO": {">", "<", ">=", "<=", "=="},
    "DIMMER": {">", "<", ">=", "<=", "=="},
    "INTDETECTOR": {"=="},
}

TIPOS_FIXOS_CONHECIDOS = {
    "FECHADURA", "TERMOSTATO", "INTDETECTOR",
    "MEDIDOR_AGUA", "DIMMER", "MEDIDOR_ENERGIA",
}

TIPOS_DE_CAMPO_VALIDOS = {"bool", "int", "string", "float"}


def validar_comparador(tipo_dispositivo, comparador):
    permitidos = COMPARADORES_POR_TIPO.get(tipo_dispositivo)
    if permitidos is None:
        raise Exception(f"Tipo '{tipo_dispositivo}' não tem regras de comparação definidas.")
    if comparador not in permitidos:
        raise Exception(f"{tipo_dispositivo} não aceita comparador '{comparador}'.")


def validar_campos_extra(node):
    nomes_campos = set()
    for campo in node["campos"]:
        if campo["tipo"] not in TIPOS_DE_CAMPO_VALIDOS:
            raise Exception(f"Tipo de campo desconhecido: '{campo['tipo']}'.")
        if campo["nome"] in nomes_campos:
            raise Exception(
                f"Campo '{campo['nome']}' duplicado no device '{node['nome']}'."
            )
        nomes_campos.add(campo["nome"])


def semantica_base(node, declarados):
    match node["acao"]:
        case "dispositivo":
            tipo = node["tipo"]
            if tipo not in TIPOS_FIXOS_CONHECIDOS:
                raise Exception(f"Tipo de dispositivo '{tipo}' desconhecido.")
            if node["nome"] in declarados:
                raise Exception(f"Dispositivo '{node['nome']}' já foi declarado.")

            validar_campos_extra(node)
            declarados[node["nome"]] = tipo

        case "trancar" | "destrancar" | "alerta":
            semantica_fechadura(node, declarados)

        case "definir_temperatura" | "ler_temperatura" | "alerta_temperatura" | "condicional_temperatura":
            semantica_temperatura(node, declarados)

        case "definir_luminosidade" | "ler_luminosidade" | "alerta_luminosidade" | "condicional_luminosidade":
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
            | "condicional_energia"
        ):
            semantica_energia(node, declarados)

        case (
            "definir_limite_agua"
            | "registrar_consumo_agua"
            | "ler_consumo_agua"
            | "resetar_consumo_agua"
            | "alerta_agua"
            | "condicional_agua"
        ):
            semantica_agua(node, declarados)

        case "condicional":
            if node["alvo"] not in declarados:
                raise Exception(f"{node['alvo']} não foi declarado.")

            tipo_alvo = declarados[node["alvo"]]
            validar_comparador(tipo_alvo, node["comparador"])

            if node["valor"]["tipo"] == "string" and node["comparador"] != "==":
                raise Exception("String só aceita '=='.")

            for item in node["se"]:
                semantica_base(item, declarados)
            for item in node["senao"]:
                semantica_base(item, declarados)

            node["tipo"] = "bool"

        case _:
            raise Exception(f"Nó desconhecido '{node}'")