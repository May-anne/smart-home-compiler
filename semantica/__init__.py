from semantica.fechadura import semantica_fechadura
from semantica.temperatura import semantica_temperatura
from semantica.luminosidade import semantica_luminosidade

def checar_declaracao(nome, tipo_esperado, declarados):
    if nome not in declarados:
        raise Exception(f"{nome} não foi declarado.")
    if declarados[nome] != tipo_esperado:
        raise Exception(f"{nome} é {declarados[nome]}, o esperado é {tipo_esperado}.")

def semantica_base(node, declarados):
    match node.get("acao") or node.get("tipo"):
        case "dispositivo":
            declarados[node["nome"]] = node["tipo"]

        case "trancar" | "destrancar" | "alerta" | "verificar_senha":
            semantica_fechadura(node, declarados)

        case "definir_temperatura" | "ler_temperatura" | "alerta_temperatura" | "condicional_temperatura":
            semantica_temperatura(node, declarados)

        case "definir_luminosidade" | "ler_luminosidade" | "alerta_luminosidade" | "condicional_luminosidade":
            semantica_luminosidade(node, declarados)

        case "condicional":
            if node["valor"]["tipo"] == "string" and node["comparador"] != "==":
                raise Exception("String só aceita '=='.")

            semantica_base(node["se"], declarados)
            semantica_base(node["senao"], declarados)
            node["tipo"] = "bool"

        case _:
            raise Exception(f"Nó desconhecido '{node}'")