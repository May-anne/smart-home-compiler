def checar_declaracao(nome, tipo_esperado, declarados):
    if nome not in declarados:
        raise Exception(f"{nome} não foi declarado.")
    if declarados[nome] != tipo_esperado:
        raise Exception(f"{nome} é {declarados[nome]}, o esperado é {tipo_esperado}.")

def semantica_luminosidade(node, declarados):
    match node["acao"]:
        case "definir_luminosidade":
            checar_declaracao(node["alvo"], "DIMMER", declarados)
            if not (0 <= node["valor"] <= 100):
                raise Exception(
                    f"Valor de luminosidade '{node['valor']}' fora do intervalo permitido [0, 100]."
                )
            node["tipo"] = "void"

        case "ler_luminosidade":
            checar_declaracao(node["alvo"], "DIMMER", declarados)
            node["tipo"] = "void"

        case "alerta_luminosidade":
            node["tipo"] = "void"

        case "condicional_luminosidade":
            checar_declaracao(node["alvo"], "DIMMER", declarados)
            if not (0 <= node["valor"] <= 100):
                raise Exception(
                    f"Valor de referência '{node['valor']}' na condicional fora do intervalo [0, 100]."
                )
            semantica_luminosidade(node["se_verdadeiro"], declarados)
            semantica_luminosidade(node["se_falso"], declarados)
            node["tipo"] = "bool"

        case _:
            raise Exception(f"Nó desconhecido em luminosidade: '{node['acao']}'")