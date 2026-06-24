from lark import Token, Tree


def transformer_intdetector(tree: Tree) -> dict:
    if isinstance(tree, Token):
        return str(tree)

    match tree.data:
        case "comando_intrusao":
            return transformer_intdetector(tree.children[0])

        case "configurar_detector":
            alvo = str(tree.children[0])
            timeout = float(str(tree.children[1]))
            codigo = str(tree.children[2]).strip('"')
            return {
                "acao": "configurar_detector",
                "alvo": alvo,
                "timeout": timeout,
                "codigo": codigo,
            }

        case "armar_detector":
            return {"acao": "armar_detector", "alvo": str(tree.children[0])}

        case "desarmar_detector":
            return {"acao": "desarmar_detector", "alvo": str(tree.children[0])}

        case "detectar_presenca":
            return {"acao": "detectar_presenca", "alvo": str(tree.children[0])}

        case "informar_senha":
            alvo = str(tree.children[0])
            senha = str(tree.children[1]).strip('"')
            return {"acao": "informar_senha", "alvo": alvo, "senha": senha}

        case "timeout_expirado":
            return {"acao": "timeout_expirado", "alvo": str(tree.children[0])}

        case "disparar_alarme":
            return {"acao": "disparar_alarme", "alvo": str(tree.children[0])}

        case "definir_hora_funcionamento":
            return {
                "acao": "definir_hora_funcionamento",
                "alvo": str(tree.children[0]),
                "hora_inicio": str(tree.children[1]),
                "hora_fim": str(tree.children[2]),
            }

        case _:
            raise ValueError(
                f"Nó desconhecido no detector de intrusão: '{tree.data}'"
            )
