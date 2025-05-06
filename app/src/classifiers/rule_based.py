def classify_log(descricao):
    """
    CLASSIFICAÇÃO INICIAL (BASE PARA TREINO)
    Regras básicas para criar labels:
    - Crítico: contém palavras como 'erro', 'falha'
    - Suspeito: contém 'atualização', 'reinicio'
    - Normal: outros casos
    """
    criticas = ['erro', 'falhou', 'insuficiente', 'encerrado']
    suspeitas = ['atualização', 'reiniciado', 'pausado']
    
    if any(word in descricao.lower() for word in criticas):
        return 'Crítico'
    elif any(word in descricao.lower() for word in suspeitas):
        return 'Suspeito'
    return 'Normal'