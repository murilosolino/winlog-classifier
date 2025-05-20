import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Função para treinar IA com dados conhecidos e aplicar em desconhecidos
def aplicar_modelo_ia(df_treino: pd.DataFrame, df_predicao: pd.DataFrame):
    # Verificar se temos dados de treino suficientes
    if df_treino['Classificacao'].nunique() < 2:
        print("⚠️ Não há classes suficientes para treinar o modelo.")
        df_predicao['Predicao_IA'] = 'Normal'  # fallback padrão
        return df_predicao, {}

    # Vetorização TF-IDF no conjunto combinado
    tfidf = TfidfVectorizer(max_features=1000)
    X_treino = tfidf.fit_transform(df_treino['Descricao_Processada'])
    y_treino = df_treino['Classificacao']

    # Treina o modelo com os dados conhecidos
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(
        X_treino, y_treino, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)

    # Avaliação no próprio treino
    y_pred = model.predict(X_treino)
    metrics = classification_report(y_treino, y_pred, output_dict=True)

    # Aplica IA nos dados desconhecidos
    X_pred = tfidf.transform(df_predicao['Descricao_Processada'])
    df_predicao['Predicao_IA'] = model.predict(X_pred)

    return df_predicao, metrics