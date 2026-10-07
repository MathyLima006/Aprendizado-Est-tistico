import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
import plotly.graph_objects as go

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
    ["Visão Geral", "Explorar País", "Classificação SVM"]
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

    # População por continente

    st.subheader("🌍 População por continente")

    continente = (
        dados.groupby("Continent")["2022 Population"]
        .sum()
        .reset_index()
        .sort_values("2022 Population", ascending=True)
    )

    # Converter para bilhões
    continente["População"] = continente["2022 Population"] / 1_000_000_000

    grafico = px.bar(
        continente,
        x="População",
        y="Continent",
        orientation="h",
        title="População mundial por continente em 2022",
        labels={
            "População": "População (bilhões)",
            "Continent": "Continente"
        },
        text="População"
    )

    # Mostrar o valor no final de cada barra
    # Formatação dos valores
    
    def formatar_populacao(valor):
        if valor >= 1:
            return f"{valor:.2f}".replace(".", ",") + " B"
        else:
            return f"{valor * 1000:.0f} M"

    continente["Texto"] = continente["População"].apply(formatar_populacao)

    grafico.update_traces(
        text=continente["Texto"],
        textposition="outside"
    )

    grafico.update_layout(
        height=450,
        title_x=0.5,

        xaxis=dict(
            title="População (bilhões)",
            tickformat=".1f",
            dtick=1
        ),

        yaxis=dict(
            title=""
        ),

        margin=dict(
            l=20,
            r=130,
            t=70,
            b=20
        )
    )

    st.plotly_chart(
        grafico,
        use_container_width=True
    )

    # População x Área

    st.subheader("📊 População × Área dos países")

    grafico = px.scatter(
    dados,
    x="Area (km²)",
    y="2022 Population",
    hover_name="Country",
    color="Continent",
    title="Relação entre área e população em 2022",
    labels={
        "Area (km²)": "Área",
        "2022 Population": "População",
        "Continent": "Continente"
    }
    )

    # Escala logarítmica
    
    grafico.update_xaxes(
    type="log",
    tickvals=[
        1e3,
        1e4,
        1e5,
        1e6,
        1e7
    ],
    ticktext=[
        "1 mil",
        "10 mil",
        "100 mil",
        "1 M",
        "10 M"
    ],
    title=""
    )

    grafico.update_yaxes(
    type="log",
    tickvals=[
        1e4,
        1e5,
        1e6,
        1e7,
        1e8,
        1e9
    ],
    ticktext=[
        "10 mil",
        "100 mil",
        "1 M",
        "10 M",
        "100 M",
        "1 B"
    ],
    title="População"
    )

  # Aparência dos pontos
    
    grafico.update_traces(
    marker=dict(
        size=9,
        opacity=0.75
    )
    )

    grafico.update_layout(
    height=520,
    title_x=0.5,

    legend_title_text="Continente",

    margin=dict(
        l=20,
        r=20,
        t=70,
        b=20
    )
    )

    st.plotly_chart(
    grafico,
    use_container_width=True
     )


    # Mapa da densidade populacional


    st.subheader("🗺️ Densidade populacional por país")

   # Criar escala logarítmica da densidade
    
    dados["Densidade Log"] = dados["Density (per km²)"].apply(
    lambda x: np.log10(x) if x > 0 else 0
    )

    grafico = px.choropleth(
    dados,
    locations="Country",
    locationmode="country names",
    color="Densidade Log",
    hover_name="Country",
    hover_data={
        "Density (per km²)": ":.2f",
        "2022 Population": ":,.0f",
        "Continent": True,
        "Densidade Log": False
    },
    title="Densidade populacional por país em 2022",
    labels={
        "Density (per km²)": "Densidade (hab/km²)",
        "2022 Population": "População",
        "Continent": "Continente"
    },
    color_continuous_scale="Plasma"
    )

    grafico.update_coloraxes(
    colorbar=dict(
        title="Hab/km²",
        tickvals=[0, 1, 2, 3, 4],
        ticktext=[
            "1",
            "10",
            "100",
            "1 mil",
            "10 mil"
        ]
    )
    )

    grafico.update_layout(
    height=550,
    title_x=0.5,
    margin=dict(
        l=0,
        r=0,
        t=70,
        b=0
    )
)

    st.plotly_chart(
    grafico,
    use_container_width=True
    )
    
    # 2 Página 
