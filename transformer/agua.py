from lark import Tree, Token


def transformer_agua(tree: Tree) -> dict:
    if isinstance(tree, Token):
        return str(tree)

    match tree.data:
        case "comando_agua":
            return transformer_agua(tree.children[0])

        case "dispositivo_medidor_agua":
            nome = str(tree.children[0])
            return {"acao": "dispositivo_medidor_agua", "nome": nome, "tipo": "MEDIDOR_AGUA"}

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

        case "condicional_agua":
            alvo = str(tree.children[0])
            operador = str(tree.children[1])
            valor = float(str(tree.children[2]))
            ramo_verdadeiro = transformer_agua(tree.children[3])
            ramo_falso = transformer_agua(tree.children[4])
            return {
                "acao": "condicional_agua",
                "alvo": alvo,
                "operador": operador,
                "valor": valor,
                "se_verdadeiro": ramo_verdadeiro,
                "se_falso": ramo_falso,
            }

        case _:
            raise ValueError(f"Nó desconhecido em água: '{tree.data}'")