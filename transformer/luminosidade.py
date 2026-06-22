# transformer/luminosidade.py
#
# Converte a Parse Tree gerada pelo Lark em dicionários Python estruturados
# (a AST do compilador) para o módulo de luminosidade.
#
# Mesma estrutura do transformer de temperatura, adaptada para:
#   - DIMMER em vez de TERMOSTATO
#   - DEFINIR_LUMINOSIDADE / LER_LUMINOSIDADE
#   - ALERTA_LUZ em vez de ALERTA
#   - Valores são porcentagens (0–100), não graus Celsius

from lark import Tree, Token


def transformer_luminosidade(tree: Tree) -> dict:
    """
    Ponto de entrada do transformer de luminosidade.

    Recebe um nó Tree do Lark e retorna um dicionário Python representando
    aquele nó na AST. Chama a si mesmo recursivamente nos filhos.

    Parâmetros:
        tree: Nó da árvore sintática produzida pelo Lark.

    Retorna:
        Dicionário com "tipo_no" e os atributos do comando.

    Levanta:
        ValueError se a regra do nó não pertence à gramática de luminosidade.
    """
    if isinstance(tree, Token):
        return str(tree)

    regra = tree.data

    # ─── Regra guarda-chuva ───────────────────────────────────────────────────
    if regra == "comando_luminosidade":
        return transformer_luminosidade(tree.children[0])

    # ─── Declaração de dispositivo ────────────────────────────────────────────
    # Exemplo: DISPOSITIVO quarto : DIMMER
    # tree.children: [Token(IDENTIFICADOR, 'quarto')]
    elif regra == "dispositivo_dimmer":
        nome = str(tree.children[0])
        return {
            "tipo_no": "dispositivo_dimmer",
            "nome": nome,
        }

    # ─── Definir luminosidade ─────────────────────────────────────────────────
    # Exemplo: DEFINIR_LUMINOSIDADE quarto PARA 70
    # tree.children: [Token(IDENTIFICADOR, 'quarto'), Token(NUMERO, '70')]
    # O valor é armazenado como float aqui; a análise semântica valida
    # que está no intervalo [0, 100].
    elif regra == "definir_luminosidade":
        alvo = str(tree.children[0])
        valor = float(str(tree.children[1]))
        return {
            "tipo_no": "definir_luminosidade",
            "alvo": alvo,
            "valor": valor,
        }

    # ─── Ler luminosidade ─────────────────────────────────────────────────────
    # Exemplo: LER_LUMINOSIDADE quarto
    # tree.children: [Token(IDENTIFICADOR, 'quarto')]
    elif regra == "ler_luminosidade":
        alvo = str(tree.children[0])
        return {
            "tipo_no": "ler_luminosidade",
            "alvo": alvo,
        }

    # ─── Alerta de luminosidade ───────────────────────────────────────────────
    # Exemplo: ALERTA_LUZ "Luminosidade muito baixa!"
    # tree.children: [Token(TEXTO, '"Luminosidade muito baixa!"')]
    elif regra == "alerta_luminosidade":
        mensagem = str(tree.children[0]).strip('"')
        return {
            "tipo_no": "alerta_luminosidade",
            "mensagem": mensagem,
        }

    # ─── Condicional de luminosidade ──────────────────────────────────────────
    # Exemplo:
    #   SE quarto < 30 ENTAO
    #       DEFINIR_LUMINOSIDADE quarto PARA 80
    #   SENAO
    #       ALERTA_LUZ "Luminosidade adequada"
    #   FIM
    #
    # tree.children (após filtragem de literais anônimas pelo Lark):
    #   [0] Token(IDENTIFICADOR, 'quarto')
    #   [1] Token(COMPARADOR, '<')
    #   [2] Token(NUMERO, '30')
    #   [3] Tree('comando_luminosidade', [...])   ← ramo ENTAO
    #   [4] Tree('comando_luminosidade', [...])   ← ramo SENAO
    elif regra == "condicional_luminosidade":
        alvo = str(tree.children[0])
        operador = str(tree.children[1])
        valor = float(str(tree.children[2]))
        ramo_verdadeiro = transformer_luminosidade(tree.children[3])
        ramo_falso = transformer_luminosidade(tree.children[4])
        return {
            "tipo_no": "condicional_luminosidade",
            "alvo": alvo,
            "operador": operador,
            "valor": valor,
            "se_verdadeiro": ramo_verdadeiro,
            "se_falso": ramo_falso,
        }

    else:
        raise ValueError(
            f"[Transformer Luminosidade] Regra desconhecida: '{regra}'.\n"
            f"Verifique se este nó pertence à gramática de luminosidade."
        )