elif pagina == "Explorar País":

    st.title("🔎Explorar País")

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
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "População",
            f"{pais['2022 Population']:,.0f}"
        )
    
    with col2:
        st.metric(
            "Área (km²)",
            f"{pais['Area (km²)']:,.0f}"
        )
    
    with col3:
        st.metric(
            "Densidade",
            f"{pais['Density (per km²)']:.2f}"
        )
    
    with col4:
        crescimento = (
            pais["2022 Population"] / pais["1970 Population"] - 1
        ) * 100
    
        st.metric(
            "Crescimento desde 1970",
            f"{crescimento:.1f}%"
        )
    
    
    st.divider()
    
    
    # Informações básicas
    st.write(f"**Capital:** {pais['Capital']}")
    st.write(f"**Continente:** {pais['Continent']}")
    st.write(f"**Ranking mundial:** {pais['Rank']}")
    
    
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
    
    st.divider()
    
    # Comparação entre países
    
    st.subheader("⚖️ Comparar Países")
    
    col1, col2 = st.columns(2)
    
    with col1:
        pais1_escolhido = st.selectbox(
            "Primeiro país",
            dados["Country"],
            key="pais1"
        )
    
    with col2:
        pais2_escolhido = st.selectbox(
            "Segundo país",
            dados["Country"],
            key="pais2"
        )
    
    pais1 = dados[dados["Country"] == pais1_escolhido].iloc[0]
    pais2 = dados[dados["Country"] == pais2_escolhido].iloc[0]
    
    st.write("### 📊 Comparação")
    
    # Crescimento desde 1970
    crescimento1 = (
        pais1["2022 Population"] / pais1["1970 Population"] - 1
    ) * 100
    
    crescimento2 = (
        pais2["2022 Population"] / pais2["1970 Population"] - 1
    ) * 100
    
    # Aumento absoluto da população
    aumento1 = (
        pais1["2022 Population"] - pais1["1970 Population"]
    )
    
    aumento2 = (
        pais2["2022 Population"] - pais2["1970 Population"]
    )
    
    
    # Crescimento desde 1970
    crescimento1 = (
        pais1["2022 Population"] / pais1["1970 Population"] - 1
    ) * 100
    
    crescimento2 = (
        pais2["2022 Population"] / pais2["1970 Population"] - 1
    ) * 100
    
    
    # Aumento absoluto da população
    aumento1 = pais1["2022 Population"] - pais1["1970 Population"]
    aumento2 = pais2["2022 Population"] - pais2["1970 Population"]
    
    
    def formatar_numero(valor):
        valor = abs(valor)
    
        if valor >= 1_000_000_000:
            return f"{valor / 1_000_000_000:.2f} B"
    
        elif valor >= 1_000_000:
            return f"{valor / 1_000_000:.2f} M"
    
        elif valor >= 1_000:
            return f"{valor / 1_000:.1f} mil"
    
        return f"{valor:,.0f}"
    
    
    def mostrar_crescimento(valor):
        if valor > 0:
            return f"🟢 ▲ {valor:.1f}%"
        elif valor < 0:
            return f"🔴 ▼ {abs(valor):.1f}%"
        else:
            return "⚪ — 0%"
    
    
    def mostrar_aumento(valor):
        if valor > 0:
            return f"🟢 +{formatar_numero(valor)}"
        elif valor < 0:
            return f"🔴 -{formatar_numero(valor)}"
        else:
            return "⚪ 0"
    
    
    # Tabela de comparação
    col1, col2, col3 = st.columns([1.5, 1, 1])
    
    with col1:
        st.write("### Indicador")
        st.write("População")
        st.write("Área (km²)")
        st.write("Densidade")
        st.write("Ranking")
        st.write("Crescimento desde 1970")
        st.write("Aumento populacional")
    
    with col2:
        st.write(f"### {pais1_escolhido}")
        st.write(formatar_numero(pais1["2022 Population"]))
        st.write(formatar_numero(pais1["Area (km²)"]))
        st.write(f"{pais1['Density (per km²)']:.2f}")
        st.write(f"{int(pais1['Rank'])}º")
        st.write(mostrar_crescimento(crescimento1))
        st.write(mostrar_aumento(aumento1))
    
    with col3:
        st.write(f"### {pais2_escolhido}")
        st.write(formatar_numero(pais2["2022 Population"]))
        st.write(formatar_numero(pais2["Area (km²)"]))
        st.write(f"{pais2['Density (per km²)']:.2f}")
        st.write(f"{int(pais2['Rank'])}º")
        st.write(mostrar_crescimento(crescimento2))
        st.write(mostrar_aumento(aumento2))
    
    
    # Evolução dos dois países
    anos = [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022]
    
    comparacao = pd.DataFrame({
        "Ano": anos,
        pais1_escolhido: [
            pais1["1970 Population"],
            pais1["1980 Population"],
            pais1["1990 Population"],
            pais1["2000 Population"],
            pais1["2010 Population"],
            pais1["2015 Population"],
            pais1["2020 Population"],
            pais1["2022 Population"]
        ],
        pais2_escolhido: [
            pais2["1970 Population"],
            pais2["1980 Population"],
            pais2["1990 Population"],
            pais2["2000 Population"],
            pais2["2010 Population"],
            pais2["2015 Population"],
            pais2["2020 Population"],
            pais2["2022 Population"]
        ]
    })
    
    comparacao = comparacao.melt(
        id_vars="Ano",
        var_name="País",
        value_name="População"
    )
    
    grafico = px.line(
        comparacao,
        x="Ano",
        y="População",
        color="País",
        markers=True,
        title=f"Evolução da população: {pais1_escolhido} × {pais2_escolhido}"
    )
    
    maior_populacao = comparacao["População"].max()
    
    if maior_populacao < 100_000_000:
        intervalo = 10_000_000
    elif maior_populacao < 500_000_000:
        intervalo = 50_000_000
    elif maior_populacao < 1_000_000_000:
        intervalo = 100_000_000
    else:
        intervalo = 200_000_000
    
    limite = (
        int(maior_populacao / intervalo) + 1
    ) * intervalo
    
    valores = list(range(0, limite + intervalo, intervalo))
    
    def formatar_eixo(valor):
        if valor >= 1_000_000_000:
            return f"{valor / 1_000_000_000:.1f}B"
        else:
            return f"{valor / 1_000_000:.0f}M"
    
    grafico.update_yaxes(
        tickvals=valores,
        ticktext=[formatar_eixo(valor) for valor in valores],
        title="População"
    )
    
    grafico.update_layout(
        height=500,
        title_x=0.5,
        margin=dict(l=20, r=20, t=70, b=20)
    )
    
    st.plotly_chart(
        grafico,
        use_container_width=True
    )
    
    if crescimento1 > crescimento2:
        st.success(
            f"🏆 {pais1_escolhido} teve o maior crescimento proporcional desde 1970."
        )
    elif crescimento2 > crescimento1:
        st.success(
            f"🏆 {pais2_escolhido} teve o maior crescimento proporcional desde 1970."
        )
    else:
        st.info("⚖️ Os dois países tiveram o mesmo crescimento proporcional.")

