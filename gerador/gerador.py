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
    ind  = "    " * nivel
    ind1 = "    " * (nivel + 1)

    match node["acao"]:

        case "dispositivo":
            tipo_orig = (declarados or {}).get(node["nome"], node["tipo"])
            tipo_cpp  = MAPA_TIPOS.get(tipo_orig, tipo_orig)
            return f"{ind}{tipo_cpp} {node['nome']};"

        case "definir_temperatura":
            return f"{ind}{node['alvo']}.setTemperatura({node['valor']});"

        case "ler_temperatura":
            return f"{ind}{node['alvo']}.lerTemperatura();"

        case "alerta_temperatura":
            return f'{ind}std::cout << "[TEMP] {node["mensagem"]}" << std::endl;'

        case "condicional_temperatura":
            op    = MAPA_COMPARADORES[node["operador"]]
            se    = gerar_cpp(node["se_verdadeiro"], nivel + 1, declarados)
            senao = gerar_cpp(node["se_falso"],      nivel + 1, declarados)
            return (
                f"{ind}if ({node['alvo']}.getTemperatura() {op} {node['valor']}) {{\n"
                f"{se}\n{ind}}} else {{\n{senao}\n{ind}}}"
            )

        case "definir_luminosidade":
            return f"{ind}{node['alvo']}.setLuminosidade({node['valor']});"

        case "ler_luminosidade":
            return f"{ind}{node['alvo']}.lerLuminosidade();"

        case "alerta_luminosidade":
            return f'{ind}std::cout << "[LUZ] {node["mensagem"]}" << std::endl;'

        case "condicional_luminosidade":
            op    = MAPA_COMPARADORES[node["operador"]]
            se    = gerar_cpp(node["se_verdadeiro"], nivel + 1, declarados)
            senao = gerar_cpp(node["se_falso"],      nivel + 1, declarados)
            return (
                f"{ind}if ({node['alvo']}.getLuminosidade() {op} {node['valor']}) {{\n"
                f"{se}\n{ind}}} else {{\n{senao}\n{ind}}}"
            )

        case "trancar":
            return f"{ind}{node['nome']}.trancar();"

        case "destrancar":
            return (
                f"{ind}{node['nome']}.destrancar();\n"
                f"{ind1}// LED: {node['led']}"
            )

        case "alerta":
            return f"{ind}// LED: {node['led']}"
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

        case "condicional_energia":
            op    = MAPA_COMPARADORES[node["operador"]]
            se    = gerar_cpp(node["se_verdadeiro"], nivel + 1, declarados)
            senao = gerar_cpp(node["se_falso"],      nivel + 1, declarados)
            return (
                f"{ind}if ({node['alvo']}.getConsumo() {op} {node['valor']}) {{\n"
                f"{se}\n{ind}}} else {{\n{senao}\n{ind}}}"
            )

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
        
        case "informar_senha_fechadura":
            return f"{ind}{node['nome']}.informarSenha(\"{node['senha']}\");"

        case "condicional_agua":
            op    = MAPA_COMPARADORES[node["operador"]]
            se    = gerar_cpp(node["se_verdadeiro"], nivel + 1, declarados)
            senao = gerar_cpp(node["se_falso"],      nivel + 1, declarados)
            return (
                f"{ind}if ({node['alvo']}.getConsumo() {op} {node['valor']}) {{\n"
                f"{se}\n{ind}}} else {{\n{senao}\n{ind}}}"
            )

        case "condicional":
            op     = MAPA_COMPARADORES[node["comparador"]]
            valor  = node["valor"]["valor"]
            if node["valor"]["tipo"] == "string":
                valor = f'"{valor}"'
            tipo   = (declarados or {}).get(node["alvo"], "")
            metodo = MAPA_METODOS.get(tipo, "getValor()")
            linhas_se    = "\n".join(gerar_cpp(i, nivel + 1, declarados) for i in node["se"])
            linhas_senao = "\n".join(gerar_cpp(i, nivel + 1, declarados) for i in node["senao"])
            return (
                f"{ind}if ({node['alvo']}.{metodo} {op} {valor}) {{\n"
                f"{linhas_se}\n{ind}}} else {{\n{linhas_senao}\n{ind}}}"
            )

        case _:
            raise ValueError(f"Nó desconhecido no gerador C++: '{node['acao']}'")


def gerar_programa(nos, declarados=None):
    linhas = [
        '#include "SmartHome.h"',
        "#include <iostream>\n",
        "int main() {",
    ]
    for no in nos:
        linhas.append(gerar_cpp(no, nivel=1, declarados=declarados))
    linhas += ["", "    return 0;", "}"]
    return "\n".join(linhas)