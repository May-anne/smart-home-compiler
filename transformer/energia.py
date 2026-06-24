from lark import Tree, Token


def transformer_energia(tree: Tree) -> dict:
    if isinstance(tree, Token):
        return str(tree)

    match tree.data:
        case "comando_energia":
            return transformer_energia(tree.children[0])

        case "dispositivo_medidor_energia":
            nome = str(tree.children[0])
            return {"acao": "dispositivo_medidor_energia", "nome": nome, "tipo": "MEDIDOR_ENERGIA"}

        case "definir_limite_energia":
            alvo = str(tree.children[0])
            valor = float(str(tree.children[1]))
            return {"acao": "definir_limite_energia", "alvo": alvo, "valor": valor}

        case "registrar_consumo_energia":
            alvo = str(tree.children[0])
            valor = float(str(tree.children[1]))
            return {"acao": "registrar_consumo_energia", "alvo": alvo, "valor": valor}

        case "ler_consumo_energia":
            alvo = str(tree.children[0])
            return {"acao": "ler_consumo_energia", "alvo": alvo}

        case "resetar_consumo_energia":
            alvo = str(tree.children[0])
            return {"acao": "resetar_consumo_energia", "alvo": alvo}

        case "alerta_energia":
            mensagem = str(tree.children[0]).strip('"')
            return {"acao": "alerta_energia", "mensagem": mensagem}

        case "condicional_energia":
            alvo = str(tree.children[0])
            operador = str(tree.children[1])
            valor = float(str(tree.children[2]))
            ramo_verdadeiro = transformer_energia(tree.children[3])
            ramo_falso = transformer_energia(tree.children[4])
            return {
                "acao": "condicional_energia",
                "alvo": alvo,
                "operador": operador,
                "valor": valor,
                "se_verdadeiro": ramo_verdadeiro,
                "se_falso": ramo_falso,
            }

        case _:
            raise ValueError(f"Nó desconhecido em energia: '{tree.data}'")