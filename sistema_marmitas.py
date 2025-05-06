import streamlit as st
import pandas as pd
from datetime import date
import os
import streamlit_authenticator as stauth

st.set_page_config(page_title="Meal Prep USA", layout="wide")

# ==================== Funções de carregamento ====================
def carregar_csv(nome_arquivo, default=pd.DataFrame()):
    try:
        return pd.read_csv(nome_arquivo)
    except:
        return default

CSV_CLIENTES = "clientes.csv"
CSV_PEDIDOS = "pedidos.csv"
CSV_SABORES = "sabores.csv"

clientes_df = carregar_csv(CSV_CLIENTES)
pedidos_df = carregar_csv(CSV_PEDIDOS)
sabores_df = carregar_csv(CSV_SABORES, pd.DataFrame({"Sabor": [
    "Frango grelhado", "Feijoada", "Strogonoff de frango",
    "Strogonoff de carne", "Frango assado", "Salmão assado", "Tilápia assada"]}))

# ==================== Autenticação com senha em texto ====================
credentials = {
    "usernames": {
        "admin": {
            "name": "Admin",
            "password": stauth.Hasher(["senha123"]).generate()[0]
        }
    }
}

authenticator = stauth.Authenticate(
    credentials, "meal_prep", "abcdef", cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login("Login")

# ==================== Lógica de login ====================
if authentication_status:
    st.sidebar.success(f"Bem-vindo(a), {name}!")
    authenticator.logout("Logout", "sidebar")

    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://raw.githubusercontent.com/claytonribeirodossantos/MealPrep/main/1.jpeg", width=100)
    with col2:
        st.markdown("<h1 style='color: #4CAF50;'>Sistema Interno de Gestão de Marmitas</h1>", unsafe_allow_html=True)

    st.markdown("---")
    menu = st.sidebar.selectbox("📁 Navegação", [
        "📦 Cadastrar Pedido", "📊 Resumo de Produção", "👤 Clientes", "🍽️ Sabores", "💰 Pagamentos"
    ])

    if menu == "📦 Cadastrar Pedido":
        st.subheader("Cadastrar Pedido")
        if not clientes_df.empty:
            cliente = st.selectbox("Cliente", clientes_df["Nome"])
            sabor = st.selectbox("Sabor da Marmita", sabores_df["Sabor"])
            quantidade = st.number_input("Quantidade", min_value=1, step=1)
            data_pedido = st.date_input("Data da entrega", value=date.today())
            if st.button("Registrar Pedido", type="primary"):
                novo = pd.DataFrame({
                    "Cliente": [cliente], "Sabor": [sabor],
                    "Quantidade": [quantidade], "Data": [data_pedido],
                    "Pago": [False], "Entregue": [False]
                })
                pedidos_df = pd.concat([pedidos_df, novo], ignore_index=True)
                pedidos_df.to_csv(CSV_PEDIDOS, index=False)
                st.success("Pedido registrado com sucesso!")
        else:
            st.warning("Nenhum cliente cadastrado ainda.")

    elif menu == "📊 Resumo de Produção":
        st.subheader("Resumo de Produção por Sabor")
        if not pedidos_df.empty:
            resumo = pedidos_df.groupby("Sabor")["Quantidade"].sum().reset_index()
            st.table(resumo)
        else:
            st.info("Nenhum pedido registrado ainda.")

    elif menu == "👤 Clientes":
        st.subheader("Clientes Cadastrados")
        st.dataframe(clientes_df)
        st.markdown("### Adicionar Novo Cliente")
        novo_nome = st.text_input("Nome do Cliente")
        novo_endereco = st.text_input("Endereço")
        if st.button("Adicionar Cliente"):
            if novo_nome and novo_endereco:
                novo_cliente = pd.DataFrame({"Nome": [novo_nome], "Endereco": [novo_endereco]})
                clientes_df = pd.concat([clientes_df, novo_cliente], ignore_index=True)
                clientes_df.to_csv(CSV_CLIENTES, index=False)
                st.success("Cliente adicionado com sucesso!")
            else:
                st.warning("Preencha todos os campos.")

    elif menu == "🍽️ Sabores":
        st.subheader("Sabores Disponíveis")
        st.dataframe(sabores_df)
        novo_sabor = st.text_input("Novo Sabor")
        if st.button("Adicionar Sabor"):
            if novo_sabor:
                sabores_df = pd.concat([sabores_df, pd.DataFrame({"Sabor": [novo_sabor]})], ignore_index=True)
                sabores_df.to_csv(CSV_SABORES, index=False)
                st.success("Sabor adicionado com sucesso!")
            else:
                st.warning("Informe o nome do sabor.")

    elif menu == "💰 Pagamentos":
        st.subheader("Controle de Pagamentos e Entregas")
        if not pedidos_df.empty:
            for i, row in pedidos_df.iterrows():
                with st.expander(f"Pedido {i+1}: {row['Cliente']}"):
                    pago = st.checkbox("Pago?", value=row["Pago"], key=f"pago_{i}")
                    entregue = st.checkbox("Entregue?", value=row["Entregue"], key=f"entregue_{i}")
                    pedidos_df.at[i, "Pago"] = pago
                    pedidos_df.at[i, "Entregue"] = entregue
            if st.button("Salvar Alterações"):
                pedidos_df.to_csv(CSV_PEDIDOS, index=False)
                st.success("Alterações salvas com sucesso!")
        else:
            st.info("Nenhum pedido registrado ainda.")

elif authentication_status is False:
    st.error("Nome de usuário ou senha incorretos.")
elif authentication_status is None:
    st.warning("Por favor, insira suas credenciais para continuar.")
