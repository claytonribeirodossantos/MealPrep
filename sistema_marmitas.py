
import streamlit as st
import pandas as pd
from datetime import date

# Inicialização dos dados (poderia ser lido de um arquivo)
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

st.set_page_config(page_title="Sistema de Marmitas - Interno", layout="wide")
st.title("Sistema Interno de Gestão de Marmitas")

menu = st.sidebar.radio("Menu", ["Cadastrar Pedido", "Resumo de Produção", "Clientes", "Sabores", "Pagamentos"])

# 1. Cadastrar Pedido
if menu == "Cadastrar Pedido":
    st.header("Cadastrar Pedido")
    cliente = st.selectbox("Cliente", list(clientes.keys()))
    sabor = st.selectbox("Sabor da Marmita", sabores)
    quantidade = st.number_input("Quantidade", min_value=1, step=1)
    data_pedido = st.date_input("Data da entrega", value=date.today())

    if st.button("Registrar Pedido"):
        pedidos.append({
            "Cliente": cliente,
            "Sabor": sabor,
            "Quantidade": quantidade,
            "Data": data_pedido,
            "Pago": False,
            "Entregue": False
        })
        st.success("Pedido registrado com sucesso!")

# 2. Resumo de Produção
elif menu == "Resumo de Produção":
    st.header("Resumo de Produção por Sabor")
    if pedidos:
        df_pedidos = pd.DataFrame(pedidos)
        resumo = df_pedidos.groupby("Sabor")["Quantidade"].sum().reset_index()
        st.table(resumo)
    else:
        st.info("Nenhum pedido registrado ainda.")

# 3. Gerenciar Clientes
elif menu == "Clientes":
    st.header("Clientes Cadastrados")
    for nome, endereco in clientes.items():
        st.write(f"- **{nome}**: {endereco}")
    
    st.subheader("Adicionar Novo Cliente")
    novo_nome = st.text_input("Nome do Cliente")
    novo_endereco = st.text_input("Endereço")

    if st.button("Adicionar Cliente"):
        if novo_nome and novo_endereco:
            clientes[novo_nome] = novo_endereco
            st.success(f"Cliente {novo_nome} adicionado!")
        else:
            st.warning("Preencha todos os campos.")

# 4. Gerenciar Sabores
elif menu == "Sabores":
    st.header("Sabores Disponíveis")
    for s in sabores:
        st.write(f"- {s}")
    
    st.subheader("Adicionar Novo Sabor")
    novo_sabor = st.text_input("Novo Sabor")

    if st.button("Adicionar Sabor"):
        if novo_sabor:
            sabores.append(novo_sabor)
            st.success(f"Sabor '{novo_sabor}' adicionado!")
        else:
            st.warning("Informe o nome do sabor.")

# 5. Pagamentos
elif menu == "Pagamentos":
    st.header("Controle de Pagamentos e Entregas")
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
