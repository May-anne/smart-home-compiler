def checar_declaracao(nome, tipo_esperado, declarados):
    if nome not in declarados:
        raise Exception(f"{nome} não foi declarado.")
    if declarados[nome] != tipo_esperado:
        raise Exception(f"{nome} é {declarados[nome]}, o esperado é {tipo_esperado}.")


def semantica_agua(node, declarados):
    match node["acao"]:
        case "dispositivo_medidor_agua":
            declarados[node["nome"]] = "MEDIDOR_AGUA"
            node["tipo"] = "void"

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

        case "condicional_agua":
            checar_declaracao(node["alvo"], "MEDIDOR_AGUA", declarados)
            if node["valor"] < 0:
                raise Exception(
                    f"Valor de referência '{node['valor']}' na condicional não pode ser negativo."
                )
            semantica_agua(node["se_verdadeiro"], declarados)
            semantica_agua(node["se_falso"], declarados)
            node["tipo"] = "bool"

        case _:
            raise Exception(f"Nó desconhecido em água: '{node['acao']}'")