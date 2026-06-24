from semantica.utils import checar_declaracao

def semantica_energia(node, declarados):
    match node["acao"]:
        case "definir_limite_energia":
            checar_declaracao(node["alvo"], "MEDIDOR_ENERGIA", declarados)
            if node["valor"] < 0:
                raise Exception(
                    f"Limite de energia '{node['valor']}' não pode ser negativo."
                )
            node["tipo"] = "void"

        case "registrar_consumo_energia":
            checar_declaracao(node["alvo"], "MEDIDOR_ENERGIA", declarados)
            if node["valor"] < 0:
                raise Exception(
                    f"Consumo de energia '{node['valor']}' kWh não pode ser negativo."
                )
            node["tipo"] = "void"

        case "ler_consumo_energia":
            checar_declaracao(node["alvo"], "MEDIDOR_ENERGIA", declarados)
            node["tipo"] = "void"

        case "resetar_consumo_energia":
            checar_declaracao(node["alvo"], "MEDIDOR_ENERGIA", declarados)
            node["tipo"] = "void"

        case "alerta_energia":
            node["tipo"] = "void"

        case _:
            raise Exception(f"Nó desconhecido em energia: '{node['acao']}'")