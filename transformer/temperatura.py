# transformer/temperatura.py
#
# Converte a Parse Tree gerada pelo Lark em dicionários Python estruturados
# (a AST do compilador) para o módulo de temperatura.
#
# Cada função match converte um nó da árvore Lark em um dicionário com
# a chave "tipo_no" identificando o tipo do nó e as demais chaves
# carregando os atributos relevantes para as etapas seguintes.
#
# Pipeline:
#   Parse Tree (Lark)  →  transformer_temperatura()  →  dict Python

from lark import Tree, Token


def transformer_temperatura(tree: Tree) -> dict:
    """
    Ponto de entrada do transformer de temperatura.

    Recebe um nó Tree do Lark e retorna um dicionário Python representando
    aquele nó na AST. Chama a si mesmo recursivamente nos filhos.

    Parâmetros:
        tree: Nó da árvore sintática produzida pelo Lark.

    Retorna:
        Dicionário com "tipo_no" e os atributos do comando.

    Levanta:
        ValueError se a regra do nó não pertence à gramática de temperatura.
    """
    # Segurança: se recebermos um Token puro, retorna como string
    if isinstance(tree, Token):
        return str(tree)

    regra = tree.data

    # ─── Regra guarda-chuva ───────────────────────────────────────────────────
    # comando_temperatura apenas encapsula um dos outros nós.
    # Delega diretamente para o filho.
    if regra == "comando_temperatura":
        return transformer_temperatura(tree.children[0])

    # ─── Declaração de dispositivo ────────────────────────────────────────────
    # Exemplo: DISPOSITIVO sala : TERMOSTATO
    # tree.children: [Token(IDENTIFICADOR, 'sala')]
    elif regra == "dispositivo_termostato":
        nome = str(tree.children[0])
        return {
            "tipo_no": "dispositivo_termostato",
            "nome": nome,
        }

    # ─── Definir temperatura ──────────────────────────────────────────────────
    # Exemplo: DEFINIR_TEMPERATURA sala PARA 22
    # tree.children: [Token(IDENTIFICADOR, 'sala'), Token(NUMERO, '22')]
    elif regra == "definir_temperatura":
        alvo = str(tree.children[0])
        valor = float(str(tree.children[1]))
        return {
            "tipo_no": "definir_temperatura",
            "alvo": alvo,
            "valor": valor,
        }

    # ─── Ler temperatura ──────────────────────────────────────────────────────
    # Exemplo: LER_TEMPERATURA sala
    # tree.children: [Token(IDENTIFICADOR, 'sala')]
    elif regra == "ler_temperatura":
        alvo = str(tree.children[0])
        return {
            "tipo_no": "ler_temperatura",
            "alvo": alvo,
        }

    # ─── Alerta de temperatura ────────────────────────────────────────────────
    # Exemplo: ALERTA "Temperatura elevada!"
    # tree.children: [Token(TEXTO, '"Temperatura elevada!"')]
    # O .strip('"') remove as aspas que o Lark inclui no token TEXTO.
    elif regra == "alerta_temperatura":
        mensagem = str(tree.children[0]).strip('"')
        return {
            "tipo_no": "alerta_temperatura",
            "mensagem": mensagem,
        }

    # ─── Condicional de temperatura ───────────────────────────────────────────
    # Exemplo:
    #   SE sala > 25 ENTAO
    #       DEFINIR_TEMPERATURA sala PARA 20
    #   SENAO
    #       ALERTA "Temperatura ok"
    #   FIM
    #
    # tree.children (após filtragem de literais anônimas pelo Lark):
    #   [0] Token(IDENTIFICADOR, 'sala')
    #   [1] Token(COMPARADOR, '>')
    #   [2] Token(NUMERO, '25')
    #   [3] Tree('comando_temperatura', [...])   ← ramo ENTAO
    #   [4] Tree('comando_temperatura', [...])   ← ramo SENAO
    elif regra == "condicional_temperatura":
        alvo = str(tree.children[0])
        operador = str(tree.children[1])
        valor = float(str(tree.children[2]))
        # Chamada recursiva para os dois ramos da condicional
        ramo_verdadeiro = transformer_temperatura(tree.children[3])
        ramo_falso = transformer_temperatura(tree.children[4])
        return {
            "tipo_no": "condicional_temperatura",
            "alvo": alvo,
            "operador": operador,
            "valor": valor,
            "se_verdadeiro": ramo_verdadeiro,
            "se_falso": ramo_falso,
        }

    else:
        raise ValueError(
            f"[Transformer Temperatura] Regra desconhecida: '{regra}'.\n"
            f"Verifique se este nó pertence à gramática de temperatura."
        )
