import pandas as pd
import streamlit as st
import plotly.express as px

# Carregar o DataFrame
caminho_arquivo = "C:\\Users\\pablo paiva\\PROJETOS\\RELATÓRIO ANUAL 2024 DAS ACESSORIAS  - resultado_analise.csv"
df = pd.read_csv(caminho_arquivo)

# Sidebar para filtros
st.sidebar.header("Filtros")
bancos = st.sidebar.multiselect("Filtrar por Banco:", df["Banco"].unique())
assessoria_selecionada = st.sidebar.multiselect("Filtrar por Assessoria:", df["Assessoria"].unique())

# Aplicando filtros
if bancos:
    df = df[df["Banco"].isin(bancos)]
if assessoria_selecionada:
    df = df[df["Assessoria"].isin(assessoria_selecionada)]

# Cálculo das métricas
total_contatos = df["Contagem"].sum()
num_assessorias = df["Assessoria"].nunique()

# Média de contatos por assessoria (separadamente para cada assessoria)
media_contatos_assessoria_separada = df.groupby("Assessoria")["Contagem"].mean()
media_contatos_assessoria = round(media_contatos_assessoria_separada.mean(), 2)

# Outras métricas
banco_mais_contatos = df.groupby("Banco")["Contagem"].sum().idxmax()
assessoria_mais_contatada = df.groupby("Assessoria")["Contagem"].sum().idxmax()
media_contatos_banco = round(df.groupby("Banco")["Contagem"].mean().mean(), 2)
banco_maior_media = df.groupby("Banco")["Contagem"].mean().idxmax()

# Exibir métricas com fontes ajustadas
st.title("📈 Análise de Contatos das Assessorias")

# Ajustando tamanho da fonte para as métricas
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<h3 style='font-size: 18px;'>📞 Total de Contatos</h3>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='font-size: 16px;'>{total_contatos}</h4>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<h3 style='font-size: 18px;'>🏢 Número de Assessorias Únicas</h3>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='font-size: 16px;'>{num_assessorias}</h4>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<h3 style='font-size: 18px;'>📊 Média de Contatos por Assessoria</h3>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='font-size: 16px;'>{media_contatos_assessoria}</h4>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown(f"<h3 style='font-size: 18px;'>🏦 Banco com mais contatos</h3>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='font-size: 16px;'>{banco_mais_contatos}</h4>", unsafe_allow_html=True)

with col5:
    st.markdown(f"<h3 style='font-size: 18px;'>💼 Assessoria mais contatada</h3>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='font-size: 16px;'>{assessoria_mais_contatada}</h4>", unsafe_allow_html=True)

with col6:
    st.markdown(f"<h3 style='font-size: 18px;'>📉 Média de contatos por banco</h3>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='font-size: 16px;'>{media_contatos_banco}</h4>", unsafe_allow_html=True)

# Reduzindo o tamanho da fonte para o valor de cada métrica
st.markdown(f"<h3 style='font-size: 18px;'>📊 Banco com maior média de contatos por assessoria</h3>", unsafe_allow_html=True)
st.markdown(f"<h4 style='font-size: 16px;'>{banco_maior_media}</h4>", unsafe_allow_html=True)


# Top 10 assessorias mais contatadas
top_assessorias = df.groupby("Assessoria")["Contagem"].sum().reset_index()
top_assessorias = top_assessorias.sort_values(by="Contagem", ascending=False).head(10)

# Gráfico de barras - Top 10 assessorias
fig_bar = px.bar(top_assessorias, x="Assessoria", y="Contagem", title="Top 10 Assessorias Mais Contatadas")
st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico dinâmico para bancos mais relevantes - abaixo do gráfico das assessorias
if assessoria_selecionada:
    df_bancos = df.groupby("Banco")["Contagem"].sum().reset_index()
    df_bancos = df_bancos.sort_values(by="Contagem", ascending=True)  # Ordenando para gráfico horizontal

    fig_bancos = px.bar(df_bancos, x="Contagem", y="Banco", orientation="h", 
                        title=f"Bancos com mais retorno - {', '.join(assessoria_selecionada)}")
    st.plotly_chart(fig_bancos, use_container_width=True)
else:
    st.write("### Selecione uma assessoria para ver o retorno dos bancos.")

# Exibir tabela filtrada
st.write("### 📋 Dados Filtrados:")
st.dataframe(df)
