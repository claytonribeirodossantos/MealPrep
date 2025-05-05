
import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(page_title="Meal Prep USA", layout="wide")

CSV_CLIENTES = "clientes.csv"

def carregar_clientes():
    if os.path.exists(CSV_CLIENTES):
        df = pd.read_csv(CSV_CLIENTES)
        return dict(zip(df["Nome"], df["Endereco"]))
    return {}

def salvar_clientes(clientes_dict):
    df = pd.DataFrame(list(clientes_dict.items()), columns=["Nome", "Endereco"])
    df.to_csv(CSV_CLIENTES, index=False)

def buscar_endereco_nominatim(query):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "addressdetails": 1,
        "limit": 3
    }
    headers = {
        "User-Agent": "MealPrepUSA/1.0"
    }
    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()
        resultados = r.json()
        return [r["display_name"] for r in resultados]
    except Exception:
        return []

clientes = carregar_clientes()

st.markdown(
    '<div style="text-align: center;">'
    '<img src="https://raw.githubusercontent.com/willianrod/mealprepusa/main/logo_mealprepusa.jpeg" width="200">'
    '<h1 style="color:#4CAF50;">📋 Gestão de Clientes - Meal Prep USA</h1>'
    '</div>',
    unsafe_allow_html=True
)
st.markdown("---")

aba = st.sidebar.radio("📁 Ações", ["🔍 Buscar Cliente", "➕ Adicionar Cliente", "🗑️ Excluir Cliente"])

if aba == "🔍 Buscar Cliente":
    st.markdown("### 🔍 Buscar Cliente Cadastrado")
    with st.container():
        nome_busca = st.text_input("Digite o nome do cliente para buscar")
        if st.button("Buscar"):
            if nome_busca in clientes:
                endereco = clientes[nome_busca]
                st.success(f"✅ Endereço encontrado:\n\n{endereco}")
            else:
                st.warning("⚠️ Cliente não encontrado.")

elif aba == "➕ Adicionar Cliente":
    st.markdown("### ➕ Cadastrar Novo Cliente")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            nome_novo = st.text_input("Nome do novo cliente")
        with col2:
            endereco_digitado = st.text_input("Endereço (inicie a digitação para sugestões)")
        
        sugestoes = buscar_endereco_nominatim(endereco_digitado) if endereco_digitado else []
        endereco_final = st.selectbox("Endereços sugeridos:", sugestoes) if sugestoes else endereco_digitado

        if st.button("💾 Salvar Cliente", use_container_width=True):
            if nome_novo and endereco_final:
                clientes[nome_novo] = endereco_final
                salvar_clientes(clientes)
                st.success(f"Cliente {nome_novo} salvo com sucesso! ✅")
            else:
                st.error("Preencha todos os campos.")

elif aba == "🗑️ Excluir Cliente":
    st.markdown("### 🗑️ Remover Cliente da Base")
    if clientes:
        nome_excluir = st.selectbox("Selecione o cliente a ser removido", list(clientes.keys()))
        if st.button("❌ Excluir Cliente", type="primary"):
            clientes.pop(nome_excluir)
            salvar_clientes(clientes)
            st.success(f"Cliente {nome_excluir} removido com sucesso!")
    else:
        st.info("Nenhum cliente cadastrado ainda.")
