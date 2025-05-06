import pandas as pd

def generate_critical_alerts(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    GERA ALERTAS PARA EVENTOS CRÍTICOS
    
    Parâmetros:
    df (DataFrame): DataFrame com coluna 'Predicao_IA'
    verbose (bool): Se True, imprime os alertas no console
    
    Retorna:
    DataFrame: Alertas críticos filtrados
    """
    alertas = df[df['Predicao_IA'] == 'Crítico']
    
    if verbose:
        if not alertas.empty:
            print("\n🚨 ALERTAS CRÍTICOS DETECTADOS 🚨")
            for _, row in alertas.iterrows():
                print(f"[{row['Data']}] {row['Fonte']} - {row['Descricao']}")
        else:
            print("\n✅ Nenhum alerta crítico detectado")
    
    return alertas