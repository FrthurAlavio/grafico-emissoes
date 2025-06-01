import streamlit as st
import pandas as pd
import plotly.express as px

# Carrega os dados
df = pd.read_csv("SEEG.csv")

# Transforma os dados para o formato longo
df_melted = df.melt(id_vars="Categoria", var_name="Ano", value_name="Emissões (MtCO2e)")
df_melted["Ano"] = df_melted["Ano"].astype(int)

# Interface Streamlit
st.set_page_config(page_title="Emissões de Gases no Brasil", layout="centered")
st.title("🚩🚩 Principais Setores de Emissão de Gases de Efeito Estufa no Brasil")

# Menu de seleção
grafico_tipo = st.selectbox("Escolha o tipo de gráfico:", ["Gráfico de Linha", "Gráfico de Pizza (apenas de 2023)", "Gráfico de Barras"])

if grafico_tipo == "Gráfico de Linha":
    fig = px.line(
        df_melted,
        x="Ano",
        y="Emissões (MtCO2e)",
        color="Categoria",
        title="Evolução dos principais setores de Emissões de Gases de Efeito Estufa (1990–2023)"
    )
    st.plotly_chart(fig, use_container_width=True)

elif grafico_tipo == "Gráfico de Pizza (2023)":
    df_2023 = df[["Categoria", "2023"]].copy()
    df_2023.columns = ["Categoria", "Emissões"]
    fig = px.pie(
        df_2023,
        values="Emissões",
        names="Categoria",
        title="Participação por Setor nas Emissões em 2023"
    )
    st.plotly_chart(fig, use_container_width=True)

elif grafico_tipo == "Gráfico de Barras":
    ano = st.slider("Escolha o ano", min_value=1990, max_value=2023, value=2023)
    df_ano = df[["Categoria", str(ano)]].copy()
    df_ano.columns = ["Categoria", "Emissões"]
    fig = px.bar(
        df_ano,
        x="Categoria",
        y="Emissões",
        title=f"Emissões de Gases por Setor - {ano}",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Adicional
st.markdown("""
## ℹ️ Sobre os Dados
**Fonte:** [SEEG](https://seeg.eco.br/dados/)
Os dados representam as emissões de gases de efeito estufa (GEE) convertidas em CO₂ equivalente (CO₂e). 
 
- Os valores são expressos em **milhões de toneladas** (Mt)
- Inclui setores como: energia, agropecuária, uso da terra, resíduos e indústria

Feito por [Arquivo Alternativo](https://www.arquivoalternativo.com/)
""")
