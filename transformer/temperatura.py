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

        case "condicional_temperatura":
            alvo = str(tree.children[0])
            operador = str(tree.children[1])
            valor = float(str(tree.children[2]))
            ramo_verdadeiro = transformer_temperatura(tree.children[3])
            ramo_falso = transformer_temperatura(tree.children[4])
            return {
                "acao": "condicional_temperatura",
                "alvo": alvo,
                "operador": operador,
                "valor": valor,
                "se_verdadeiro": ramo_verdadeiro,
                "se_falso": ramo_falso,
            }

        case _:
            raise ValueError(f"Nó desconhecido em temperatura: '{tree.data}'")