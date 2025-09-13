import random
from datetime import datetime, timedelta

# Configurações
NUM_LOGS = 1000
FILE_NAME = "massive_logs_windows.txt"

fontes = [
    "Serviço de Backup", "Gerenciador de Atualizações", "Segurança do Sistema",
    "Aplicativo Financeiro", "Servidor de Banco de Dados", "Interface de Rede",
    "Monitor de Desempenho", "Serviço de Autenticação", "Player de Mídia",
    "Navegador Web", "Antivirus", "Serviço de Email", "Ferramenta de Diagnóstico"
]

descricoes = {
    "Erro": [
        "Erro fatal no módulo de kernel",
        "Falha na inicialização do serviço",
        "Acesso negado ao recurso crítico",
        "Serviço encerrado inesperadamente",
        "Memória insuficiente para concluir operação",
        "Falha na autenticação do usuário: {user}",
        "Kernel panic detectado no processo",
        "BSOD registrado durante execução do sistema",
        "Corrupção de dados no arquivo: {file}"
    ],
    "Aviso": [
        "Tentativa de login suspeita de {ip}",
        "Comportamento anômalo detectado na porta {porta}",
        "Atualização pendente há mais de 30 dias",
        "Dispositivo não reconhecido conectado: {device}",
        "Alteração de configuração do sistema detectada",
        "Reiniciado após travamento não documentado",
        "Latência alta na rede: {ms}ms",
        "Mudança de permissões em arquivo sensível: {file}"
    ],
    "Informação": [
        "Backup concluído com sucesso",
        "Novo dispositivo conectado: {device}",
        "Usuário {user} logou com sucesso",
        "Atualização {version} instalada",
        "Operação concluída em {time}s",
        "Serviço de diagnóstico executado sem erros",
        "Verificação automática finalizada com êxito"
    ]
}

# Função auxiliar para gerar ID de evento
def gerar_id_evento(tipo_evento, conhecido=True):
    if conhecido:
        if tipo_evento == "Erro":
            return random.choice([random.randint(2200, 2299), random.randint(5000, 5099)])
        elif tipo_evento == "Aviso":
            return random.choice([random.randint(3000, 3099), random.randint(7000, 7099)])
        elif tipo_evento == "Informação":
            return random.choice([random.randint(1000, 1099), random.randint(4000, 4099)])
    else:
        # Gera ID fora de todos os intervalos conhecidos
        while True:
            id_candidato = random.randint(1000, 9999)
            if not (
                2200 <= id_candidato <= 2299 or 5000 <= id_candidato <= 5099 or
                3000 <= id_candidato <= 3099 or 7000 <= id_candidato <= 7099 or
                1000 <= id_candidato <= 1099 or 4000 <= id_candidato <= 4099
            ):
                return id_candidato

# Geração dos logs
with open(FILE_NAME, "w", encoding="utf-8") as file:
    base_time = datetime.now() - timedelta(days=30)

    for _ in range(NUM_LOGS):
        fonte = random.choice(fontes)
        tipo_evento = random.choice(list(descricoes.keys()))
        descricao = random.choice(descricoes[tipo_evento])

        dynamic_vars = {
            "percent": random.randint(1, 10),
            "user": f"USER-{random.randint(1000, 9999)}",
            "file": f"arquivo_{random.randint(1, 100)}.db",
            "ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "ms": random.randint(150, 2000),
            "device": random.choice(["USB", "HD_Externo", "Impressora"]),
            "version": f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
            "time": random.randint(2, 3600),
            "porta": random.randint(1000, 65535)
        }

        descricao_formatada = descricao.format(**dynamic_vars)

        base_time += timedelta(seconds=random.randint(30, 300))
        timestamp = base_time.strftime("%Y-%m-%d %H:%M:%S")

        # Decide se o ID será conhecido ou não
        conhecido = random.random() < 0.3  # 30% dos logs com ID conhecido
        id_evento = gerar_id_evento(tipo_evento, conhecido=conhecido)

        file.write(
            f"Data: {timestamp}\n"
            f"Fonte: {fonte}\n"
            f"ID do Evento: {id_evento}\n"
            f"Descrição: {descricao_formatada}\n\n"
        )

print(f"✅ Arquivo {FILE_NAME} gerado com {NUM_LOGS} logs mistos (conhecidos e desconhecidos).")