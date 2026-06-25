from lark import Tree, Token

def transformer_luminosidade(tree: Tree) -> dict:
    if isinstance(tree, Token):
        return str(tree)

    match tree.data:
        case "comando_luminosidade":
            return transformer_luminosidade(tree.children[0])

        case "definir_luminosidade":
            alvo = str(tree.children[0])
            valor = float(str(tree.children[1]))
            return {"acao": "definir_luminosidade", "alvo": alvo, "valor": valor}

        case "ler_luminosidade":
            alvo = str(tree.children[0])
            return {"acao": "ler_luminosidade", "alvo": alvo}

        case "alerta_luminosidade":
            mensagem = str(tree.children[0]).strip('"')
            return {"acao": "alerta_luminosidade", "mensagem": mensagem}

        case _:
            raise ValueError(f"Nó desconhecido em luminosidade: '{tree.data}'")