def checar_declaracao(nome, tipo_esperado, declarados):
    if nome not in declarados:
        raise Exception(f"{nome} não foi declarado.")
    if declarados[nome] != tipo_esperado:
        raise Exception(f"{nome} é {declarados[nome]}, o esperado é {tipo_esperado}.")


def semantica_energia(node, declarados):
    match node["acao"]:
        case "dispositivo_medidor_energia":
            declarados[node["nome"]] = "MEDIDOR_ENERGIA"
            node["tipo"] = "void"

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