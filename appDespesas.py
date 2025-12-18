import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

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
st.header("Resumo Financeiro")
if not st.session_state['data'].empty:
    df = st.session_state['data'].copy()
    
    # Converter despesas em valores negativos
    df['Valor_Real'] = df.apply(lambda x: -x['Valor'] if x['Tipo'] == 'Despesa' else x['Valor'], axis=1)
    
    # Saldo diário
    saldo_diario = df.groupby('Data')['Valor_Real'].sum().reset_index().sort_values('Data')
    st.subheader("Saldo Diário")
    st.dataframe(saldo_diario)
    
    # Saldo total
    saldo_total = saldo_diario['Valor_Real'].sum()
    st.subheader(f"Saldo Total: {saldo_total:.2f}")
    
    # Gráfico: receitas vs despesas por dia
    st.subheader("Receitas e Despesas por Dia")
    df_grafico = df.copy()
    df_grafico['Valor_Pos'] = df_grafico['Valor']
    df_grafico.loc[df_grafico['Tipo'] == 'Despesa', 'Valor_Pos'] *= -1
    fig1 = px.bar(df_grafico, x='Data', y='Valor_Pos', color='Tipo', text='Valor_Pos', title="Receitas vs Despesas por Dia")
    st.plotly_chart(fig1)
    
    # Gráfico: despesas e receitas por categoria
    st.subheader("Despesas e Receitas por Categoria")
    df_categoria = df.groupby(['Categoria', 'Tipo'])['Valor'].sum().reset_index()
    fig2 = px.bar(df_categoria, x='Categoria', y='Valor', color='Tipo', barmode='group', text='Valor',
                  title="Despesas e Receitas por Categoria")
    st.plotly_chart(fig2)
    
else:
    st.info("Ainda não existem entradas registadas.")

