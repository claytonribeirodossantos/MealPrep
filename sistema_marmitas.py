from PIL import Image
import streamlit as st
import pandas as pd
from datetime import datetime

# Carrega o logo
logo = Image.open("logo_mealprep.jpeg")  # Renomeie o arquivo da imagem para este nome ou ajuste conforme necessário

# Configuração da página
st.set_page_config(page_title="Meal Prep USA - Base de Clientes", layout="centered")

# Estilo customizado com as cores do logo
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
st.image(logo, width=200)
st.title("Base de Clientes - Meal Prep USA")

# Inicializa a lista de clientes
if "clientes" not in st.session_state:
    st.session_state.clientes = []

# Formulário para novo cliente
with st.form("form_cliente"):
    nome = st.text_input("Nome completo")
    endereco = st.text_input("Endereço (com complemento)")
    telefone = st.text_input("Telefone")
    submit = st.form_submit_button("Cadastrar")

    if submit:
        if nome and endereco and telefone:
            data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            novo_cliente = {
                "Nome": nome,
                "Endereço": endereco,
                "Telefone": telefone,
                "Data de Cadastro": data_cadastro
            }
            st.session_state.clientes.append(novo_cliente)
            st.success("Cliente cadastrado com sucesso!")
        else:
            st.warning("Preencha todos os campos.")

# Exibição da tabela de clientes
if st.session_state.clientes:
    df = pd.DataFrame(st.session_state.clientes)
    st.subheader("Clientes cadastrados")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Nenhum cliente cadastrado ainda.")
