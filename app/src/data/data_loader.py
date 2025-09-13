import pandas as pd

def load_logs(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().split('\n\n')
    
    logs = []
    for entry in content:
        if entry.strip():
            log = {}
            for line in entry.split('\n'):
                if line.startswith('Data:'):
                    log['Data'] = line.split(': ', 1)[1]
                elif line.startswith('Fonte:'):
                    log['Fonte'] = line.split(': ', 1)[1]
                elif line.startswith('ID do Evento:'):
                    log['ID_Evento'] = int(line.split(': ', 1)[1])
                elif line.startswith('Descrição:'):
                    log['Descricao'] = line.split(': ', 1)[1]
            logs.append(log)
    return pd.DataFrame(logs)
