
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

aba = st.sidebar.radio("📁 Ações", ["🔍 Buscar e Editar Cliente", "➕ Adicionar Cliente"])

# =================== BUSCA COM EDIÇÃO ===================
if aba == "🔍 Buscar e Editar Cliente":
    st.subheader("🔍 Buscar Cliente com Autocompletar")
    
    nome_digitado = st.text_input("Digite o nome do cliente")
    sugestoes = [nome for nome in clientes.keys() if nome.lower().startswith(nome_digitado.lower())] if nome_digitado else []

    if sugestoes:
        nome_escolhido = st.selectbox("Selecione o cliente", sugestoes)
        endereco_atual = clientes[nome_escolhido]

        st.markdown("#### ✏️ Editar Cliente")
        novo_nome = st.text_input("Nome do cliente", value=nome_escolhido)
        novo_endereco = st.text_input("Endereço", value=endereco_atual)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Salvar Alterações"):
                clientes.pop(nome_escolhido)
                clientes[novo_nome] = novo_endereco
                salvar_clientes(clientes)
                st.success(f"Cliente '{nome_escolhido}' atualizado para '{novo_nome}' com sucesso!")

        with col2:
            if st.button("🗑️ Excluir Cliente"):
                clientes.pop(nome_escolhido)
                salvar_clientes(clientes)
                st.warning(f"Cliente '{nome_escolhido}' foi excluído com sucesso!")

# =================== ADICIONAR NOVO ===================
elif aba == "➕ Adicionar Cliente":
    st.subheader("➕ Adicionar Novo Cliente")
    col1, col2 = st.columns(2)
    with col1:
        nome_novo = st.text_input("Nome do novo cliente")
    with col2:
        endereco_digitado = st.text_input("Endereço (digite para sugestões)")

    sugestoes_end = buscar_endereco_nominatim(endereco_digitado) if endereco_digitado else []
    endereco_final = st.selectbox("Endereços sugeridos:", sugestoes_end) if sugestoes_end else endereco_digitado

    if st.button("✅ Cadastrar Cliente", use_container_width=True):
        if nome_novo and endereco_final:
            clientes[nome_novo] = endereco_final
            salvar_clientes(clientes)
            st.success(f"Cliente '{nome_novo}' cadastrado com sucesso!")
        else:
            st.error("Preencha todos os campos.")
