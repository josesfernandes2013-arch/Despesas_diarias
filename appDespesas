import streamlit as st
import pandas as pd
from datetime import datetime

# Título da aplicação
st.title("App de Registo de Despesas e Receitas Diárias")

# Inicializar ou carregar dados
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Data', 'Tipo', 'Categoria', 'Descrição', 'Valor'])

# Formulário para adicionar uma nova entrada
st.header("Adicionar nova entrada")
with st.form("nova_entrada"):
    tipo = st.selectbox("Tipo", ["Despesa", "Receita"])
    categoria = st.text_input("Categoria")
    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor", min_value=0.0, format="%.2f")
    data_entrada = st.date_input("Data", datetime.today())
    
    submit = st.form_submit_button("Adicionar")
    
    if submit:
        nova_linha = {
            "Data": data_entrada,
            "Tipo": tipo,
            "Categoria": categoria,
            "Descrição": descricao,
            "Valor": valor
        }
        st.session_state['data'] = pd.concat([st.session_state['data'], pd.DataFrame([nova_linha])], ignore_index=True)
        st.success(f"{tipo} adicionada com sucesso!")

# Visualizar histórico
st.header("Histórico de Entradas")
st.dataframe(st.session_state['data'].sort_values(by="Data", ascending=False))

# Resumo financeiro
st.header("Resumo Diário")
if not st.session_state['data'].empty:
    resumo = st.session_state['data'].copy()
    resumo['Valor'] = resumo.apply(lambda x: -x['Valor'] if x['Tipo'] == 'Despesa' else x['Valor'], axis=1)
    saldo_diario = resumo.groupby('Data')['Valor'].sum().reset_index().sort_values('Data', ascending=False)
    saldo_total = saldo_diario['Valor'].sum()
    
    st.subheader("Saldo Diário")
    st.dataframe(saldo_diario)
    
    st.subheader(f"Saldo Total: {saldo_total:.2f}")
else:
    st.info("Ainda não existem entradas registadas.")

# Rodar com: streamlit run nome_do_arquivo.py
