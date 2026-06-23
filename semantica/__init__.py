from semantica.fechadura import semantica_fechadura

def checar_declaracao(nome, tipo_esperado, declarados):
    if nome not in declarados:
        raise Exception(f"{nome} não foi declarado.")
    if declarados[nome] != tipo_esperado:
        raise Exception(f"{nome} é {declarados[nome]}, o esperado é {tipo_esperado}.")

def semantica_base(node, declarados):
    match node.get("acao") or node.get("tipo"):
        case "dispositivo":
            declarados[node["nome"]] = node["tipo"]

        case "trancar" | "destrancar" | "alerta" | "verificar_senha":
            semantica_fechadura(node, declarados)
        
        # outros casos...

        case "condicional":
            if node["valor"]["tipo"] == "string" and node["comparador"] != "==":
                    raise Exception("String só aceita '=='.")

            semantica_base(node["se"], declarados)
            semantica_base(node["senao"], declarados)
            node["tipo"] = "bool"

        case _:
            raise Exception(f"Nó desconhecido '{node}'")