from transformer.transformer_fechadura import transformer_fechadura
from transformer.transformer_intdetector import transformer_intdetector
from transformer.agua import transformer_agua
from transformer.energia import transformer_energia

def transformer(tree):
    match tree.data:
        case "instrucao":
            return transformer(tree.children[0])
        case "dispositivo_fechadura" | "trancar" | "destrancar" | "alerta":
            return transformer_fechadura(tree)
        case (
            "comando_intrusao"
            | "dispositivo_intrusao"
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
        case (
            "comando_agua"
            | "dispositivo_medidor_agua"
            | "definir_limite_agua"
            | "registrar_consumo_agua"
            | "ler_consumo_agua"
            | "resetar_consumo_agua"
            | "alerta_agua"
            | "condicional_agua"
        ):
            return transformer_agua(tree)
        case (
             "comando_energia"
             | "dispositivo_medidor_energia"
             | "definir_limite_energia"
             | "registrar_consumo_energia"
             | "ler_consumo_energia"
             | "resetar_consumo_energia"
             | "alerta_energia"
             | "condicional_energia"
        ):
            return transformer_energia(tree)
        
        case "device":
            nome_instancia = str(tree.children[0])
            tipo_dispositivo = transformer(tree.children[1])  
            campos = [transformer(c) for c in tree.children[2:]] 
            return {
                "acao": "dispositivo",
                "nome": nome_instancia,
                "tipo": tipo_dispositivo,
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