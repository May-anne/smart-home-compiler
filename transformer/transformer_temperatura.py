from lark import Tree, Token

def transformer_temperatura(tree: Tree) -> dict:
    if isinstance(tree, Token):
        return str(tree)

    match tree.data:
        case "comando_temperatura":
            return transformer_temperatura(tree.children[0])

        case "dispositivo_termostato":
            nome = str(tree.children[0])
            return {"acao": "dispositivo_termostato", "nome": nome}

        case "definir_temperatura":
            alvo = str(tree.children[0])
            valor = float(str(tree.children[1]))
            return {"acao": "definir_temperatura", "alvo": alvo, "valor": valor}

        case "ler_temperatura":
            alvo = str(tree.children[0])
            return {"acao": "ler_temperatura", "alvo": alvo}

        case "alerta_temperatura":
            mensagem = str(tree.children[0]).strip('"')
            return {"acao": "alerta_temperatura", "mensagem": mensagem}
        
        case _:
            raise ValueError(f"Nó desconhecido em temperatura: '{tree.data}'")