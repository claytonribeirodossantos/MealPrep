from pathlib import Path

code = """
import streamlit as st
import pandas as pd
from datetime import date
import os
import streamlit_authenticator as stauth

st.set_page_config(page_title="Meal Prep USA", layout="wide")

CSV_CLIENTES = "clientes.csv"
CSV_PEDIDOS = "pedidos.csv"
CSV_SABORES = "sabores.csv"

def carregar_csv(nome_arquivo, default=pd.DataFrame()):
    try:
        return pd.read_csv(nome_arquivo)
    except:
        return default

clientes_df = carregar_csv(CSV_CLIENTES)
pedidos_df = carregar_csv(CSV_PEDIDOS)
sabores_df = carregar_csv(CSV_SABORES, pd.DataFrame({"Sabor": [
    "Frango grelhado", "Feijoada", "Strogonoff de frango",
    "Strogonoff de carne", "Frango assado", "Salmão assado", "Tilápia assada"]}))

credentials = {
    "usernames": {
        "admin": {
            "name": "Admin",
            "password": "pbkdf2:sha256:260000$YQWRdj8GlQXV6u5j$6ed944aa7b2e2c529a91b8b75c1893a7f5c2e18cfb9d110d3c04d36044fbd4e7"
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "meal_prep", "abcdef", cookie_expiry_days=30
)
name, authentication_status, username = authenticator.login("Login", location="main")

if authentication_status:
    st.sidebar.success(f"Bem-vindo(a), {name}!")
    authenticator.logout("Logout", "sidebar")

    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://raw.githubusercontent.com/claytonribeirodossantos/MealPrep/main/1.jpeg", width=100)
    with col2:
        st.markdown("<h1 style='color: #4CAF50;'>Sistema Interno de Gestão de Marmitas</h1>", unsafe_allow_html=True)
    st.markdown("---")

    menu = st.sidebar.selectbox("📁 Navegação", ["📦 Cadastrar Pedido", "📊 Resumo de Produção", "👤 Clientes", "🍽️ Sabores", "💰 Pagamentos"])

    if menu == "👤 Clientes":
        st.subheader("Clientes Cadastrados")

        if not clientes_df.empty:
            clientes_df_display = clientes_df.copy()
            clientes_df_display.index = clientes_df_display.index + 1
            st.dataframe(clientes_df_display, use_container_width=True)

            st.markdown("### ✏️ Alterar ou ❌ Excluir Clientes")
            for i, row in clientes_df.iterrows():
                with st.expander(f"{i+1}. {row['Nome']}"):
                    novo_nome = st.text_input("Nome", value=row["Nome"], key=f"nome_{i}")
                    novo_endereco = st.text_input("Endereço", value=row["Endereco"], key=f"endereco_{i}")

                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("Salvar Alterações", key=f"salvar_{i}"):
                            clientes_df.at[i, "Nome"] = novo_nome
                            clientes_df.at[i, "Endereco"] = novo_endereco
                            clientes_df.to_csv(CSV_CLIENTES, index=False)
                            st.success("Cliente alterado com sucesso!")
                    with col2:
                        if st.button("❌ Excluir Cliente", key=f"excluir_{i}"):
                            if st.checkbox("Confirmar exclusão", key=f"confirmar_{i}"):
                                clientes_df = clientes_df.drop(i).reset_index(drop=True)
                                clientes_df.to_csv(CSV_CLIENTES, index=False)
                                st.warning("Cliente excluído.")
                                st.experimental_rerun()

        st.markdown("### ➕ Adicionar Novo Cliente")
        novo_nome = st.text_input("Nome do Cliente")
        novo_endereco = st.text_input("Endereço (opcional)")
        if st.button("Adicionar Cliente"):
            if novo_nome:
                novo_cliente = pd.DataFrame({
                    "Nome": [novo_nome],
                    "Endereco": [novo_endereco if novo_endereco else ""]
                })
                clientes_df = pd.concat([clientes_df, novo_cliente], ignore_index=True)
                clientes_df.to_csv(CSV_CLIENTES, index=False)
                st.success("Cliente adicionado com sucesso!")
                st.experimental_rerun()
            else:
                st.warning("Informe ao menos o nome do cliente.")

elif authentication_status is False:
    st.error("Nome de usuário ou senha incorretos.")
elif authentication_status is None:
    st.warning("Por favor, insira suas credenciais para continuar.")
"""

path = Path("/mnt/data/sistema_marmitas_clientes_atualizado.py")
path.write_text(code)
path
