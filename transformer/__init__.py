from transformer.transformer_fechadura import transformer_fechadura

def transformer(tree):
    match tree.data:
        case "instrucao":
            return transformer(tree.children[0])
        case "dispositivo_fechadura" | "trancar" | "destrancar" | "alerta":
            return transformer_fechadura(tree)
        # outros casos...
        case "valor":
            valor = tree.children[0]
            if valor.type == "STRING":
                return {"tipo": "string", "valor": str(valor).strip('"')}
            elif valor.type == "NUMERO":
                return {"tipo": "numero", "valor": int(str(valor))}
        case "condicional":
            alvo = str(tree.children[0])
            comparador = str(tree.children[1])
            valor = transformer(tree.children[2])
            se = transformer(tree.children[3])
            senao = transformer(tree.children[4])
            return {
                "acao": "condicional",
                "alvo": alvo,
                "comparador": comparador,
                "valor": valor,
                "se": se,
                "senao": senao,
            }
        case "bloco":
            return [transformer(c) for c in tree.children]
        case "comando":
            return transformer(tree.children[0])
        case "start":
            return [transformer(filho) for filho in tree.children]
        case _:
            raise ValueError(f"Nó desconhecido na árvore: '{tree.data}'")