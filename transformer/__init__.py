from transformer.transformer_fechadura import transformer_fechadura
from transformer.transformer_intdetector import transformer_intdetector
from transformer.energia import transformer_energia
from transformer.agua import transformer_agua

def transformer(tree):
    match tree.data:
        case "instrucao":
            return transformer(tree.children[0])
        case "dispositivo_fechadura" | "trancar" | "destrancar" | "alerta":
            return transformer_fechadura(tree)
        case (
            "comando_intrusao"
            | "configurar_detector"
            | "armar_detector"
            | "desarmar_detector"
            | "detectar_presenca"
            | "informar_senha"
            | "timeout_expirado"
            | "disparar_alarme"
            | "definir_hora_funcionamento"
        ):
            return transformer_intdetector(tree)
        case "device":
            nome = str(tree.children[0])
            tipo_device = transformer(tree.children[1])
            campos = [transformer(c) for c in tree.children[2:]]
            return {
                "acao": "declarar_device",
                "nome": nome,
                "tipo_device": tipo_device,
                "campos": campos,
            }
        case "tipo":
            return str(tree.children[0])
        case "campo":
            tipo_campo = str(tree.children[0])
            nome_campo = str(tree.children[1])
            return {"tipo": tipo_campo, "nome": nome_campo}
        case "valor":
            valor = tree.children[0]
            if valor.type == "TEXTO":
                return {"tipo": "string", "valor": str(valor).strip('"')}
            elif valor.type == "NUMERO":
                texto_num = str(valor)
                num = float(texto_num) if "." in texto_num else int(texto_num)
                return {"tipo": "numero", "valor": num}
            else:
                raise ValueError(f"Tipo de valor desconhecido: {valor.type}")
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
        case "start":
            return [transformer(filho) for filho in tree.children]
        case _:
            raise ValueError(f"Nó desconhecido na árvore: '{tree.data}'")
