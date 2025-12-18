import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Despesas & Receitas", layout="wide")
st.title("💰 App Avançada de Despesas e Receitas")

# Inicializar ou carregar dados
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Data', 'Tipo', 'Categoria', 'Descrição', 'Valor'])

# Sidebar: nova entrada
with st.sidebar:
    st.header("➕ Nova Entrada")
    tipo = st.selectbox("Tipo", ["Despesa", "Receita"])
    categoria = st.text_input("Categoria")
    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor", min_value=0.0, format="%.2f")
    data_entrada = st.date_input("Data", datetime.today())
    if st.button("Adicionar"):
        nova_linha = {
            "Data": data_entrada,
            "Tipo": tipo,
            "Categoria": categoria,
            "Descrição": descricao,
            "Valor": valor
        }
        st.session_state['data'] = pd.concat([st.session_state['data'], pd.DataFrame([nova_linha])], ignore_index=True)
        st.success(f"{tipo} adicionada com sucesso!")

# Preparar dados
df = st.session_state['data'].copy()
if not df.empty:
    df['Valor_Real'] = df.apply(lambda x: -x['Valor'] if x['Tipo']=="Despesa" else x['Valor'], axis=1)
    df = df.sort_values('Data')
    df['Saldo_Acumulado'] = df['Valor_Real'].cumsum()

# Abas principais
tabs = st.tabs(["📋 Histórico", "📊 Resumo", "📈 Gráficos", "💾 Exportar"])

# Aba 1: Histórico
with tabs[0]:
    st.header("Histórico de Entradas")
    if not df.empty:
        st.dataframe(df.sort_values(by="Data", ascending=False))
    else:
        st.info("Ainda não existem entradas registadas.")

# Aba 2: Resumo
with tabs[1]:
    st.header("Resumo Financeiro")
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        saldo_total = df['Valor_Real'].sum()
        receitas_total = df[df['Tipo']=="Receita"]['Valor'].sum()
        despesas_total = df[df['Tipo']=="Despesa"]['Valor'].sum()
        
        col1.metric("Saldo Total", f"{saldo_total:.2f}")
        col2.metric("Total Receitas", f"{receitas_total:.2f}")
        col3.metric("Total Despesas", f"{despesas_total:.2f}")
    else:
        st.info("Sem dados para resumo.")

# Aba 3: Gráficos
with tabs[2]:
    st.header("Visualização Gráfica Avançada")
    if not df.empty:
        # Filtros
        categorias = ["Todos"] + df['Categoria'].unique().tolist()
        categoria_filtro = st.selectbox("Filtrar por Categoria", categorias)
        df_grafico = df.copy()
        if categoria_filtro != "Todos":
            df_grafico = df_grafico[df_grafico['Categoria']==categoria_filtro]

        # Gráfico diário de receitas e despesas
        st.subheader("Receitas e Despesas por Dia")
        df_diario = df_grafico.pivot_table(index='Data', columns='Tipo', values='Valor', aggfunc='sum').fillna(0)
        st.bar_chart(df_diario)

        # Gráfico de saldo acumulado
        st.subheader("Saldo Acumulado")
        st.line_chart(df_grafico.set_index('Data')['Saldo_Acumulado'])

        # Gráfico por categoria
        st.subheader("Total por Categoria")
        df_categoria = df_grafico.groupby(['Categoria','Tipo'])['Valor'].sum().unstack(fill_value=0)
        st.bar_chart(df_categoria)
    else:
        st.info("Sem dados para gráficos.")

# Aba 4: Exportação
with tabs[3]:
    st.header("Exportar Dados")
    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar CSV",
            data=csv,
            file_name='despesas_receitas.csv',
            mime='text/csv'
        )
    else:
        st.info("Sem dados para exportar.")



