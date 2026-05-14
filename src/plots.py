import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import sample_colorscale
import streamlit as st


TEMPLATE = "plotly_white"
PAPER_BG = "#FFFFFF"
NAVY = "#001830"
GREEN = "#27BD80"
BLACK = "#151515"
CONTINUOUS_SCALE = [[0, "#F5F5F5"], [0.5, "#27BD80"], [1, "#001830"]]
BAR_SCALE = [[0, "#27BD80"], [0.55, "#001830"], [1, "#151515"]]

LABELS = {
    "nucleo": "Núcleo",
    "nome": "Nome",
    "nota_satisfacao": "Satisfação",
    "nota_crescimento": "Crescimento profissional",
    "nota_sobrecarga": "Sobrecarga",
    "nota_valorizacao": "Valorização",
    "nota_voz": "Voz ouvida",
    "nota_pertencimento": "Pertencimento",
    "probabilidade_sair": "Probabilidade de sair",
    "motivado": "Motivação",
    "participacao_eventos": "Participação em eventos",
    "pensou_em_sair": "Pensou em sair",
    "media": "Média",
    "quantidade": "Quantidade",
    "pergunta": "Pergunta",
    "nota": "Nota",
    "percentual": "Percentual",
}


def _gradiente_cjr(total):
    if total <= 1:
        return [NAVY]

    posicoes = [indice / (total - 1) for indice in range(total)]
    return sample_colorscale(BAR_SCALE, posicoes)


def _render(fig, height=360):
    fig.update_layout(
        template=TEMPLATE,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PAPER_BG,
        font={"color": BLACK, "family": "Arial, sans-serif"},
        title={"font": {"color": NAVY, "size": 16}},
        height=height,
        margin={"l": 18, "r": 18, "t": 54, "b": 18},
        hovermode="closest",
        autosize=False,
    )
    fig.update_xaxes(
        color=BLACK,
        gridcolor="rgba(21, 21, 21, 0.12)",
        linecolor="rgba(21, 21, 21, 0.45)",
        zerolinecolor="rgba(21, 21, 21, 0.35)",
    )
    fig.update_yaxes(
        color=BLACK,
        gridcolor="rgba(21, 21, 21, 0.08)",
        linecolor="rgba(21, 21, 21, 0.45)",
        zerolinecolor="rgba(21, 21, 21, 0.35)",
    )
    st.plotly_chart(
        fig,
        width='stretch',
        config={
            "displayModeBar": False,
            "responsive": False,
        },
    )
    return fig


def _colunas_presentes(df, colunas):
    return [coluna for coluna in colunas if coluna in df.columns]


def _resumir_texto(texto, limite=48):
    texto = str(texto)
    if len(texto) <= limite:
        return texto
    return f"{texto[:limite - 3]}..."


def titulo_coluna(coluna):
    return LABELS.get(coluna, coluna.replace("_", " ").title())


def plot_media(pergunta, df, coluna_nucleo="nucleo"):
    media = df.groupby(coluna_nucleo, as_index=False)[pergunta].mean()
    media = media.sort_values(pergunta)

    fig = px.bar(
        media,
        x=pergunta,
        y=coluna_nucleo,
        orientation="h",
        color=coluna_nucleo,
        color_discrete_sequence=_gradiente_cjr(len(media)),
        title=f"Média por núcleo: {titulo_coluna(pergunta)}",
        labels={
            pergunta: "Média (1 a 10)",
            coluna_nucleo: "Núcleo",
        },
    )
    fig.update_xaxes(range=[0, 10.5])
    fig.update_layout(showlegend=False)
    fig.update_traces(marker_line_color=BLACK, marker_line_width=0.6)

    return _render(fig)


def plot_boxplot(pergunta, df, coluna_nucleo="nucleo", coluna_nome="nome"):
    media = df.groupby(coluna_nucleo)[pergunta].mean().sort_values()
    hover_data = _colunas_presentes(df, [coluna_nome])

    fig = px.box(
        df,
        x=pergunta,
        y=coluna_nucleo,
        orientation="h",
        color=coluna_nucleo,
        color_discrete_sequence=_gradiente_cjr(df[coluna_nucleo].nunique()),
        hover_data=hover_data,
        title=f"Distribuição das respostas: {titulo_coluna(pergunta)}",
        labels={
            pergunta: "Nota (1 a 10)",
            coluna_nucleo: "Núcleo",
            coluna_nome: "Nome",
        },
        category_orders={coluna_nucleo: media.index.tolist()},
        points="outliers",
    )
    fig.update_xaxes(range=[0, 10.5])
    fig.update_layout(showlegend=False)
    fig.update_traces(line={"color": NAVY}, marker={"line": {"color": BLACK, "width": 0.8}})

    return _render(fig)


