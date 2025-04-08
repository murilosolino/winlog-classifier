import random
from datetime import datetime, timedelta

# Configurações
NUM_LOGS = 500  # Quantidade de logs
FILE_NAME = "massive_logs_windows.txt" #nome do arquivo criado

# Fontes de aplicativos/serviços
fontes = [
    "Serviço de Backup",
    "Gerenciador de Atualizações",
    "Segurança do Sistema",
    "Aplicativo Financeiro",
    "Servidor de Banco de Dados",
    "Interface de Rede",
    "Monitor de Desempenho",
    "Serviço de Autenticação",
    "Player de Mídia",
    "Navegador Web",
    "Antivirus",
    "Serviço de Email",
    "Ferramenta de Diagnóstico"
]

# Tipos de eventos e descrições associadas
descricoes = {
    "Erro": [
        "Falha na inicialização do serviço",
        "Acesso não autorizado detectado",
        "Espaço em disco crítico (apenas {percent}% livre)",
        "Conexão de rede interrompida",
        "Falha na autenticação do usuário: {user}",
        "Corrupção de dados no arquivo: {file}"
    ],
    "Aviso": [
        "Tentativa de login suspeita de {ip}",
        "Uso de CPU acima de 85%",
        "Atualização pendente há mais de 30 dias",
        "Configuração de segurança não padrão",
        "Latência alta na rede: {ms}ms"
    ],
    "Informação": [
        "Backup concluído com sucesso",
        "Novo dispositivo conectado: {device}",
        "Usuário {user} logou com sucesso",
        "Atualização {version} instalada",
        "Operação concluída em {time}s"
    ]
}

# Gerar logs
with open(FILE_NAME, "w", encoding="utf-8") as file:
    base_time = datetime.now() - timedelta(days=30)
    
    for _ in range(NUM_LOGS):
        # Gerar dados variados
        fonte = random.choice(fontes)
        tipo_evento = random.choice(list(descricoes.keys()))
        descricao = random.choice(descricoes[tipo_evento])
        
        # Adicionar variáveis dinâmicas
        dynamic_vars = {
            "percent": random.randint(1, 10),
            "user": f"USER-{random.randint(1000, 9999)}",
            "file": f"arquivo_{random.randint(1, 100)}.db",
            "ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "ms": random.randint(150, 2000),
            "device": random.choice(["USB", "HD_Externo", "Impressora"]),
            "version": f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
            "time": random.randint(2, 3600)
        }
        
        # Formatar descrição
        descricao_formatada = descricao.format(**dynamic_vars)
        
        # Gerar timestamp
        base_time += timedelta(seconds=random.randint(30, 300))
        timestamp = base_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Gerar ID de evento baseado no tipo
        id_evento = {
            "Erro": random.randint(1000, 1999),
            "Aviso": random.randint(2000, 2999),
            "Informação": random.randint(3000, 3999)
        }[tipo_evento]
        
        # Escrever no arquivo
        file.write(
            f"Data: {timestamp}\n"
            f"Fonte: {fonte}\n"
            f"ID do Evento: {id_evento}\n"
            f"Descrição: {descricao_formatada}\n\n"
        )

print(f"Arquivo {FILE_NAME} gerado com {NUM_LOGS} logs sintéticos!")