def checar_declaracao(nome, tipo_esperado, declarados):
    if nome not in declarados:
        raise Exception(f"'{nome}' não foi declarado.")
    if declarados[nome] != tipo_esperado:
        raise Exception(
            f"'{nome}' é do tipo '{declarados[nome]}', mas o esperado é '{tipo_esperado}'."
        )
