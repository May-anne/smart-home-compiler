from lark import Tree

def transformer_fechadura(tree: Tree):
    match tree.data:
        case "dispositivo_fechadura":
            nome = str(tree.children[0])
            return {"acao": "dispositivo", "nome":nome, "tipo":"FECHADURA"}
        case "trancar":
            alvo = str(tree.children[0])
            return {"acao": "trancar", "alvo": alvo}
        case "destrancar":
            alvo = str(tree.children[0])
            senha = str(tree.children[1]).strip('"')
            return {"acao": "destrancar", "alvo": alvo, "senha": senha, "led": "verde"}
        case "alerta":
            return {"acao": "alerta", "led": "vermelho"}
        case _:
            raise ValueError(f"Nó desconhecido em fechadura: '{tree.data}'")
