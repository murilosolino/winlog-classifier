import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parents[2])
sys.path.append(root_dir)

from src.data.data_loader import load_logs
from src.pre_processor.preprocessor import preprocess_text 
from src.classifiers.rule_based import classify_log

st.set_page_config(page_title="Análise de Logs (Regras)", layout="wide", page_icon="🔍")

st.title("🔍 Sistema de Análise de Logs - Classificação por Regras")

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

st.subheader("Distribuição de Classificações")
fig_count = px.histogram(df, x='Classificacao', color='Classificacao',
                         color_discrete_map={'Normal': 'green', 'Suspeito': 'orange', 'Crítico': 'red', 'Desconhecido': 'black'},
                         title='Distribuição das Classificações')
st.plotly_chart(fig_count, use_container_width=True)

st.subheader("Frequência de Eventos ao Longo do Tempo")
df['Data'] = pd.to_datetime(df['Data'])
df.set_index('Data', inplace=True)
df_resampled = df.resample('H')['Classificacao'].count().reset_index()
fig_time = px.line(df_resampled, x='Data', y='Classificacao', markers=True,
                    title='Quantidade de Eventos por Hora')
st.plotly_chart(fig_time, use_container_width=True)

st.subheader("📦 Contagem de Classificações")
st.dataframe(df['Classificacao'].value_counts().reset_index().rename(
    columns={'index': 'Classificacao', 'Classificacao': 'Contagem'}))

csv = df.reset_index().to_csv(index=False).encode('utf-8')
st.sidebar.download_button("📥 Baixar resultados em CSV", data=csv,
                           file_name="resultado_logs.csv", mime="text/csv")

st.success("✅ Análise concluída!")