from lark import Tree

def transformer_fechadura(tree: Tree):
    match tree.data:
        case "comando_fechadura":
            return transformer_fechadura(tree.children[0])
        
        case "informar_senha_fechadura":
            nome = str(tree.children[0])
            senha = str(tree.children[1]).strip('"')
            return {"acao": "informar_senha_fechadura", "nome": nome, "senha": senha}
        
        case "trancar":
            nome = str(tree.children[0])
            return {"acao": "trancar", "nome": nome}
        
        case "destrancar":
            nome = str(tree.children[0])
            return {"acao": "destrancar", "nome": nome, "led": "verde"}
        
        case "alerta":
            return {"acao": "alerta", "led": "vermelho"}
        
        case _:
            raise ValueError(f"Nó desconhecido em fechadura: '{tree.data}'")