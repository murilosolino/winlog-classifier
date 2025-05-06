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
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
from src.data_loader import load_logs
from src.preprocessor import preprocess_text
nltk.download('stopwords')





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

# EXECUÇÃO PRINCIPAL
if __name__ == "__main__":
    # 1. CARREGA E PREPARA OS DADOS
    df = load_logs('data/raw/massive_logs_windows.txt')
    df['Descricao_Processada'] = df['Descricao'].apply(preprocess_text)
    df['Classificacao'] = df['Descricao'].apply(classify_log)
    
    # 2. TRANSFORMA TEXTO EM VETORES NUMÉRICOS (TF-IDF)
    tfidf = TfidfVectorizer(max_features=1000)
    X = tfidf.fit_transform(df['Descricao_Processada'])
    y = df['Classificacao']
    
    # 3. TREINA MODELO DE MACHINE LEARNING
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    model = MultinomialNB()
    model.fit(X_train, y_train)
    
    # 4. GERA PREDIÇÕES E ALERTAS
    df['Predicao_IA'] = model.predict(X)
    
    # SISTEMA DE ALERTAS EM TEMPO REAL
    alertas = df[df['Predicao_IA'] == 'Crítico']
    if not alertas.empty:
        print("\n🚨 ALERTAS CRÍTICOS DETECTADOS 🚨")
        for _, row in alertas.iterrows():
            print(f"[{row['Data']}] {row['Fonte']} - {row['Descricao']}")
    
    # VISUALIZAÇÃO DOS RESULTADOS
    plt.figure(figsize=(15, 6))
    
    # Gráfico de distribuição de classificações
    plt.subplot(1, 2, 1)
    sns.countplot(x='Predicao_IA', data=df, 
                 palette={'Normal':'green', 'Suspeito':'orange', 'Crítico':'red'})
    plt.title('Distribuição de Classificações')
    
    # Gráfico temporal de eventos
    plt.subplot(1, 2, 2)
    df['Data'] = pd.to_datetime(df['Data'])
    df.set_index('Data', inplace=True)
    df.resample('H')['Predicao_IA'].count().plot(kind='line', marker='o')
    plt.title('Frequência de Eventos por Hora')
    
    plt.tight_layout()
    plt.show()
    
    # RELATÓRIO DE PERFORMANCE
    print("\n📊 MÉTRICAS DO MODELO:")
    print(classification_report(y, df['Predicao_IA']))