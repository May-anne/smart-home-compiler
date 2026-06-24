from gerador.agua import gerar_codigo_agua
from gerador.energia import gerar_codigo_energia


def gerar(node):
    acao = node["acao"]

    match acao:
        case (
            "definir_limite_agua" | "registrar_consumo_agua"
            | "ler_consumo_agua"  | "resetar_consumo_agua"
            | "alerta_agua"       | "condicional_agua"
        ):
            gerar_codigo_agua(node)

        case (
            "definir_limite_energia" | "registrar_consumo_energia"
            | "ler_consumo_energia"  | "resetar_consumo_energia"
            | "alerta_energia"       | "condicional_energia"
        ):
            gerar_codigo_energia(node)

        case _:
            raise Exception(f"Nó desconhecido no gerador: '{acao}'")


def gerar_programa(nos: list):
    print("// Código gerado automaticamente")
    print("int main() {")
    for no in nos:
        if isinstance(no, list):
            for sub in no:
                gerar(sub)
        else:
            gerar(no)
    print("    return 0;")
    print("}")