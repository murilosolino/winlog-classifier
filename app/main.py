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
from src.ml_model import aplicar_modelo_ia

nltk.download('stopwords')

# EXECUÇÃO PRINCIPAL
if __name__ == "__main__":
    # 1. CARREGAMENTO E PRÉ-PROCESSAMENTO
    df = load_logs('docs/massive_logs_windows.txt')
    df['Descricao_Processada'] = df['Descricao'].apply(preprocess_text)

    # 2. CLASSIFICAÇÃO BASEADA EM REGRAS
    df['Classificacao'] = df['ID_Evento'].apply(classify_log)

    # 3. SEPARAR E CLASSIFICAR LOGS DESCONHECIDOS COM IA
    df_conhecidos = df[df['Classificacao'] != 'Desconhecido']
    df_desconhecidos = df[df['Classificacao'] == 'Desconhecido'].copy()

    if not df_desconhecidos.empty:
        df_desconhecidos, metrics = aplicar_modelo_ia(df_conhecidos, df_desconhecidos)

        # Substituir a classificação original pelos resultados da IA
        df_desconhecidos['Classificacao'] = df_desconhecidos['Predicao_IA']

        # Reunir os dois conjuntos
        df = pd.concat([df_conhecidos, df_desconhecidos])

    else:
        metrics = {}
        df['Predicao_IA'] = None  # Coluna vazia se não houve IA

    # 4. GARANTIR QUE TODOS TENHAM 'Predicao_IA'
    df['Predicao_IA'] = df.get('Predicao_IA', pd.NA)
    df['Predicao_IA'] = df['Predicao_IA'].fillna(df['Classificacao'])

    # 5. VISUALIZAÇÃO DOS RESULTADOS
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

    contagem_total = df['Classificacao'].value_counts()
    print("\n📦 Contagem de classificações totais:")
    print(contagem_total)

    # 7. MÉTRICAS DO MODELO
    if metrics:
        print("\n📊 MÉTRICAS DO MODELO:")
        for label, met in metrics.items():
            if isinstance(met, dict):
                print(f"\nClasse: {label}")
                for k, v in met.items():
                    print(f"  {k}: {v:.2f}")

