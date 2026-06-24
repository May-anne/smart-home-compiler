from semantica.semantica_fechadura import semantica_fechadura
from semantica.semantica_intdetector import semantica_intdetector
from semantica.temperatura import semantica_temperatura
from semantica.luminosidade import semantica_luminosidade
from semantica.semantica_energia import semantica_energia
from semantica.semantica_agua import semantica_agua

def semantica_base(node, declarados):
    
    match node["acao"]:
        case "dispositivo":
            declarados[node["nome"]] = node["tipo"]

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

            if tipo_alvo in ("FECHADURA",) and node["comparador"] != "==":
                raise Exception(f"{tipo_alvo} só aceita comparador '=='.")

            if node["valor"]["tipo"] == "string" and node["comparador"] != "==":
                raise Exception("String só aceita '=='.")

            for item in node["se"]:
                semantica_base(item, declarados)
            for item in node["senao"]:
                semantica_base(item, declarados)

            node["tipo"] = "bool"

        case _:
            raise Exception(f"Nó desconhecido '{node}'")
