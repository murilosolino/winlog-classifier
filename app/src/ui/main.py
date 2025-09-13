"""
SISTEMA DE ANÁLISE DE LOGS INTELIGENTE
Fluxo principal:
1. Carrega logs brutos
2. Pré-processa o texto
3. Classifica automaticamente
4. Gera alertas e visualizações
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import nltk
import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parents[2])
sys.path.append(root_dir)

from src.data.data_loader import load_logs
from src.pre_processor.preprocessor import preprocess_text 
from src.classifiers.rule_based import classify_log
from src.ml.ml_model import aplicar_modelo_ia

nltk.download('stopwords')

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Análise de Logs Inteligente",
                   layout="wide",
                   page_icon="🔍")

st.title("🔍 Sistema Inteligente de Análise de Logs")

# SIDEBAR - Carregamento de dados
st.sidebar.header("Configurações")
file_uploaded = st.sidebar.file_uploader("Carregar arquivo de logs (.txt)", type=["txt"])
use_default = st.sidebar.checkbox("Usar logs padrão", value=True)

# 1. CARREGAMENTO
if use_default:
    df = load_logs('../data/massive_logs_windows.txt')
    st.sidebar.success("Usando logs padrão")
elif file_uploaded:
    df = load_logs(file_uploaded)
    st.sidebar.success("Arquivo carregado com sucesso")
else:
    st.warning("⚠️ Carregue um arquivo ou use os logs padrão para continuar.")
    st.stop()

# 2. PRÉ-PROCESSAMENTO
with st.spinner("🔄 Processando dados..."):
    df['Descricao_Processada'] = df['Descricao'].apply(preprocess_text)

# 3. CLASSIFICAÇÃO BASEADA EM REGRAS
df['Classificacao'] = df['ID_Evento'].apply(classify_log)

# 4. IA PARA LOGS DESCONHECIDOS
df_conhecidos = df[df['Classificacao'] != 'Desconhecido']
df_desconhecidos = df[df['Classificacao'] == 'Desconhecido'].copy()

if not df_desconhecidos.empty:
    df_desconhecidos, metrics = aplicar_modelo_ia(df_conhecidos, df_desconhecidos)
    df_desconhecidos['Classificacao'] = df_desconhecidos['Predicao_IA']
    df = pd.concat([df_conhecidos, df_desconhecidos])
else:
    metrics = {}
    df['Predicao_IA'] = None

# 5. COMPLETA COLUNA 'Predicao_IA'
df['Predicao_IA'] = df.get('Predicao_IA', pd.NA)
df['Predicao_IA'] = df['Predicao_IA'].fillna(df['Classificacao'])

# VISUALIZAÇÃO DAS CLASSIFICAÇÕES
st.subheader("Distribuição de Classificações")
fig_count = px.histogram(df, x='Predicao_IA', color='Predicao_IA',
                         color_discrete_map={'Normal': 'green', 'Suspeito': 'orange', 'Crítico': 'red'},
                         title='Distribuição das Classificações')
st.plotly_chart(fig_count, use_container_width=True)

# GRÁFICO TEMPORAL
st.subheader("Frequência de Eventos ao Longo do Tempo")
df['Data'] = pd.to_datetime(df['Data'])
df.set_index('Data', inplace=True)
df_resampled = df.resample('H')['Predicao_IA'].count().reset_index()
fig_time = px.line(df_resampled, x='Data', y='Predicao_IA', markers=True,
                    title='Quantidade de Eventos por Hora')
st.plotly_chart(fig_time, use_container_width=True)

# TABELA RESUMIDA
st.subheader("📊 Contagem de Classificações")
st.dataframe(df['Classificacao'].value_counts().reset_index().rename(
    columns={'index': 'Classificacao', 'Classificacao': 'Contagem'}))

# MÉTRICAS DO MODELO IA
if metrics:
    st.subheader("📈 Métricas do Modelo IA")
    for label, met in metrics.items():
        if isinstance(met, dict):
            st.markdown(f"**Classe: {label}**") 
            st.write({k: f"{v:.2f}" for k, v in met.items()})

# DOWNLOAD DOS RESULTADOS
csv = df.reset_index().to_csv(index=False).encode('utf-8')
st.sidebar.download_button("📥 Baixar resultados em CSV", data=csv,
                           file_name="resultado_logs.csv", mime="text/csv")

st.success("✅ Análise concluída!")
