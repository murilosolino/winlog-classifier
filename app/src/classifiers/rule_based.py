
def classify_log(id_evento):
    """
    Classifica logs com base em intervalos de ID.
    Se não reconhecido, retorna 'Desconhecido'
    """
    id_evento = int(id_evento)  # garantir tipo correto

    # Intervalos fictícios (pode ajustar para mais realismo)
    if (1000 <= id_evento <= 1199) or (5000 <= id_evento <= 5199):
        return 'Crítico'
    elif (2000 <= id_evento <= 2199) or (5200 <= id_evento <= 5399):
        return 'Suspeito'
    elif (3000 <= id_evento <= 3999) or (5400 <= id_evento <= 5599):
        return 'Normal'
    else:
        return 'Desconhecido'