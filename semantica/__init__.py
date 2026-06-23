from semantica.semantica_fechadura import semantica_fechadura
from semantica.temperatura import semantica_temperatura
from semantica.luminosidade import semantica_luminosidade

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