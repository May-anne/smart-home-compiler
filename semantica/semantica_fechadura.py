def checar_declaracao(nome, tipo_esperado, declarados):
    if nome not in declarados:
        raise Exception(f"{nome} não foi declarado.")
    if declarados[nome] != tipo_esperado:
        raise Exception(f"{nome} é {declarados[nome]}, o esperado é {tipo_esperado}.")
    
def semantica_fechadura(node, declarados):
    match node["acao"]:
        case "trancar":
            checar_declaracao(node["alvo"], "FECHADURA", declarados)
            node["tipo"] = "void"
        case "destrancar":
            checar_declaracao(node["alvo"], "FECHADURA", declarados)
            node["tipo"] = "void"
        case "alerta":
            node["tipo"] = "void"
        case _:
            raise Exception(f"Nó desconhecido em fechadura: '{node['acao']}'")