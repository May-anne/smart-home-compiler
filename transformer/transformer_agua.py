from lark import Tree, Token


def transformer_agua(tree: Tree) -> dict:
    if isinstance(tree, Token):
        return str(tree)

    match tree.data:
        case "comando_agua":
            return transformer_agua(tree.children[0])

        case "definir_limite_agua":
            alvo = str(tree.children[0])
            valor = float(str(tree.children[1]))
            return {"acao": "definir_limite_agua", "alvo": alvo, "valor": valor}

        case "registrar_consumo_agua":
            alvo = str(tree.children[0])
            valor = float(str(tree.children[1]))
            return {"acao": "registrar_consumo_agua", "alvo": alvo, "valor": valor}

        case "ler_consumo_agua":
            alvo = str(tree.children[0])
            return {"acao": "ler_consumo_agua", "alvo": alvo}

        case "resetar_consumo_agua":
            alvo = str(tree.children[0])
            return {"acao": "resetar_consumo_agua", "alvo": alvo}

        case "alerta_agua":
            mensagem = str(tree.children[0]).strip('"')
            return {"acao": "alerta_agua", "mensagem": mensagem}

        case _:
            raise ValueError(f"Nó desconhecido em água: '{tree.data}'")