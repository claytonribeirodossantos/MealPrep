import streamlit as st
import pandas as pd
from datetime import date
import os
import streamlit_authenticator as stauth

st.set_page_config(page_title="Meal Prep USA", layout="wide")

# Arquivos CSV
CSV_CLIENTES = "clientes.csv"
CSV_PEDIDOS = "pedidos.csv"
CSV_SABORES = "sabores.csv"

def carregar_csv(nome_arquivo, default=pd.DataFrame()):
    try:
        return pd.read_csv(nome_arquivo)
    except:
        return default

# Carregar dados
clientes_df = carregar_csv(CSV_CLIENTES)
pedidos_df = carregar_csv(CSV_PEDIDOS)
sabores_df = carregar_csv(CSV_SABORES, pd.DataFrame({"Sabor": [
    "Frango grelhado", "Feijoada", "Strogonoff de frango",
    "Strogonoff de carne", "Frango assado", "Salmão assado", "Tilápia assada"
]}))

# Autenticação
credentials = {
    "usernames": {
        "admin": {
            "name": "Admin",
            "password": "pbkdf2:sha256:260000$YQWRdj8GlQXV6u5j$6ed944aa7b2e2c529a91b8b75c1893a7f5c2e18cfb9d110d3c04d36044fbd4e7"
        }
    }
}
authenticator = stauth.Authenticate(credentials, "meal_prep", "abcdef", cookie_expiry_days=30)
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

    menu = st.sidebar.selectbox("📁 Navegação", [
        "📦 Cadastrar Pedido",
        "📊 Resumo de Produção",
        "👤 Clientes",
        "🍽️ Sabores",
        "💰 Pagamentos"
    ])

    # ---------------- PEDIDOS ----------------
    if "Cadastrar Pedido" in menu:
        st.subheader("Cadastrar Pedido")
        if not clientes_df.empty:
            cliente = st.selectbox("Cliente", clientes_df["Nome"])
            sabor = st.selectbox("Sabor da Marmita", sabores_df["Sabor"])
            quantidade = st.number_input("Quantidade", min_value=1, step=1)
            data_pedido = st.date_input("Data da entrega", value=date.today())

            if st.button("Registrar Pedido", type="primary"):
                novo_pedido = pd.DataFrame({
                    "Cliente": [cliente], "Sabor": [sabor],
                    "Quantidade": [quantidade], "Data": [data_pedido],
                    "Pago": [False], "Entregue": [False]
                })
                pedidos_df = pd.concat([pedidos_df, novo_pedido], ignore_index=True)
                pedidos_df.to_csv(CSV_PEDIDOS, index=False)
                st.success("Pedido registrado com sucesso!")
        else:
            st.warning("Nenhum cliente cadastrado ainda.")

        if not pedidos_df.empty:
            st.subheader("Alterar Pedidos Existentes")
            for i, row in pedidos_df.iterrows():
                with st.expander(f"Pedido {i+1} - {row['Cliente']}"):
                    pedidos_df.at[i, "Cliente"] = st.selectbox("Cliente", clientes_df["Nome"],
                        index=clientes_df[clientes_df["Nome"] == row["Cliente"]].index[0], key=f"cliente_{i}")
                    pedidos_df.at[i, "Sabor"] = st.selectbox("Sabor", sabores_df["Sabor"],
                        index=sabores_df[sabores_df["Sabor"] == row["Sabor"]].index[0], key=f"sabor_{i}")
                    pedidos_df.at[i, "Quantidade"] = st.number_input("Quantidade", min_value=1,
                        step=1, value=int(row["Quantidade"]), key=f"quant_{i}")
                    pedidos_df.at[i, "Data"] = st.date_input("Data da entrega",
                        value=pd.to_datetime(row["Data"]), key=f"data_{i}")
            if st.button("Salvar Alterações nos Pedidos"):
                pedidos_df.to_csv(CSV_PEDIDOS, index=False)
                st.success("Pedidos atualizados com sucesso!")

            if st.button("Zerar todos os pedidos"):
                pedidos_df = pd.DataFrame(columns=pedidos_df.columns)
                pedidos_df.to_csv(CSV_PEDIDOS, index=False)
                st.warning("Todos os pedidos foram zerados.")

    # ---------------- RESUMO ----------------
    elif "Resumo de Produção" in menu:
        st.subheader("Resumo de Produção")

        if not pedidos_df.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📌 Por Cliente")
                resumo_cliente = pedidos_df.groupby("Cliente")["Quantidade"].sum().reset_index()
                resumo_cliente = resumo_cliente.sort_values("Quantidade", ascending=False)
                resumo_cliente.index += 1
                st.dataframe(resumo_cliente, use_container_width=True)

            with col2:
                st.markdown("### 🍽️ Por Sabor")
                resumo_sabor = pedidos_df.groupby("Sabor")["Quantidade"].sum().reset_index()
                resumo_sabor = resumo_sabor.sort_values("Quantidade", ascending=False)
                resumo_sabor.index += 1
                st.dataframe(resumo_sabor, use_container_width=True)

            total_geral = pedidos_df["Quantidade"].sum()
            st.markdown("---")
            st.success(f"**Total geral de marmitas da semana: {total_geral}**")
        else:
            st.info("Nenhum pedido registrado ainda.")

    # ---------------- CLIENTES ----------------
    elif "Clientes" in menu:
        st.subheader("Clientes Cadastrados")
        if not clientes_df.empty:
            clientes_df_display = clientes_df.copy()
            clientes_df_display.index += 1
            st.dataframe(clientes_df_display)

        st.markdown("### ➕ Adicionar Novo Cliente")
        novo_nome = st.text_input("Nome do Cliente")
        novo_endereco = st.text_input("Endereço (opcional)")
        if st.button("Adicionar Cliente"):
            if novo_nome:
                novo_cliente = pd.DataFrame({"Nome": [novo_nome], "Endereco": [novo_endereco or ""]})
                clientes_df = pd.concat([clientes_df, novo_cliente], ignore_index=True)
                clientes_df.to_csv(CSV_CLIENTES, index=False)
                st.success("Cliente adicionado com sucesso!")
            else:
                st.warning("Informe ao menos o nome do cliente.")

    # ---------------- SABORES ----------------
    elif "Sabores" in menu:
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

    # ---------------- PAGAMENTOS ----------------
    elif "💰 Pagamentos" in menu:
        st.subheader("Controle de Pagamentos e Entregas")
        if not pedidos_df.empty:
            for i, row in pedidos_df.iterrows():
                with st.expander(f"Pedido {i+1}: {row['Cliente']}"):
                    pago = st.checkbox("Pago?", value=row["Pago"], key=f"pago_{i}")
                    entregue = st.checkbox("Entregue?", value=row["Entregue"], key=f"entregue_{i}")
                    pedidos_df.at[i, "Pago"] = pago
                    pedidos_df.at[i, "Entregue"] = entregue

            if st.button("Salvar Alterações de Pagamento"):
                pedidos_df.to_csv(CSV_PEDIDOS, index=False)
                st.success("Alterações salvas com sucesso!")
        else:
            st.info("Nenhum pedido registrado ainda.")

# ---------------- LOGIN ----------------
elif authentication_status is False:
    st.error("Nome de usuário ou senha incorretos.")
elif authentication_status is None:
    st.warning("Por favor, insira suas credenciais para continuar.")
