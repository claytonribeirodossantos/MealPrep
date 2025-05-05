
import streamlit as st
import pandas as pd
from datetime import date
import os

# ========== CONFIGURAÇÕES ==========
st.set_page_config(page_title="Meal Prep USA", layout="wide")

# ========== LOGIN ==========
usuarios = {"admin": "1234", "cozinha": "marmita"}
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.image("https://raw.githubusercontent.com/willianrod/mealprepusa/main/logo_mealprepusa.jpeg", width=300)
    st.title("Login - Meal Prep USA")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario in usuarios and usuarios[usuario] == senha:
            st.session_state.logado = True
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos")
    st.stop()

# ========== DADOS ==========
CSV_CLIENTES = "clientes.csv"

if os.path.exists(CSV_CLIENTES):
    df_clientes = pd.read_csv(CSV_CLIENTES)
    clientes = dict(zip(df_clientes["Nome"], df_clientes["Endereco"]))
else:
    clientes = {}

sabores = [
    "Frango grelhado", "Feijoada", "Strogonoff de frango",
    "Strogonoff de carne", "Frango assado", "Salmão assado", "Tilápia assada"
]
pedidos = []

# ========== INTERFACE ==========
st.image("https://raw.githubusercontent.com/willianrod/mealprepusa/main/logo_mealprepusa.jpeg", width=300)
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Sistema Interno de Gestão de Marmitas</h1>", unsafe_allow_html=True)
st.markdown("---")
menu = st.sidebar.radio("Menu", ["Cadastrar Pedido", "Resumo de Produção", "Clientes", "Sabores", "Pagamentos"])

# ========== PEDIDOS ==========
if menu == "Cadastrar Pedido":
    st.subheader("Cadastrar Pedido")
    if clientes:
        cliente = st.selectbox("Cliente", list(clientes.keys()))
        sabor = st.selectbox("Sabor da Marmita", sabores)
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        data_pedido = st.date_input("Data da entrega", value=date.today())
        if st.button("Registrar Pedido", type="primary"):
            pedidos.append({
                "Cliente": cliente, "Sabor": sabor,
                "Quantidade": quantidade, "Data": data_pedido,
                "Pago": False, "Entregue": False
            })
            st.success("Pedido registrado com sucesso!")
    else:
        st.warning("Nenhum cliente cadastrado ainda.")

# ========== PRODUÇÃO ==========
elif menu == "Resumo de Produção":
    st.subheader("Resumo de Produção por Sabor")
    if pedidos:
        df = pd.DataFrame(pedidos)
        resumo = df.groupby("Sabor")["Quantidade"].sum().reset_index()
        st.table(resumo)
    else:
        st.info("Nenhum pedido registrado ainda.")

# ========== CLIENTES ==========
elif menu == "Clientes":
    st.subheader("Clientes Cadastrados")
    if clientes:
        for nome, endereco in clientes.items():
            st.write(f"- **{nome}**: {endereco}")
    else:
        st.info("Nenhum cliente cadastrado ainda.")

    st.markdown("### Adicionar Novo Cliente")
    novo_nome = st.text_input("Nome do Cliente")
    novo_endereco = st.text_input("Endereço")
    if st.button("Adicionar Cliente"):
        if novo_nome and novo_endereco:
            clientes[novo_nome] = novo_endereco
            df = pd.DataFrame(list(clientes.items()), columns=["Nome", "Endereco"])
            df.to_csv(CSV_CLIENTES, index=False)
            st.success(f"Cliente {novo_nome} adicionado com sucesso!")
        else:
            st.warning("Preencha todos os campos.")

    st.markdown("### Editar Cliente Existente")
    cliente_editar = st.selectbox("Selecione o cliente", list(clientes.keys()))
    novo_nome_editar = st.text_input("Novo nome", value=cliente_editar)
    novo_endereco_editar = st.text_input("Novo endereço", value=clientes[cliente_editar])
    if st.button("Salvar Alterações"):
        if novo_nome_editar and novo_endereco_editar:
            clientes.pop(cliente_editar)
            clientes[novo_nome_editar] = novo_endereco_editar
            df = pd.DataFrame(list(clientes.items()), columns=["Nome", "Endereco"])
            df.to_csv(CSV_CLIENTES, index=False)
            st.success("Cliente atualizado com sucesso!")

# ========== SABORES ==========
elif menu == "Sabores":
    st.subheader("Sabores Disponíveis")
    for s in sabores:
        st.write(f"- {s}")
    novo_sabor = st.text_input("Novo Sabor")
    if st.button("Adicionar Sabor"):
        if novo_sabor:
            sabores.append(novo_sabor)
            st.success(f"Sabor '{novo_sabor}' adicionado!")
        else:
            st.warning("Informe o nome do sabor.")

# ========== PAGAMENTOS ==========
elif menu == "Pagamentos":
    st.subheader("Controle de Pagamentos e Entregas")
    if pedidos:
        df = pd.DataFrame(pedidos)
        for i, row in df.iterrows():
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
