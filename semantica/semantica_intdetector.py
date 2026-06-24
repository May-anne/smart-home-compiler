from semantica.utils import checar_declaracao

def semantica_intdetector(node, declarados):
    match node["acao"]:
        case "configurar_detector":
            checar_declaracao(node["alvo"], "INTDETECTOR", declarados)

            timeout = node["timeout"]
            if timeout <= 0:
                raise Exception("O timeout do detector deve ser maior que zero.")
            if not timeout.is_integer():
                raise Exception("O timeout do detector deve ser um número inteiro.")
            node["timeout"] = int(timeout)

            if not node["codigo"]:
                raise Exception("O código do detector não pode ser vazio.")

            node["tipo"] = "void"

        case (
            "armar_detector"
            | "desarmar_detector"
            | "detectar_presenca"
            | "timeout_expirado"
            | "disparar_alarme"
        ):
            checar_declaracao(node["alvo"], "INTDETECTOR", declarados)
            node["tipo"] = "void"

        case "informar_senha":
            checar_declaracao(node["alvo"], "INTDETECTOR", declarados)
            if not node["senha"]:
                raise Exception("A senha informada não pode ser vazia.")
            node["tipo"] = "void"

        case "definir_hora_funcionamento":
            checar_declaracao(node["alvo"], "INTDETECTOR", declarados)
            if node["hora_inicio"] == node["hora_fim"]:
                raise Exception(
                    "O início e o fim do horário de funcionamento devem ser diferentes."
                )
            node["tipo"] = "void"

        case _:
            raise Exception(
                f"Nó desconhecido no detector de intrusão: '{node['acao']}'"
            )
