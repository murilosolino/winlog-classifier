import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

def criar_matriz_confusao(df_conhecidos, modelo_selecionado):
    classes = sorted(df_conhecidos['Classificacao'].unique())
    
    if len(classes) < 2:
        st.warning("Não há classes suficientes para criar uma matriz de confusão.")
        return
    
    # Preparar dados para validação
    test_size = min(0.3, 1.0 if len(df_conhecidos) < 10 else 0.2)
    X = df_conhecidos['Descricao_Processada']
    y = df_conhecidos['Classificacao']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    # Preparar pipelines
    nb_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
        ('classifier', MultinomialNB())
    ])
    
    rf_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000)),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    # Gerar matriz para o modelo principal
    st.subheader("🧩 Matriz de Confusão")
    
    if modelo_selecionado == "Naive Bayes":
        pipeline = nb_pipeline
        colorscale = 'Blues'
    else:
        pipeline = rf_pipeline
        colorscale = 'Greens'

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    
    # Calcular matriz de confusão
    cm = confusion_matrix(y_test, y_pred, labels=classes)
    
    # Criar heatmap da matriz de confusão
    fig = ff.create_annotated_heatmap(
        z=cm,
        x=classes,
        y=classes,
        annotation_text=cm,
        colorscale=colorscale
    )
    
    fig.update_layout(
        title=f'Matriz de Confusão - {modelo_selecionado}',
        xaxis=dict(title='Classe Prevista'),
        yaxis=dict(title='Classe Real')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    outro_modelo = "Random Forest" if modelo_selecionado == "Naive Bayes" else "Naive Bayes"
    if st.button(f"Comparar com {outro_modelo}"):
        exibir_comparacao_modelos(X_train, X_test, y_train, y_test, classes)

def exibir_comparacao_modelos(X_train, X_test, y_train, y_test, classes):
    st.subheader("Comparação entre Naive Bayes e Random Forest")
    
    # Treinar os dois modelos
    nb_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
        ('classifier', MultinomialNB())
    ])
    
    rf_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000)),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    nb_pipeline.fit(X_train, y_train)
    rf_pipeline.fit(X_train, y_train)
    
    nb_pred = nb_pipeline.predict(X_test)
    rf_pred = rf_pipeline.predict(X_test)
    
    # Criar matrizes de confusão
    nb_cm = confusion_matrix(y_test, nb_pred, labels=classes)
    rf_cm = confusion_matrix(y_test, rf_pred, labels=classes)
    
    # Criar layout lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Naive Bayes**")
        fig_nb = ff.create_annotated_heatmap(
            z=nb_cm,
            x=classes,
            y=classes,
            annotation_text=nb_cm,
            colorscale='Blues'
        )
        fig_nb.update_layout(height=400, width=400)
        st.plotly_chart(fig_nb)
    
    with col2:
        st.markdown("**Random Forest**")
        fig_rf = ff.create_annotated_heatmap(
            z=rf_cm,
            x=classes,
            y=classes,
            annotation_text=rf_cm,
            colorscale='Greens'
        )
        fig_rf.update_layout(height=400, width=400)
        st.plotly_chart(fig_rf)
    
    # Adicionar métricas comparativas
    from sklearn.metrics import accuracy_score
    
    nb_acc = accuracy_score(y_test, nb_pred)
    rf_acc = accuracy_score(y_test, rf_pred)
    
    comp_data = pd.DataFrame({
        'Modelo': ['Naive Bayes', 'Random Forest'],
        'Acurácia': [nb_acc, rf_acc]
    })
    
    fig_comp = px.bar(comp_data, x='Modelo', y='Acurácia', 
                      color='Modelo', title='Comparação de Acurácia')
    st.plotly_chart(fig_comp, use_container_width=True)