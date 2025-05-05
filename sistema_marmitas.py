
import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(page_title="Meal Prep USA", layout="wide")

# ================= CONFIG =================
CSV_CLIENTES = "clientes.csv"

# ================= FUNÇÕES AUXILIARES =================
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
    except Exception as e:
        return []

# ================= INTERFACE =================
clientes = carregar_clientes()

st.image("https://raw.githubusercontent.com/willianrod/mealprepusa/main/logo_mealprepusa.jpeg", width=300)
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Gestão de Clientes - Meal Prep USA</h1>", unsafe_allow_html=True)
st.markdown("---")

aba = st.sidebar.radio("Ações", ["Buscar Cliente", "Adicionar Cliente", "Excluir Cliente"])

# ================= BUSCAR CLIENTE =================
if aba == "Buscar Cliente":
    nome_busca = st.text_input("Buscar cliente pelo nome")
    if st.button("Buscar"):
        if nome_busca in clientes:
            st.success(f"Endereço de {nome_busca}:")
            st.info(clientes[nome_busca])
        else:
            st.warning("Cliente não encontrado.")

# ================= ADICIONAR CLIENTE =================
elif aba == "Adicionar Cliente":
    nome_novo = st.text_input("Nome do novo cliente")
    endereco_digitado = st.text_input("Digite o endereço")

    sugestoes = []
    if endereco_digitado:
        sugestoes = buscar_endereco_nominatim(endereco_digitado)

    if sugestoes:
        endereco_final = st.selectbox("Selecione o endereço sugerido:", sugestoes)
    else:
        endereco_final = endereco_digitado

    if st.button("Salvar Cliente"):
        if nome_novo and endereco_final:
            clientes[nome_novo] = endereco_final
            salvar_clientes(clientes)
            st.success("Cliente salvo com sucesso!")
        else:
            st.warning("Preencha todos os campos.")

# ================= EXCLUIR CLIENTE =================
elif aba == "Excluir Cliente":
    if clientes:
        nome_excluir = st.selectbox("Selecione o cliente para excluir", list(clientes.keys()))
        if st.button("Excluir Cliente"):
            clientes.pop(nome_excluir)
            salvar_clientes(clientes)
            st.success(f"Cliente '{nome_excluir}' excluído com sucesso!")
    else:
        st.info("Nenhum cliente cadastrado.")
