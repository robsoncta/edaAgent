import asyncio
import streamlit as st
import pandas as pd
import os
import tempfile
import json
from datetime import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from utils.config import Config
from utils.helpers import ensure_directories, clean_temp_files, validate_csv_file
from main import EDASystem

st.set_page_config(
    page_title="EDA Agente Inteligente",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""<style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; }
    .sidebar .sidebar-content { background-color: #ffffff; }
</style>""", unsafe_allow_html=True)

async def main():
    initialize_session_state()
    config_sidebar = st.sidebar.container()
    with config_sidebar:
        st.title("⚙️ Configurações")
        llm_provider = st.selectbox(
            "Provider LLM",
            options=["openai", "groq"],
            index=0 if st.session_state.get('llm_provider_select', "openai") == "openai" else 1,
            key="llm_provider_select"
        )
        tokens_limit = st.slider(
            "Max Tokens",
            min_value=100,
            max_value=2000,
            value=1000 if llm_provider == "openai" else 300,
            step=100,
            key="tokens_slider"
        )

    if not st.session_state.system_initialized:
        config = Config()
        st.session_state.eda_system = EDASystem(llm_provider, tokens_limit, config)
        st.session_state.system_initialized = True
        st.session_state.current_config = f"Provider: {llm_provider} | Tokens: {tokens_limit}"

    eda_system = st.session_state.eda_system

    st.title("🤖 EDA Agente Inteligente")

    if not st.session_state.dataset_loaded:
        await load_dataset_section(eda_system)
    else:
        await chat_section(eda_system)

    add_visualization_sidebar()

async def load_dataset_section(eda_system: EDASystem):
    st.header("1. Carregue seu Dataset CSV")
    tab1, tab2, tab3 = st.tabs(["📤 Upload Local", "🔗 URL Direta", "📊 Exemplos"])

    with tab1:
        uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
                temp_file.write(uploaded_file.getvalue())
                file_path = temp_file.name
            await process_dataset(file_path, "Upload Local", eda_system)

    with tab2:
        url = st.text_input("URL do CSV")
        if st.button("Carregar URL") and url:
            await process_dataset(url, "URL Direta", eda_system)

    with tab3:
        example = st.selectbox("Dataset de Exemplo", ["Iris", "Tips", "Titanic"])
        if st.button("Carregar Exemplo"):
            url_map = {"Iris": "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv",
                       "Tips": "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv",
                       "Titanic": "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"}
            await process_dataset(url_map[example], f"Exemplo {example}", eda_system)

async def process_dataset(source: str, source_type: str, eda_system: EDASystem):
    with st.spinner("Validando e carregando dataset..."):
        is_valid, msg, data = validate_csv_file(source)
        if not is_valid:
            st.error(msg)
            return
        eda_system.current_dataset = data
        st.session_state.dataset_loaded = True
        st.session_state.dataset_source = source_type
        st.session_state.current_dataset_info = {
            "shape": data.shape,
            "columns": data.columns.tolist(),
            "dtypes": data.dtypes.to_dict(),
            "head": data.head(5).to_dict(orient="records")
        }
        await initial_analysis(eda_system)
        st.rerun()

async def initial_analysis(eda_system: EDASystem):
    with st.spinner("Executando análise inicial..."):
        try:
            response = await eda_system.analyze("Execute análise exploratória inicial do dataset")
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        except Exception as e:
            if handle_rate_limit_error(str(e), eda_system.llm_provider):
                return
            st.error(f"Erro na análise inicial: {str(e)}")

async def chat_section(eda_system: EDASystem):
    st.header("2. Chat Interativo")
    st.info(f"Dataset: {st.session_state.dataset_source} | {st.session_state.current_dataset_info['shape'][0]} linhas x {st.session_state.current_dataset_info['shape'][1]} colunas")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "images" in message:
                for img in message["images"]:
                    st.image(img)

    if prompt := st.chat_input("Faça sua pergunta sobre os dados..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        await process_user_question(prompt, eda_system)

async def process_user_question(question: str, eda_system: EDASystem):
    with st.spinner("Analisando..."):
        try:
            response = await eda_system.analyze(question)
            parsed = parse_response(response)
            with st.chat_message("assistant"):
                st.markdown(parsed["text"])
                for img_path in parsed["images"]:
                    st.image(img_path)
            st.session_state.chat_history.append({"role": "assistant", "content": parsed["text"], "images": parsed["images"]})
        except Exception as e:
            if handle_rate_limit_error(str(e), eda_system.llm_provider):
                return
            st.error(f"Erro: {str(e)}")

def parse_response(response: str) -> dict:
    lines = response.split("\n")
    text = ""
    images = []
    for line in lines:
        if line.startswith("IMAGE:"):
            images.append(line.split(":")[1].strip())
        else:
            text += line + "\n"
    return {"text": text, "images": images}

def initialize_session_state():
    keys = ['eda_system', 'dataset_loaded', 'chat_history', 'current_dataset_info', 'current_config', 'system_initialized', 'dataset_source', 'session_finalized']
    for key in keys:
        if key not in st.session_state:
            st.session_state[key] = None if key == 'eda_system' else False if 'loaded' in key or 'initialized' in key or 'finalized' in key else [] if 'history' in key else {} if 'info' in key else ""

def add_visualization_sidebar():
    if st.session_state.dataset_loaded:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Visualizações Rápidas")
        if st.sidebar.button("🎯 Gerar Todas as Visualizações"):
            asyncio.run(process_user_question("Gere todas as visualizações possíveis", st.session_state.eda_system))
        st.sidebar.markdown("**Gráficos Específicos:**")
        if st.sidebar.button("📈 Matriz Correlação"):
            asyncio.run(process_user_question("Gere matriz de correlação", st.session_state.eda_system))
        if st.sidebar.button("📊 Distribuições"):
            asyncio.run(process_user_question("Mostre distribuições das variáveis", st.session_state.eda_system))
        if st.sidebar.button("🎯 Scatter Plots"):
            asyncio.run(process_user_question("Crie scatter plots entre variáveis", st.session_state.eda_system))
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📋 Info do Dataset")
        info = st.session_state.current_dataset_info
        col1, col2 = st.sidebar.columns(2)
        col1.metric("Linhas", info["shape"][0])
        col2.metric("Colunas", info["shape"][1])
        numeric = len([dt for dt in info["dtypes"].values() if pd.api.types.is_numeric_dtype(dt)])
        categorical = len(info["dtypes"]) - numeric
        st.sidebar.markdown(f"**Numéricas:** {numeric}")
        st.sidebar.markdown(f"**Categóricas:** {categorical}")

if __name__ == "__main__":
    asyncio.run(main())