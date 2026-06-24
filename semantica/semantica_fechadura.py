def checar_declaracao(nome, tipo_esperado, declarados):
    if nome not in declarados:
        raise Exception(f"{nome} não foi declarado.")
    if declarados[nome] != tipo_esperado:
        raise Exception(f"{nome} é {declarados[nome]}, o esperado é {tipo_esperado}.")


def semantica_fechadura(node, declarados, senha_validada):
    match node["acao"]:
        case "informar_senha_fechadura":
            checar_declaracao(node["nome"], "FECHADURA", declarados)
            senha_validada[node["nome"]] = node["senha"]
            node["tipo"] = "void"

        case "trancar":
            checar_declaracao(node["nome"], "FECHADURA", declarados)
            if node["nome"] not in senha_validada:
                raise Exception(
                    f"{node['nome']}: é preciso informar a senha (INFORMAR_SENHA) antes de TRANCAR."
                )
            del senha_validada[node["nome"]]
            node["tipo"] = "void"

        case "destrancar":
            checar_declaracao(node["nome"], "FECHADURA", declarados)
            if node["nome"] not in senha_validada:
                raise Exception(
                    f"{node['nome']}: é preciso informar a senha (INFORMAR_SENHA) antes de DESTRANCAR."
                )
            del senha_validada[node["nome"]]
            node["tipo"] = "void"

        case "alerta":
            node["tipo"] = "void"

        case _:
            raise Exception(f"Nó desconhecido em fechadura: '{node['acao']}'")