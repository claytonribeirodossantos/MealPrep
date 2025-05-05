
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Clientes - Meal Prep USA", layout="wide")

CSV_CLIENTES = "clientes.csv"

def carregar_clientes():
    if os.path.exists(CSV_CLIENTES):
        df = pd.read_csv(CSV_CLIENTES)
        return df
    return pd.DataFrame(columns=["Nome", "Endereco"])

def salvar_clientes(df):
    df.to_csv(CSV_CLIENTES, index=False)

def remover_cliente(df, nome):
    df = df[df["Nome"] != nome]
    salvar_clientes(df)
    return df

def atualizar_cliente(df, nome_antigo, nome_novo, novo_endereco):
    df.loc[df["Nome"] == nome_antigo, "Nome"] = nome_novo
    df.loc[df["Nome"] == nome_novo, "Endereco"] = novo_endereco
    salvar_clientes(df)
    return df

st.markdown("""
    <style>
    .cliente-card {
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        background-color: #f9f9f9;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .cliente-nome {
        font-weight: bold;
        font-size: 18px;
        color: #333;
    }
    .cliente-endereco {
        font-size: 14px;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📇 Clientes - Meal Prep USA")
df_clientes = carregar_clientes()

with st.expander("➕ Adicionar Novo Cliente"):
    nome_novo = st.text_input("Nome do Cliente")
    endereco_novo = st.text_input("Endereço")
    if st.button("✅ Cadastrar"):
        if nome_novo and endereco_novo:
            df_clientes.loc[len(df_clientes)] = [nome_novo, endereco_novo]
            salvar_clientes(df_clientes)
            st.success("Cliente adicionado com sucesso!")
        else:
            st.warning("Preencha os dois campos.")

st.markdown("### 🧾 Lista de Clientes")
for _, row in df_clientes.iterrows():
    with st.container():
        st.markdown('<div class="cliente-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="cliente-nome">{row["Nome"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="cliente-endereco">{row["Endereco"]}</div>', unsafe_allow_html=True)

        col1, col2 = st.columns([1,1])
        with col1:
            if st.button(f"✏️ Editar {row['Nome']}"):
                with st.form(f"form_editar_{row['Nome']}"):
                    novo_nome = st.text_input("Novo Nome", value=row["Nome"])
                    novo_endereco = st.text_input("Novo Endereço", value=row["Endereco"])
                    if st.form_submit_button("Salvar Alterações"):
                        df_clientes = atualizar_cliente(df_clientes, row["Nome"], novo_nome, novo_endereco)
                        st.success("Cliente atualizado com sucesso!")
                        st.experimental_rerun()
        with col2:
            if st.button(f"🗑️ Excluir {row['Nome']}"):
                df_clientes = remover_cliente(df_clientes, row["Nome"])
                st.warning("Cliente removido.")
                st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)
