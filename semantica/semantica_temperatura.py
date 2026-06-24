from semantica.utils import checar_declaracao

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

        case _:
            raise Exception(f"Nó desconhecido em temperatura: '{node['acao']}'")