from lark import Tree

def transformer_fechadura(tree: Tree):
    match tree.data:
        case "dispositivo_fechadura":
            nome = str(tree.children[0])
            return {"nome":nome, "tipo":"FECHADURA"}
        case "trancar":
            alvo = str(tree.children[0])
            return {"acao": "trancar", "alvo": alvo}
        case "destrancar":
            alvo = str(tree.children[0])
            senha = str(tree.children[1]).strip('"')
            return {"acao": "destrancar", "alvo": alvo, "senha": senha}
        case "alerta":
            mensagem = str(tree.children[0]).strip('"')
            return {"acao": "alerta", "mensagem": mensagem}
        case "verificar_senha":
            alvo = str(tree.children[0])
            senha = str(tree.children[1]).strip('"')
            se_verdadeiro = transformer_fechadura(tree.children[2])
            se_falso = transformer_fechadura(tree.children[3])
            return {
                "acao": "verificar_senha",
                "alvo": alvo,
                "senha": senha,
                "se_verdadeiro": se_verdadeiro,
                "se_falso": se_falso,
            }
        case _:
            raise ValueError(f"Nó desconhecido em fechadura: '{tree.data}'")