# Página 3

elif pagina == "Classificação SVM":

    st.title("🤖 Classificação de Países com SVM")

    st.write(
        "O modelo SVM classifica os países em duas categorias "
        "de densidade populacional: baixa e alta."
    )

    # ==========================================
    # PREPARAÇÃO DOS DADOS
    # ==========================================

    dados_svm = dados.copy()

    # Mediana da densidade populacional
    mediana_densidade = dados_svm[
        "Density (per km²)"
    ].median()

    # Criação das duas classes
    dados_svm["Classe"] = np.where(
        dados_svm["Density (per km²)"] <= mediana_densidade,
        "Baixa",
        "Alta"
    )

    # ==========================================
    # CARACTERÍSTICAS UTILIZADAS PELO SVM
    # ==========================================

    X = dados_svm[
        [
            "Area (km²)",
            "1970 Population",
            "1980 Population",
            "1990 Population",
            "2000 Population",
            "2010 Population",
            "2015 Population",
            "2020 Population"
        ]
    ]

    y = dados_svm["Classe"]

    # ==========================================
    # TREINO E TESTE
    # ==========================================

    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # ==========================================
    # NORMALIZAÇÃO
    # ==========================================

    scaler = StandardScaler()

    X_treino = scaler.fit_transform(X_treino)
    X_teste = scaler.transform(X_teste)

    # ==========================================
    # MODELO SVM
    # ==========================================

    modelo = SVC(
        kernel="linear",
        C=1.0
    )

    modelo.fit(
        X_treino,
        y_treino
    )

    # ==========================================
    # PREVISÃO
    # ==========================================

    previsoes = modelo.predict(
        X_teste
    )

    acuracia = accuracy_score(
        y_teste,
        previsoes
    )

    # ==========================================
    # DESEMPENHO
    # ==========================================

    st.subheader("📊 Desempenho do modelo")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Acurácia",
            f"{acuracia * 100:.1f}%"
        )

    with col2:
        st.metric(
            "Dados de treinamento",
            len(X_treino)
        )

    with col3:
        st.metric(
            "Dados de teste",
            len(X_teste)
        )

    # ==========================================
    # MATRIZ DE CONFUSÃO
    # ==========================================

    st.subheader("🎯 Matriz de Confusão")

    matriz = confusion_matrix(
        y_teste,
        previsoes,
        labels=["Baixa", "Alta"]
    )

    matriz_df = pd.DataFrame(
        matriz,
        index=[
            "Real: Baixa",
            "Real: Alta"
        ],
        columns=[
            "Previsto: Baixa",
            "Previsto: Alta"
        ]
    )

    st.dataframe(
        matriz_df,
        use_container_width=True
    )

    # ==========================================
    # CLASSIFICAÇÃO DE UM PAÍS
    # ==========================================

    st.divider()

    st.subheader("🌎 Classificar um país")

    pais_escolhido = st.selectbox(
        "Selecione um país",
        dados_svm["Country"]
    )

    pais = dados_svm[
        dados_svm["Country"] == pais_escolhido
    ].iloc[0]

    dados_pais = [[
        pais["Area (km²)"],
        pais["1970 Population"],
        pais["1980 Population"],
        pais["1990 Population"],
        pais["2000 Population"],
        pais["2010 Population"],
        pais["2015 Population"],
        pais["2020 Population"]
    ]]

    dados_pais = scaler.transform(
        dados_pais
    )

    classe_prevista = modelo.predict(
        dados_pais
    )[0]

    classe_real = pais["Classe"]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Classe real",
            classe_real
        )

    with col2:
        st.metric(
            "Classe prevista pelo SVM",
            classe_prevista
        )

    if classe_real == classe_prevista:
        st.success(
            "✅ O SVM classificou o país corretamente!"
        )
    else:
        st.warning(
            "⚠️ O SVM classificou o país em uma classe diferente."
        )

    # ==========================================
    # GRÁFICO DE DIVISÃO DAS CLASSES
    # ==========================================

    st.divider()

    st.subheader("📈 Divisão das classes pelo SVM")

    st.write(
        "A linha representa a fronteira de decisão encontrada "
        "pelo SVM para separar os países de baixa e alta densidade."
    )

    # ------------------------------------------
    # DADOS PARA O GRÁFICO
    # ------------------------------------------

    dados_grafico = dados_svm[
        [
            "Country",
            "Area (km²)",
            "2022 Population",
            "Classe"
        ]
    ].copy()

    # Escala logarítmica para reduzir
    # a diferença entre países muito grandes
    dados_grafico["Área Log"] = np.log10(
        dados_grafico["Area (km²)"].clip(lower=1)
    )

    dados_grafico["População Log"] = np.log10(
        dados_grafico["2022 Population"].clip(lower=1)
    )

    # ------------------------------------------
    # REMOÇÃO DOS OUTLIERS
    # ------------------------------------------

    def remover_outliers(df, coluna):

        Q1 = df[coluna].quantile(0.25)
        Q3 = df[coluna].quantile(0.75)

        IQR = Q3 - Q1

        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR

        return df[
            (df[coluna] >= limite_inferior) &
            (df[coluna] <= limite_superior)
        ]

    dados_grafico = remover_outliers(
        dados_grafico,
        "Área Log"
    )

    dados_grafico = remover_outliers(
        dados_grafico,
        "População Log"
    )

    # ------------------------------------------
    # PREPARAÇÃO DO SVM VISUAL
    # ------------------------------------------

    X_visual = dados_grafico[
        [
            "Área Log",
            "População Log"
        ]
    ]

    y_visual = dados_grafico["Classe"]

    scaler_visual = StandardScaler()

    X_visual = scaler_visual.fit_transform(
        X_visual
    )

    # SVM linear para criar uma fronteira simples e visualizável
    modelo_visual = SVC(
        kernel="linear",
        C=1.0
    )

    modelo_visual.fit(
        X_visual,
        y_visual
    )

    # ------------------------------------------
    # FRONTEIRA E MARGENS DO SVM
    # ------------------------------------------

    coeficientes = modelo_visual.coef_[0]
    intercepto = modelo_visual.intercept_[0]

    x_linha = np.linspace(
        X_visual[:, 0].min() - 0.5,
        X_visual[:, 0].max() + 0.5,
        300
    )

    # Fronteira central: decisão = 0
    y_fronteira = (
        -(
            coeficientes[0] * x_linha
            + intercepto
        )
        / coeficientes[1]
    )

    # Margem superior: decisão = +1
    y_margem_superior = (
        -(
            coeficientes[0] * x_linha
            + intercepto
            - 1
        )
        / coeficientes[1]
    )

    # Margem inferior: decisão = -1
    y_margem_inferior = (
        -(
            coeficientes[0] * x_linha
            + intercepto
            + 1
        )
        / coeficientes[1]
    )

    # ------------------------------------------
    # GRÁFICO
    # ------------------------------------------

    fig = go.Figure()

    # Pontos de cada classe
    for classe in ["Baixa", "Alta"]:

        grupo = dados_grafico[
            dados_grafico["Classe"] == classe
        ]

        indices = (
            dados_grafico["Classe"] == classe
        )

        fig.add_trace(
            go.Scatter(
                x=X_visual[indices, 0],
                y=X_visual[indices, 1],
                mode="markers",
                name=classe,
                text=grupo["Country"],
                customdata=np.column_stack([
                    grupo["Area (km²)"],
                    grupo["2022 Population"]
                ]),
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Área: %{customdata[0]:,.0f} km²<br>"
                    "População: %{customdata[1]:,.0f}"
                    "<extra></extra>"
                ),
                marker=dict(
                    size=9,
                    opacity=0.8
                )
            )
        )

    # ------------------------------------------
    # MARGEM INFERIOR
    # ------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=x_linha,
            y=y_margem_inferior,
            mode="lines",
            name="Margem",
            line=dict(
                width=2,
                dash="dash"
            ),
            hoverinfo="skip"
        )
    )

    # ------------------------------------------
    # FRONTEIRA PRINCIPAL
    # ------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=x_linha,
            y=y_fronteira,
            mode="lines",
            name="Fronteira SVM",
            line=dict(
                width=4
            ),
            hoverinfo="skip"
        )
    )

    # ------------------------------------------
    # MARGEM SUPERIOR
    # ------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=x_linha,
            y=y_margem_superior,
            mode="lines",
            name="Margem",
            line=dict(
                width=2,
                dash="dash"
            ),
            hoverinfo="skip",
            showlegend=False
        )
    )

    fig.update_layout(
        title="Separação entre baixa e alta densidade",
        title_x=0.5,
        height=600,
        xaxis_title="Área do país (normalizada)",
        yaxis_title="População em 2022 (normalizada)",
        margin=dict(
            l=20,
            r=20,
            t=70,
            b=20
        ),
        legend_title="Classe"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "Os outliers foram removidos apenas da visualização "
        "para facilitar a interpretação. O modelo principal "
        "continua utilizando a base completa."
    )