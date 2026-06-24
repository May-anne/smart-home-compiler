from gramatica.base import GRAMATICA_COMPLETA

linhas = GRAMATICA_COMPLETA.split("\n")
for i, linha in enumerate(linhas, start=1):
    if 58 <= i <= 68:
        print(f"{i}: {linha}")