def plot_heatmap_medias(df, colunas_escala, coluna_nucleo="nucleo"):
    medias = df.groupby(coluna_nucleo)[colunas_escala].mean()
    medias = medias.sort_index()
    medias.columns = [titulo_coluna(coluna) for coluna in medias.columns]

    fig = px.imshow(
        medias,
        color_continuous_scale=CONTINUOUS_SCALE,
        aspect="auto",
        zmin=1,
        zmax=10,
        title="Mapa de calor das médias por núcleo",
        labels={
            "x": "Pergunta",
            "y": "Núcleo",
            "color": "Média",
        },
    )
    fig.update_traces(
        hovertemplate="Núcleo: %{y}<br>Pergunta: %{x}<br>Média: %{z:.2f}<extra></extra>",
        xgap=1,
        ygap=1,
    )

    return _render(fig, height=420)


def plot_ranking_perguntas(df, colunas_escala):
    medias = df[colunas_escala].mean().sort_values().reset_index()
    medias.columns = ["pergunta", "media"]
    medias["pergunta"] = medias["pergunta"].map(titulo_coluna)

    fig = px.bar(
        medias,
        x="media",
        y="pergunta",
        orientation="h",
        color="pergunta",
        color_discrete_sequence=_gradiente_cjr(len(medias)),
        title="Ranking geral das perguntas",
        labels={
            "media": "Média (1 a 10)",
            "pergunta": "Pergunta",
        },
    )
    fig.update_xaxes(range=[0, 10.5])
    fig.update_layout(showlegend=False)
    fig.update_traces(marker_line_color=BLACK, marker_line_width=0.6)

    return _render(fig)


def plot_distribuicao_notas(df, colunas_escala):
    df_longo = df[colunas_escala].melt(var_name="pergunta", value_name="nota")
    df_longo["pergunta"] = df_longo["pergunta"].map(titulo_coluna)

    fig = px.histogram(
        df_longo,
        x="nota",
        color="pergunta",
        barmode="group",
        nbins=10,
        title="Distribuição geral das notas",
        labels={
            "nota": "Nota",
            "count": "Quantidade",
            "pergunta": "Pergunta",
        },
        color_discrete_sequence=_gradiente_cjr(len(colunas_escala)),
    )
    fig.update_xaxes(range=[0.5, 10.5], dtick=1)
    fig.update_yaxes(title="Quantidade")
    fig.update_traces(marker_line_color=BLACK, marker_line_width=0.4)

    return _render(fig)


def plot_radar_nucleo(df, colunas_escala, nucleo, coluna_nucleo="nucleo"):
    df_nucleo = df[df[coluna_nucleo] == nucleo]
    medias = df_nucleo[colunas_escala].mean()

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=medias.values,
            theta=[titulo_coluna(coluna) for coluna in medias.index],
            fill="toself",
            name=nucleo,
            line={"color": GREEN, "width": 3},
            fillcolor="rgba(39, 189, 128, 0.22)",
            hovertemplate="%{theta}<br>Média: %{r:.2f}<extra></extra>",
        )
    )
    fig.update_layout(
        title=f"Perfil do núcleo: {nucleo}",
        polar={
            "bgcolor": PAPER_BG,
            "radialaxis": {
                "visible": True,
                "range": [0, 10],
                "gridcolor": "rgba(21, 21, 21, 0.14)",
                "linecolor": "rgba(21, 21, 21, 0.35)",
            },
            "angularaxis": {
                "gridcolor": "rgba(21, 21, 21, 0.12)",
                "linecolor": "rgba(21, 21, 21, 0.35)",
            }
        },
        showlegend=False,
    )

    return _render(fig, height=420)


def plot_respostas_categoricas(df, coluna):
    contagem = df[coluna].value_counts(dropna=False).reset_index()
    contagem.columns = [coluna, "quantidade"]
    contagem = contagem.sort_values("quantidade", ascending=True)
    contagem["resposta_curta"] = contagem[coluna].map(_resumir_texto)

    fig = px.bar(
        contagem,
        x="quantidade",
        y="resposta_curta",
        orientation="h",
        color="quantidade",
        color_continuous_scale=BAR_SCALE,
        custom_data=[coluna],
        color_discrete_sequence=_gradiente_cjr(contagem[coluna].nunique()),
        title=f"Respostas: {titulo_coluna(coluna)}",
        labels={
            "resposta_curta": "Resposta",
            "quantidade": "Quantidade",
        },
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    fig.update_traces(marker_line_color=BLACK, marker_line_width=0.6)
    fig.update_traces(
        hovertemplate="Resposta: %{customdata[0]}<br>Quantidade: %{x}<extra></extra>"
    )
    fig.update_xaxes(dtick=1)

    altura = min(max(320, 42 * len(contagem) + 120), 620)
    return _render(fig, height=altura)
