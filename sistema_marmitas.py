
import streamlit as st
import pandas as pd
from datetime import date

# ============================ CONFIGURAÇÕES ============================
st.set_page_config(page_title="Meal Prep USA", layout="wide")

# Logo e título
st.image("https://raw.githubusercontent.com/claytonribeirodossantos/MealPrep/main/logo_mealprepusa.jpeg", width=300)
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Sistema Interno de Gestão de Marmitas</h1>", unsafe_allow_html=True)
st.markdown("---")

# ============================ DADOS INICIAIS ============================
sabores = [
    "Frango grelhado",
    "Feijoada",
    "Strogonoff de frango",
    "Strogonoff de carne",
    "Frango assado",
    "Salmão assado",
    "Tilápia assada"
]

clientes = {
    "Andrey": "924 Venice Drive, Silver Spring, MD, USA"
}

pedidos = []

# ============================ MENU LATERAL ============================
menu = st.sidebar.radio("Menu", ["Cadastrar Pedido", "Resumo de Produção", "Clientes", "Sabores", "Pagamentos"])

# ============================ TELA: PEDIDOS ============================
if menu == "Cadastrar Pedido":
    st.subheader("Cadastrar Pedido")
    cliente = st.selectbox("Cliente", list(clientes.keys()))
    sabor = st.selectbox("Sabor da Marmita", sabores)
    quantidade = st.number_input("Quantidade", min_value=1, step=1)
    data_pedido = st.date_input("Data da entrega", value=date.today())

    if st.button("Registrar Pedido", type="primary"):
        pedidos.append({
            "Cliente": cliente,
            "Sabor": sabor,
            "Quantidade": quantidade,
            "Data": data_pedido,
            "Pago": False,
            "Entregue": False
        })
        st.success("Pedido registrado com sucesso!")

# ============================ TELA: PRODUÇÃO ============================
elif menu == "Resumo de Produção":
    st.subheader("Resumo de Produção por Sabor")
    if pedidos:
        df_pedidos = pd.DataFrame(pedidos)
        resumo = df_pedidos.groupby("Sabor")["Quantidade"].sum().reset_index()
        st.table(resumo)
    else:
        st.info("Nenhum pedido registrado ainda.")

# ============================ TELA: CLIENTES ============================
elif menu == "Clientes":
    st.subheader("Clientes Cadastrados")
    for nome, endereco in clientes.items():
        st.write(f"- **{nome}**: {endereco}")
    
    st.markdown("### Adicionar Novo Cliente")
    novo_nome = st.text_input("Nome do Cliente")
    novo_endereco = st.text_input("Endereço")

    if st.button("Adicionar Cliente"):
        if novo_nome and novo_endereco:
            clientes[novo_nome] = novo_endereco
            st.success(f"Cliente {novo_nome} adicionado!")
        else:
            st.warning("Preencha todos os campos.")

# ============================ TELA: SABORES ============================
elif menu == "Sabores":
    st.subheader("Sabores Disponíveis")
    for s in sabores:
        st.write(f"- {s}")
    
    st.markdown("### Adicionar Novo Sabor")
    novo_sabor = st.text_input("Novo Sabor")

    if st.button("Adicionar Sabor"):
        if novo_sabor:
            sabores.append(novo_sabor)
            st.success(f"Sabor '{novo_sabor}' adicionado!")
        else:
            st.warning("Informe o nome do sabor.")

# ============================ TELA: PAGAMENTOS ============================
elif menu == "Pagamentos":
    st.subheader("Controle de Pagamentos e Entregas")
    if pedidos:
        df_pedidos = pd.DataFrame(pedidos)
        for i, row in df_pedidos.iterrows():
            st.markdown(f"### Pedido {i+1}")
            st.write(f"Cliente: {row['Cliente']}")
            st.write(f"Sabor: {row['Sabor']}")
            st.write(f"Quantidade: {row['Quantidade']}")
            st.write(f"Data: {row['Data']}")

            pago = st.checkbox("Pago?", value=row["Pago"], key=f"pago_{i}")
            entregue = st.checkbox("Entregue?", value=row["Entregue"], key=f"entregue_{i}")

            pedidos[i]["Pago"] = pago
            pedidos[i]["Entregue"] = entregue
    else:
        st.info("Nenhum pedido registrado ainda.")
