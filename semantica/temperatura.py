def checar_declaracao(nome, tipo_esperado, declarados):
    if nome not in declarados:
        raise Exception(f"{nome} não foi declarado.")
    if declarados[nome] != tipo_esperado:
        raise Exception(f"{nome} é {declarados[nome]}, o esperado é {tipo_esperado}.")

def semantica_temperatura(node, declarados):
    match node["acao"]:
        case "definir_temperatura":
            checar_declaracao(node["alvo"], "TERMOSTATO", declarados)
            if not (-50 <= node["valor"] <= 100):
                raise Exception(
                    f"Valor de temperatura '{node['valor']}' fora do intervalo permitido [-50, 100]."
                )
            node["tipo"] = "void"

        case "ler_temperatura":
            checar_declaracao(node["alvo"], "TERMOSTATO", declarados)
            node["tipo"] = "void"

        case "alerta_temperatura":
            node["tipo"] = "void"

        case "condicional_temperatura":
            checar_declaracao(node["alvo"], "TERMOSTATO", declarados)
            if not (-50 <= node["valor"] <= 100):
                raise Exception(
                    f"Valor de referência '{node['valor']}' na condicional fora do intervalo [-50, 100]."
                )
            semantica_temperatura(node["se_verdadeiro"], declarados)
            semantica_temperatura(node["se_falso"], declarados)
            node["tipo"] = "bool"

        case _:
            raise Exception(f"Nó desconhecido em temperatura: '{node['acao']}'")