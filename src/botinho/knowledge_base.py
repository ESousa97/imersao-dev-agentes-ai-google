"""Knowledge base and keyword maps used by Botinho."""

from __future__ import annotations

KNOWLEDGE_BASE: dict[str, dict[str, str]] = {
    "politicas_empresa": {
        "horario_trabalho": "Horário de trabalho: 8h às 18h, segunda a sexta-feira.",
        "ferias": "Política de férias: solicitar com 30 dias de antecedência via sistema interno.",
        "home_office": "Home office: até 2 dias por semana com aprovação do gestor.",
        "equipamentos": "Equipamentos corporativos: devolução obrigatória no desligamento.",
    },
    "procedimentos_ti": {
        "reset_senha": (
            "Reset de senha: acesse o portal, clique em 'Esqueci minha senha' "
            "e valide o e-mail corporativo."
        ),
        "solicitacao_acessos": (
            "Solicitação de acessos: abra um ticket no catálogo de serviços "
            "e inclua justificativa do gestor."
        ),
        "backup": (
            "Backup corporativo: execução automática diária às 2h "
            "com restauração sob demanda via TI."
        ),
        "vpn": "VPN: obrigatória para acesso remoto aos sistemas internos da empresa.",
    },
    "problemas_tecnicos": {
        "wifi": (
            "Wi-Fi: reinicie o roteador, valide cabos e teste em outro "
            "dispositivo antes de acionar o TI."
        ),
        "email_lento": (
            "E-mail lento: limpe itens enviados/lixeira e reabra o cliente "
            "após sincronização."
        ),
        "impressora": "Impressora: confira papel, nível de tinta e reinicie o dispositivo.",
        "sistema_lento": (
            "Sistema lento: feche aplicações em excesso, reinicie o computador "
            "e valide espaço em disco."
        ),
    },
}

CATEGORY_KEYWORDS: dict[str, set[str]] = {
    "politicas_empresa": {
        "horario",
        "trabalho",
        "férias",
        "ferias",
        "home office",
        "equipamento",
        "política",
        "politica",
    },
    "procedimentos_ti": {
        "senha",
        "acesso",
        "ticket",
        "backup",
        "vpn",
        "portal",
    },
    "problemas_tecnicos": {
        "wifi",
        "wi-fi",
        "internet",
        "email",
        "impressora",
        "lento",
        "travando",
        "erro",
    },
}

SYNONYMS: dict[str, set[str]] = {
    "senha": {"password", "login", "logon"},
    "wifi": {"rede", "conexao", "conexão", "internet"},
    "email": {"e-mail", "correio", "outlook"},
    "impressora": {"printer", "imprimir"},
    "sistema_lento": {"pc lento", "computador lento", "maquina lenta", "máquina lenta"},
}
