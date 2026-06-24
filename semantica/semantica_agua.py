from semantica.utils import checar_declaracao

def semantica_agua(node, declarados):
    match node["acao"]:  
        case "definir_limite_agua":
            checar_declaracao(node["alvo"], "MEDIDOR_AGUA", declarados)
            if node["valor"] < 0:
                raise Exception(
                    f"Limite de água '{node['valor']}' não pode ser negativo."
                )
            node["tipo"] = "void"

        case "registrar_consumo_agua":
            checar_declaracao(node["alvo"], "MEDIDOR_AGUA", declarados)
            if node["valor"] < 0:
                raise Exception(
                    f"Consumo de água '{node['valor']}' litros não pode ser negativo."
                )
            node["tipo"] = "void"

        case "ler_consumo_agua":
            checar_declaracao(node["alvo"], "MEDIDOR_AGUA", declarados)
            node["tipo"] = "void"

        case "resetar_consumo_agua":
            checar_declaracao(node["alvo"], "MEDIDOR_AGUA", declarados)
            node["tipo"] = "void"

        case "alerta_agua":
            node["tipo"] = "void"

        case _:
            raise Exception(f"Nó desconhecido em água: '{node['acao']}'")