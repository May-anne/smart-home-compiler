from lark import Tree, Token

def transformer_luminosidade(tree: Tree) -> dict:
    if isinstance(tree, Token):
        return str(tree)

    match tree.data:
        case "comando_luminosidade":
            return transformer_luminosidade(tree.children[0])

        case "dispositivo_dimmer":
            nome = str(tree.children[0])
            return {"acao": "dispositivo_dimmer", "nome": nome}

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

        case "condicional_luminosidade":
            alvo = str(tree.children[0])
            operador = str(tree.children[1])
            valor = float(str(tree.children[2]))
            ramo_verdadeiro = transformer_luminosidade(tree.children[3])
            ramo_falso = transformer_luminosidade(tree.children[4])
            return {
                "acao": "condicional_luminosidade",
                "alvo": alvo,
                "operador": operador,
                "valor": valor,
                "se_verdadeiro": ramo_verdadeiro,
                "se_falso": ramo_falso,
            }

        case _:
            raise ValueError(f"Nó desconhecido em luminosidade: '{tree.data}'")