from semantica.semantica_fechadura import semantica_fechadura
from semantica.semantica_intdetector import semantica_intdetector
from semantica.temperatura import semantica_temperatura
from semantica.luminosidade import semantica_luminosidade
from semantica.semantica_energia import semantica_energia
from semantica.semantica_agua import semantica_agua

COMPARADORES_POR_TIPO = {
    "FECHADURA": {"=="},
    "TEMPERATURA": {">", "<", ">=", "<=", "=="},
    "LUMINOSIDADE": {">", "<", ">=", "<=", "=="},
    "INTRUSAO": {"=="},
}

TIPOS_FIXOS_CONHECIDOS = {"FECHADURA", "TEMPERATURA", "LUMINOSIDADE", "INTRUSAO", "ENERGIA", "AGUA"}

TIPOS_DE_CAMPO_VALIDOS = {"bool", "int", "string", "float"}

def validar_comparador(tipo_dispositivo, comparador):
    permitidos = COMPARADORES_POR_TIPO.get(tipo_dispositivo)
    if permitidos is None:
        raise Exception(f"Tipo '{tipo_dispositivo}' não tem regras de comparação definidas.")
    if comparador not in permitidos:
        raise Exception(f"{tipo_dispositivo} não aceita comparador '{comparador}'.")


def semantica_device(node, tipos_definidos):
    nome_tipo = node["nome"]

    if nome_tipo in tipos_definidos:
        raise Exception(f"Tipo de dispositivo '{nome_tipo}' já foi definido.")

    nomes_campos = set()
    for campo in node["campos"]:
        if campo["tipo"] not in TIPOS_DE_CAMPO_VALIDOS:
            raise Exception(f"Tipo de campo desconhecido: '{campo['tipo']}'.")
        if campo["nome"] in nomes_campos:
            raise Exception(
                f"Campo '{campo['nome']}' duplicado no device '{nome_tipo}'."
            )
        nomes_campos.add(campo["nome"])

    tipos_definidos[nome_tipo] = node["campos"]


def semantica_base(node, declarados, tipos_definidos=None):
    if tipos_definidos is None:
        tipos_definidos = {}

    match node["acao"]:
        case "definir_tipo":
            semantica_device(node, tipos_definidos)

        case "dispositivo":
            tipo = node["tipo"]
            if tipo not in TIPOS_FIXOS_CONHECIDOS and tipo not in tipos_definidos:
                raise Exception(
                    f"Tipo de dispositivo '{tipo}' não foi declarado "
                    f"(nem é um tipo fixo, nem foi definido com 'device {tipo} {{...}}')."
                )
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
                semantica_base(item, declarados, tipos_definidos)
            for item in node["senao"]:
                semantica_base(item, declarados, tipos_definidos)

            node["tipo"] = "bool"

        case _:
            raise Exception(f"Nó desconhecido '{node}'")