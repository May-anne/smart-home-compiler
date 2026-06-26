from semantica.utils import checar_declaracao

def semantica_fechadura(node, declarados, senha_validada):
    match node["acao"]:
        case "informar_senha_fechadura":
            checar_declaracao(node["nome"], "FECHADURA", declarados)
            senha_validada[node["nome"]] = node["senha"]
            node["tipo"] = "void"

        case "trancar":
            checar_declaracao(node["nome"], "FECHADURA", declarados)
            node["tipo"] = "void"

        case "destrancar":
            checar_declaracao(node["nome"], "FECHADURA", declarados)
            if node["nome"] not in senha_validada:
                raise Exception(
                    f"{node['nome']}: é preciso informar a senha antes de DESTRANCAR."
                )
            del senha_validada[node["nome"]]
            node["tipo"] = "void"

        case "alerta":
            node["tipo"] = "void"

        case _:
            raise Exception(f"Nó desconhecido em fechadura: '{node['acao']}'")