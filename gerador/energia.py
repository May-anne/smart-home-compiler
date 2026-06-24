def gerar_codigo_energia(node):
    match node["acao"]:

        case "definir_limite_energia":
            print(f'{node["alvo"]}.definir_limite({node["valor"]});')

        case "registrar_consumo_energia":
            print(f'{node["alvo"]}.registrar_consumo({node["valor"]});')

        case "ler_consumo_energia":
            print(f'{node["alvo"]}.ler_consumo();')

        case "resetar_consumo_energia":
            print(f'{node["alvo"]}.resetar_consumo();')

        case "alerta_energia":
            print(f'std::cout << "[ALERTA] {node["mensagem"]}" << std::endl;')

        case "condicional_energia":
            print(f'if ({node["alvo"]}.ler_consumo() {node["operador"]} {node["valor"]}) {{')
            gerar_codigo_energia(node["se_verdadeiro"])
            print('} else {')
            gerar_codigo_energia(node["se_falso"])
            print('}')

        case _:
            raise Exception(f"Nó desconhecido em energia: '{node['acao']}'")