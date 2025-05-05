import pandas as pd
import os
from PIL import Image
from datetime import datetime
import streamlit as st

# Caminho dos arquivos
CSV_PATH = "clientes.csv"
LOGO_PATH = "1.png"

# Criação do arquivo CSV se não existir
if not os.path.exists(CSV_PATH):
    df_empty = pd.DataFrame(columns=["Nome", "Endereço", "Telefone", "Data de Cadastro"])
    df_empty.to_csv(CSV_PATH, index=False)

# Carregar os dados
df = pd.read_csv(CSV_PATH)

# Configuração da página
st.set_page_config(page_title="Base de Clientes - Meal Prep USA", layout="centered")

# Estilos customizados
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    h1 {
        color: #4C7024;
    }
    .stButton>button {
        background-color: #F7941D;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Exibe o logo
if os.path.exists(LOGO_PATH):
    logo = Image.open(LOGO_PATH)
    st.image(logo, width=200)

st.title("Base de Clientes - Meal Prep USA")

# Ações do menu
aba = st.sidebar.radio("Menu", ["Cadastrar", "Buscar/Editar", "Excluir", "Listar todos"])

# --- Cadastrar novo cliente ---
if aba == "Cadastrar":
    st.header("Cadastrar novo cliente")
    with st.form("form_cadastro"):
        nome = st.text_input("Nome completo")
        endereco = st.text_input("Endereço (com complemento)")
        telefone = st.text_input("Telefone")
        submit = st.form_submit_button("Cadastrar")
        if submit:
            if nome and endereco and telefone:
                data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                novo = pd.DataFrame([[nome, endereco, telefone, data]], columns=df.columns)
                df = pd.concat([df, novo], ignore_index=True)
                df.to_csv(CSV_PATH, index=False)
                st.success("Cliente cadastrado com sucesso!")
            else:
                st.warning("Preencha todos os campos.")

# --- Buscar e editar cliente ---
elif aba == "Buscar/Editar":
    st.header("Buscar e editar cliente")
    nomes = df["Nome"].tolist()
    busca = st.selectbox("Selecione o nome", [""] + nomes)
    if busca:
        dados = df[df["Nome"] == busca].iloc[0]
        with st.form("form_editar"):
            nome = st.text_input("Nome completo", value=dados["Nome"])
            endereco = st.text_input("Endereço", value=dados["Endereço"])
            telefone = st.text_input("Telefone", value=dados["Telefone"])
            submit = st.form_submit_button("Salvar alterações")
            if submit:
                df.loc[df["Nome"] == busca, ["Nome", "Endereço", "Telefone"]] = [nome, endereco, telefone]
                df.to_csv(CSV_PATH, index=False)
                st.success("Dados atualizados com sucesso!")

# --- Excluir cliente ---
elif aba == "Excluir":
    st.header("Excluir cliente")
    nomes = df["Nome"].tolist()
    selecionado = st.selectbox("Escolha o cliente para excluir", [""] + nomes)
    if selecionado:
        if st.button(f"Confirmar exclusão de {selecionado}"):
            df = df[df["Nome"] != selecionado]
            df.to_csv(CSV_PATH, index=False)
            st.success("Cliente excluído com sucesso!")

# --- Listar todos os clientes ---
elif aba == "Listar todos":
    st.header("Clientes cadastrados")
    if df.empty:
        st.info("Nenhum cliente cadastrado.")
    else:
        st.dataframe(df, use_container_width=True)
