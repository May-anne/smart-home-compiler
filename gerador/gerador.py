MAPA_TIPOS = {
    "TERMOSTATO":      "Termostato",
    "DIMMER":          "Dimmer",
    "FECHADURA":       "Fechadura",
    "INTDETECTOR":     "DetectorIntrusao",
    "MEDIDOR_ENERGIA": "MedidorEnergia",
    "MEDIDOR_AGUA":    "MedidorAgua",
}

MAPA_COMPARADORES = {
    ">": ">", "<": "<", ">=": ">=", "<=": "<=", "==": "==", "!=": "!=",
}

MAPA_METODOS = {
    "TERMOSTATO":      "getTemperatura()",
    "DIMMER":          "getLuminosidade()",
    "MEDIDOR_ENERGIA": "getConsumo()",
    "MEDIDOR_AGUA":    "getConsumo()",
    "FECHADURA":       "getEstado()",
    "INTDETECTOR":     "getEstado()",
}


def gerar_cpp(node, nivel=0, declarados=None):
    ind = "    " * nivel

    match node["acao"]:

        case "dispositivo":
            # A semântica sobrescreve node["tipo"] com "void"; o tipo original
            # deve ser lido de node["tipo_original"], que o transformer preserva.
            tipo_orig = node.get("tipo_original")
            if tipo_orig is None:
                raise ValueError(
                    f"Dispositivo '{node['nome']}' não possui 'tipo_original'. "
                    "Verifique se o transformer está preenchendo esse campo."
                )
            tipo_cpp = MAPA_TIPOS.get(tipo_orig)
            if tipo_cpp is None:
                raise ValueError(
                    f"Tipo de dispositivo desconhecido no gerador: '{tipo_orig}'."
                )
            return f"{ind}{tipo_cpp} {node['nome']};"

        case "definir_temperatura":
            return f"{ind}{node['alvo']}.setTemperatura({node['valor']});"

        case "ler_temperatura":
            return f"{ind}{node['alvo']}.lerTemperatura();"

        case "alerta_temperatura":
            return f'{ind}std::cout << "[TEMP] {node["mensagem"]}" << std::endl;'

        case "definir_luminosidade":
            return f"{ind}{node['alvo']}.setLuminosidade({node['valor']});"

        case "ler_luminosidade":
            return f"{ind}{node['alvo']}.lerLuminosidade();"

        case "alerta_luminosidade":
            return f'{ind}std::cout << "[LUZ] {node["mensagem"]}" << std::endl;'

        case "informar_senha_fechadura":
            return f"{ind}{node['nome']}.informarSenha(\"{node['senha']}\");"

        case "trancar":
            return f"{ind}{node['nome']}.trancar();"

        case "destrancar":
            return f"{ind}{node['nome']}.destrancar();"

        case "alerta":
            return f'{ind}std::cout << "[FECHADURA] Alerta de segurança." << std::endl;'
        case "configurar_detector":
            return f"{ind}{node['alvo']}.configurar({node['timeout']}, \"{node['codigo']}\");"

        case "armar_detector":
            return f"{ind}{node['alvo']}.armar();"

        case "desarmar_detector":
            return f"{ind}{node['alvo']}.desarmar();"

        case "detectar_presenca":
            return f"{ind}{node['alvo']}.detectarPresenca();"

        case "informar_senha":
            return f"{ind}{node['alvo']}.informarSenha(\"{node['senha']}\");"

        case "timeout_expirado":
            return f"{ind}{node['alvo']}.timeoutExpirado();"

        case "disparar_alarme":
            return f"{ind}{node['alvo']}.dispararAlarme();"

        case "definir_hora_funcionamento":
            return (
                f"{ind}{node['alvo']}.setHorario"
                f"(\"{node['hora_inicio']}\", \"{node['hora_fim']}\");"
            )

        case "definir_limite_energia":
            return f"{ind}{node['alvo']}.setLimite({node['valor']});"

        case "registrar_consumo_energia":
            return f"{ind}{node['alvo']}.registrarConsumo({node['valor']});"

        case "ler_consumo_energia":
            return f"{ind}{node['alvo']}.lerConsumo();"

        case "resetar_consumo_energia":
            return f"{ind}{node['alvo']}.resetarConsumo();"

        case "alerta_energia":
            return f'{ind}std::cout << "[ENERGIA] {node["mensagem"]}" << std::endl;'

        case "definir_limite_agua":
            return f"{ind}{node['alvo']}.setLimite({node['valor']});"

        case "registrar_consumo_agua":
            return f"{ind}{node['alvo']}.registrarConsumo({node['valor']});"

        case "ler_consumo_agua":
            return f"{ind}{node['alvo']}.lerConsumo();"

        case "resetar_consumo_agua":
            return f"{ind}{node['alvo']}.resetarConsumo();"

        case "alerta_agua":
            return f'{ind}std::cout << "[AGUA] {node["mensagem"]}" << std::endl;'
        
        case "repetir":
            corpo = "\n".join(gerar_cpp(i, nivel + 1, declarados) for i in node["corpo"])
            return (
                f"{ind}for (int _i = 0; _i < {node['vezes']}; _i++) {{\n"
                f"{corpo}\n{ind}}}"
            )

        case "cena":
            nome_func = "cena_" + node["nome"].replace(" ", "_").replace("-", "_")
            corpo = "\n".join(gerar_cpp(i, nivel + 1, declarados) for i in node["corpo"])
            return (
                f"{ind}auto {nome_func} = [&]() {{\n"
                f"{corpo}\n{ind}}};\n"
                f"{ind}{nome_func}();"
            )

        case "agendar":
            cmd_cpp = gerar_cpp(node["comando"], nivel + 1, declarados)
            return (
                f"{ind}agendarTarefa(\"{node['hora']}\", [&]() {{\n"
                f"{cmd_cpp}\n{ind}}});"
            )

        case "condicional":
            op    = MAPA_COMPARADORES[node["comparador"]]
            valor = node["valor"]["valor"]
            if node["valor"]["tipo"] == "string":
                valor = f'"{valor}"'
            tipo = (declarados or {}).get(node["alvo"])
            if tipo is None:
                raise ValueError(
                    f"Alvo '{node['alvo']}' não encontrado em declarados. "
                    "Certifique-se de passar declarados para gerar_cpp."
                )
            metodo = MAPA_METODOS.get(tipo)
            if metodo is None:
                raise ValueError(
                    f"Tipo '{tipo}' do alvo '{node['alvo']}' não possui método "
                    "de acesso mapeado em MAPA_METODOS."
                )
            linhas_se    = "\n".join(gerar_cpp(i, nivel + 1, declarados) for i in node["se"])
            linhas_senao = "\n".join(gerar_cpp(i, nivel + 1, declarados) for i in node["senao"])
            return (
                f"{ind}if ({node['alvo']}.{metodo} {op} {valor}) {{\n"
                f"{linhas_se}\n{ind}}} else {{\n{linhas_senao}\n{ind}}}"
            )

        case _:
            raise ValueError(f"Nó desconhecido no gerador C++: '{node['acao']}'")


def gerar_programa(nos, declarados=None):
    # declarados: dict nome -> tipo, necessário para gerar condicionais corretamente.
    # Para dispositivos, o tipo é lido de node["tipo_original"] (preenchido pelo transformer).
    linhas = [
        '#include "SmartHome.h"',
        "#include <iostream>\n",
        "int main() {",
    ]
    for no in nos:
        linhas.append(gerar_cpp(no, nivel=1, declarados=declarados))
    linhas += ["", "    return 0;", "}"]
    return "\n".join(linhas)