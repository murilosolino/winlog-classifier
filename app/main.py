# Importação de bibliotecas
import pandas as pd  # Manipulação de dados tabulares
import re  # Expressões regulares para processamento de texto
from sklearn.feature_extraction.text import TfidfVectorizer  # Vetorização de texto
from sklearn.model_selection import train_test_split  # Divisão de dados para treino/teste
from sklearn.naive_bayes import MultinomialNB  # Algoritmo de classificação Naive Bayes
from sklearn.metrics import classification_report  # Métricas de avaliação
import matplotlib.pyplot as plt  # Visualização gráfica
import seaborn as sns  # Visualização estatística
from nltk.corpus import stopwords  # Palavras irrelevantes para filtragem
from nltk.stem import PorterStemmer  # Redução de palavras à sua raiz (stemming)
import nltk  # Natural Language Toolkit

# Download das stopwords em português (necessário apenas na primeira execução)
nltk.download('stopwords')

def load_logs(file_path):
    """
    Carrega e estrutura os logs a partir de um arquivo de texto
    Teoria: Transformação de dados não estruturados em estruturados (DataFrame)
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().split('\n\n')  # Divide o arquivo em entradas de log
    
    logs = []
    for entry in content:
        if entry.strip():  # Ignora blocos vazios
            log = {}
            for line in entry.split('\n'):  # Processa cada linha do log
                # Extração estruturada usando padrões conhecidos
                if line.startswith('Data:'):
                    log['Data'] = line.split(': ', 1)[1]  # Captura o valor após o prefixo
                elif line.startswith('Fonte:'):
                    log['Fonte'] = line.split(': ', 1)[1]
                elif line.startswith('ID do Evento:'):
                    log['ID_Evento'] = int(line.split(': ', 1)[1])
                elif line.startswith('Descrição:'):
                    log['Descricao'] = line.split(': ', 1)[1]
            logs.append(log)  # Adiciona o log estruturado à lista
    return pd.DataFrame(logs)  # Converte para DataFrame pandas

def preprocess_text(text):
    """
    Pré-processamento de texto para NLP (Natural Language Processing)
    Teoria: Normalização de texto para melhorar a qualidade da análise
    """
    text = text.lower()  # Normalização: tudo para minúsculas
    text = re.sub(r'[^\w\s]', '', text)  # Remove pontuação usando regex
    tokens = text.split()  # Tokenização: divide o texto em palavras
    
    # Remoção de stopwords (palavras sem valor semântico)
    stop_words = set(stopwords.words('portuguese'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Stemming: redução de palavras à sua raiz gramatical
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    
    return ' '.join(tokens)  # Reconstroi o texto processado

def classify_log(descricao):
    """
    Classificação baseada em regras para criar labels iniciais
    Teoria: Criação de dados rotulados para treinamento supervisionado
    """
    criticas = ['erro', 'falhou', 'insuficiente', 'encerrado']
    suspeitas = ['atualização', 'reiniciado', 'pausado']
    
    # Lógica de classificação hierárquica
    if any(word in descricao.lower() for word in criticas):
        return 'Crítico'
    elif any(word in descricao.lower() for word in suspeitas):
        return 'Suspeito'
    else:
        return 'Normal'

# Carregamento dos dados (ETL - Extract, Transform, Load)
df = load_logs('massive_logs_windows.txt')  # Extração e estruturação

# Pré-processamento dos dados
df['Descricao_Processada'] = df['Descricao'].apply(preprocess_text)  # Aplica NLP
df['Classificacao'] = df['Descricao'].apply(classify_log)  # Cria labels iniciais

# Vetorização usando TF-IDF (Term Frequency-Inverse Document Frequency)
# Teoria: Representação numérica do texto ponderando a importância das palavras
tfidf = TfidfVectorizer(max_features=1000)  # Limita ao top 1000 termos mais relevantes
X = tfidf.fit_transform(df['Descricao_Processada'])  # Transforma texto em vetores
y = df['Classificacao']  # Variável target

# Divisão dos dados para validação do modelo
# Teoria: Separação para evitar overfitting e testar generalização
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,  # 20% para teste
    random_state=42  # Semente para reprodutibilidade
)

# Criação e treinamento do modelo Naive Bayes Multinomial
# Teoria: Classificador probabilístico baseado no teorema de Bayes
model = MultinomialNB()  # Adequado para dados discretos (contagens de palavras)
model.fit(X_train, y_train)  # Ajuste do modelo aos dados de treino

# Predição e avaliação
predictions = model.predict(X)  # Classificação de todos os dados
df['Predicao_IA'] = predictions  # Adiciona previsões ao DataFrame

# Sistema de alertas para eventos críticos
alertas = df[df['Predicao_IA'] == 'Crítico']
if not alertas.empty:
    print("\n🚨 ALERTAS CRÍTICOS 🚨")
    # Iteração sobre as linhas do DataFrame filtrado
    for _, row in alertas.iterrows():
        print(f"[{row['Data']}] {row['Fonte']} - {row['Descricao']}")

# Visualização dos resultados
plt.figure(figsize=(15, 6))  # Define o tamanho da figura

# Gráfico 1: Distribuição das classificações
plt.subplot(1, 2, 1)  # Cria subplot 1x2 (posição 1)
sns.countplot(
    x='Predicao_IA', 
    data=df, 
    palette={'Normal':'green', 'Suspeito':'orange', 'Crítico':'red'}  # Esquema de cores
)
plt.title('Distribuição de Classificações')  # Título do gráfico

# Gráfico 2: Linha do tempo de eventos
plt.subplot(1, 2, 2)  # Cria subplot 1x2 (posição 2)
df['Data'] = pd.to_datetime(df['Data'])  # Converte para tipo datetime
df.set_index('Data', inplace=True)  # Define a coluna Data como índice
# Agrupamento por hora e contagem de eventos
df.resample('H')['Predicao_IA'].count().plot(kind='line', marker='o')
plt.title('Atividade de Eventos por Hora')
plt.ylabel('Quantidade de Eventos')

plt.tight_layout()  # Ajuste automático do layout
plt.show()  # Exibe os gráficos

# Relatório de performance do modelo
print("\nRelatório de Classificação:")
print(classification_report(y, predictions))  # Métricas detalhadasm