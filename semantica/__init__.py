from semantica.semantica_fechadura import semantica_fechadura
from semantica.semantica_intdetector import semantica_intdetector
from semantica.temperatura import semantica_temperatura
from semantica.luminosidade import semantica_luminosidade
from semantica.energia import semantica_energia
from semantica.agua import semantica_agua


COMPARADORES_POR_TIPO = {
    "FECHADURA": {"=="},
    "TEMPERATURA": {">", "<", ">=", "<=", "=="},
    "LUMINOSIDADE": {">", "<", ">=", "<=", "=="},
    "INTDETECTOR": {"=="},
}

TIPOS_DE_CAMPO_VALIDOS = {"bool", "int", "string", "float"}

TIPOS_DEVICE_INTERNOS = {
    "intrusion_detector": "INTDETECTOR",
    "locker": "FECHADURA",
    "temp_sensor": "TERMOSTATO",
    "hydrometer": "MEDIDOR_AGUA",
    "lum_sensor": "DIMMER",
    "energy_meter": "MEDIDOR_ENERGIA",
}

CAMPOS_INTRUSION_DETECTOR = {
    "timeout_alarm": "int",
    "passkey": "string",
    "start_time": "string",
    "end_time": "string",
    "person_detected": "bool",
}


def validar_comparador(tipo_dispositivo, comparador):
    permitidos = COMPARADORES_POR_TIPO.get(tipo_dispositivo)
    if permitidos is None:
        raise Exception(
            f"Tipo '{tipo_dispositivo}' não tem regras de comparação definidas."
        )
    if comparador not in permitidos:
        raise Exception(f"{tipo_dispositivo} não aceita comparador '{comparador}'.")


def semantica_device(node, declarados, tipos_definidos):
    nome = node["nome"]
    tipo_device = node["tipo_device"]

    if nome in declarados:
        raise Exception(f"Dispositivo '{nome}' já foi declarado.")
    if tipo_device not in TIPOS_DEVICE_INTERNOS:
        raise Exception(f"Tipo de dispositivo desconhecido: '{tipo_device}'.")

    campos_por_nome = {}
    for campo in node["campos"]:
        tipo_campo = campo["tipo"]
        nome_campo = campo["nome"]

        if tipo_campo not in TIPOS_DE_CAMPO_VALIDOS:
            raise Exception(f"Tipo de campo desconhecido: '{tipo_campo}'.")
        if nome_campo in campos_por_nome:
            raise Exception(f"Campo '{nome_campo}' duplicado no device '{nome}'.")
        campos_por_nome[nome_campo] = tipo_campo

    if tipo_device == "intrusion_detector":
        ausentes = CAMPOS_INTRUSION_DETECTOR.keys() - campos_por_nome.keys()
        extras = campos_por_nome.keys() - CAMPOS_INTRUSION_DETECTOR.keys()

        if ausentes:
            raise Exception(
                "Campos obrigatórios ausentes no intrusion_detector "
                f"'{nome}': {', '.join(sorted(ausentes))}."
            )
        if extras:
            raise Exception(
                f"Campos inválidos no intrusion_detector '{nome}': "
                f"{', '.join(sorted(extras))}."
            )

        for nome_campo, tipo_esperado in CAMPOS_INTRUSION_DETECTOR.items():
            tipo_recebido = campos_por_nome[nome_campo]
            if tipo_recebido != tipo_esperado:
                raise Exception(
                    f"Campo '{nome_campo}' do intrusion_detector '{nome}' "
                    f"deve ser '{tipo_esperado}', não '{tipo_recebido}'."
                )

    declarados[nome] = TIPOS_DEVICE_INTERNOS[tipo_device]
    tipos_definidos[nome] = node["campos"]
    node["tipo"] = "void"


def semantica_base(node, declarados, tipos_definidos=None):
    if tipos_definidos is None:
        tipos_definidos = {}

    match node["acao"]:
        case "declarar_device":
            semantica_device(node, declarados, tipos_definidos)

        case "trancar" | "destrancar" | "alerta":
            semantica_fechadura(node, declarados)

        case (
            "definir_temperatura"
            | "ler_temperatura"
            | "alerta_temperatura"
            | "condicional_temperatura"
        ):
            semantica_temperatura(node, declarados)

        case (
            "definir_luminosidade"
            | "ler_luminosidade"
            | "alerta_luminosidade"
            | "condicional_luminosidade"
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
                semantica_base(item, declarados, tipos_definidos)
            for item in node["senao"]:
                semantica_base(item, declarados, tipos_definidos)

            node["tipo"] = "bool"

        case _:
            raise Exception(f"Nó desconhecido '{node}'")
