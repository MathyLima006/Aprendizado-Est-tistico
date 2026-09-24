import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração

st.set_page_config(
    page_title="World Population",
    page_icon="🌎",
    layout="wide"
)

# Dados

dados = pd.read_excel("Pasta1.xlsx")

# Menu

st.sidebar.title("🌎 World Population")

pagina = st.sidebar.radio(
    "Página",
    ["Visão Geral", "Explorar País"]
)

# PÁGINA 1

if pagina == "Visão Geral":

    st.title("🌎 World Population")
    st.write("Dashboard sobre a população mundial.")

    # Indicadores
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Países",
            len(dados)
        )

    with col2:
        st.metric(
            "População em 2022",
            f"{dados['2022 Population'].sum() / 1e9:.2f} bilhões"
        )

    with col3:
        maior = dados.loc[
            dados["2022 Population"].idxmax(),
            "Country"
        ]

        st.metric(
            "País mais populoso",
            maior
        )

    st.divider()

    # Top 10 países

    st.subheader("🏆 Top 10 países por população")

    top10 = dados.nlargest(
        10,
        "2022 Population"
    ).sort_values("2022 Population")

    grafico = px.bar(
        top10,
        x="2022 Population",
        y="Country",
        orientation="h",
        title="População em 2022"
    )

    st.plotly_chart(
        grafico,
        use_container_width=True
    )

    # Evolução mundial

    st.subheader("📈 Evolução da população mundial")

    anos = [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022]

    populacao = [
        dados["1970 Population"].sum(),
        dados["1980 Population"].sum(),
        dados["1990 Population"].sum(),
        dados["2000 Population"].sum(),
        dados["2010 Population"].sum(),
        dados["2015 Population"].sum(),
        dados["2020 Population"].sum(),
        dados["2022 Population"].sum()
    ]

    historico = pd.DataFrame({
        "Ano": anos,
        "População": populacao
    })

    grafico = px.line(
        historico,
        x="Ano",
        y="População",
        markers=True,
        title="Crescimento da população mundial"
    )

    st.plotly_chart(
        grafico,
        use_container_width=True
    )

# PÁGINA 2

else:

    st.title("🔎 Explorar País")

    paises = sorted(
        dados["Country"].unique()
    )

    pais_escolhido = st.selectbox(
        "Escolha um país:",
        paises
    )

    pais = dados[
        dados["Country"] == pais_escolhido
    ].iloc[0]

    st.subheader(f"🌎 {pais_escolhido}")

    # Informações
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "População",
            f"{pais['2022 Population']:,.0f}"
        )

    with col2:
        st.metric(
            "Área",
            f"{pais['Area (km²)']:,.0f} km²"
        )

    with col3:
        st.metric(
            "Densidade",
            f"{pais['Density (per km²)']:.2f}"
        )

    st.divider()

    # Informações básicas
    st.write(
        f"**Capital:** {pais['Capital']}"
    )

    st.write(
        f"**Continente:** {pais['Continent']}"
    )

    st.write(
        f"**Ranking mundial:** {pais['Rank']}"
    )

    # Evolução do país

    st.subheader("📈 Evolução da população")

    anos = [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022]

    populacao = [
        pais["1970 Population"],
        pais["1980 Population"],
        pais["1990 Population"],
        pais["2000 Population"],
        pais["2010 Population"],
        pais["2015 Population"],
        pais["2020 Population"],
        pais["2022 Population"]
    ]

    historico = pd.DataFrame({
        "Ano": anos,
        "População": populacao
    })

    grafico = px.line(
        historico,
        x="Ano",
        y="População",
        markers=True,
        title=f"População de {pais_escolhido}"
    )

    st.plotly_chart(
        grafico,
        use_container_width=True
    )

