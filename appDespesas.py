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
if not st.session_state['data'].empty:
    st.dataframe(st.session_state['data'].sort_values(by="Data", ascending=False))
else:
    st.info("Ainda não existem entradas registadas.")

# Resumo financeiro
st.header("Resumo Financeiro")
if not st.session_state['data'].empty:
    df = st.session_state['data'].copy()
    
    # Converter despesas em valores negativos
    df['Valor_Real'] = df.apply(lambda x: -x['Valor'] if x['Tipo'] == 'Despesa' else x['Valor'], axis=1)
    
    # Saldo diário
    saldo_diario = df.groupby('Data')['Valor_Real'].sum().reset_index().sort_values('Data')
    st.subheader("Saldo Diário")
    st.dataframe(saldo_diario)
    
    # Saldo tota


