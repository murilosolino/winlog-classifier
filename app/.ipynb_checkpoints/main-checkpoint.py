# -*- coding: utf-8 -*-
"""
SISTEMA DE ANÁLISE DE LOGS INTELIGENTE
Fluxo principal:
1. Carrega logs brutos
2. Pré-processa o texto
3. Classifica automaticamente
4. Gera alertas e visualizações
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from src.data_loader import load_logs
from src.preprocessor import preprocess_text
from src.classifiers.rule_based import classify_log
from src.alert_system import generate_critical_alerts
from src.ml_model import aplicar_modelo_ia

nltk.download('stopwords')

# EXECUÇÃO PRINCIPAL
if __name__ == "__main__":
    # 1. CARREGAMENTO E PRÉ-PROCESSAMENTO
    df = load_logs('data/raw/massive_logs_windows.txt')
    df['Descricao_Processada'] = df['Descricao'].apply(preprocess_text)
    df['Classificacao'] = df['Descricao'].apply(classify_log)

    # 2. APLICA MODELO DE IA
    df, metrics = aplicar_modelo_ia(df)

    # 3. GERA ALERTAS
    alertas = generate_critical_alerts(df)

    # 4. VISUALIZAÇÃO DOS RESULTADOS
    plt.figure(figsize=(15, 6))

    # Gráfico de distribuição
    plt.subplot(1, 2, 1)
    sns.countplot(x='Predicao_IA', data=df,
                  palette={'Normal': 'green', 'Suspeito': 'orange', 'Crítico': 'red'})
    plt.title('Distribuição de Classificações')

    # Gráfico temporal
    plt.subplot(1, 2, 2)
    df['Data'] = pd.to_datetime(df['Data'])
    df.set_index('Data', inplace=True)
    df.resample('H')['Predicao_IA'].count().plot(kind='line', marker='o')
    plt.title('Frequência de Eventos por Hora')

    plt.tight_layout()
    plt.show()

    # 5. MÉTRICAS DO MODELO
    print("\n📊 MÉTRICAS DO MODELO:")
    for label, met in metrics.items():
        if isinstance(met, dict):
            print(f"\nClasse: {label}")
            for k, v in met.items():
                print(f"  {k}: {v:.2f}")