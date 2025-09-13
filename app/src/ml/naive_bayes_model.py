import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split

def aplicar_modelo_naive_bayes(df_conhecidos, df_desconhecidos):
    # 1. Dividir dados conhecidos em treino e validação
    if len(df_conhecidos) > 10:  
        X_train_val, X_test_val, y_train_val, y_test_val = train_test_split(
            df_conhecidos['Descricao_Processada'], 
            df_conhecidos['Classificacao'], 
            test_size=0.2,  
            random_state=42
        )
    else:
        X_train_val, y_train_val = df_conhecidos['Descricao_Processada'], df_conhecidos['Classificacao']
        X_test_val, y_test_val = pd.Series([]), pd.Series([])
    
    # 2. Criar pipeline com TF-IDF e Naive Bayes
    nb_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
        ('classifier', MultinomialNB())
    ])
    
    # 3. Treinar modelo com todos os dados conhecidos para a predição final
    X_train_full = df_conhecidos['Descricao_Processada']
    y_train_full = df_conhecidos['Classificacao']
    nb_pipeline.fit(X_train_full, y_train_full)
    
    # 4. Fazer predições nos dados desconhecidos
    X_test = df_desconhecidos['Descricao_Processada']
    predicoes = nb_pipeline.predict(X_test)
    df_desconhecidos['Predicao_IA'] = predicoes
    
    # 5. Calcular métricas usando o conjunto de validação
    metrics = {}
    if len(X_test_val) > 0:
        nb_pipeline_val = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
            ('classifier', MultinomialNB())
        ])
        nb_pipeline_val.fit(X_train_val, y_train_val)
        
        val_pred = nb_pipeline_val.predict(X_test_val)
    
        metrics = classification_report(y_test_val, val_pred, output_dict=True)
    
    return df_desconhecidos, metrics