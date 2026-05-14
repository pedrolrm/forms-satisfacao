import streamlit as st

from src.config import PAGE_TITLE
from src.data_processing import processa_dados
from src.data_source import carregar_dados
from src.plots import (
    plot_boxplot,
    plot_distribuicao_notas,
    plot_heatmap_medias,
    plot_media,
    plot_radar_nucleo,
    plot_ranking_perguntas,
    plot_respostas_categoricas,
    titulo_coluna,
)
from src.styles import aplicar_estilos
from src.ui import (
    renderizar_cabecalho_texto,
    renderizar_filtro_nucleo,
    renderizar_logo_topo,
    renderizar_metricas_principais,
    renderizar_respostas_textuais,
)


st.set_page_config(
    page_title=PAGE_TITLE,
    layout="wide",
    initial_sidebar_state="collapsed",
)

aplicar_estilos()

with st.spinner("Carregando dados..."):
    df_raw = carregar_dados()

if df_raw.empty:
    st.warning("Nenhum dado encontrado na planilha ou erro de conexão.")
    st.stop()

df, colunas_escala = processa_dados(df_raw)
colunas_categoricas = [
    coluna
    for coluna in ["motivado", "participacao_eventos", "pensou_em_sair"]
    if coluna in df.columns
]

nucleos_disponiveis = ["Todos"] + sorted(df["nucleo"].dropna().unique().tolist())

if "nucleo_selecionado" not in st.session_state:
    st.session_state.nucleo_selecionado = "Todos"

if st.session_state.nucleo_selecionado not in nucleos_disponiveis:
    st.session_state.nucleo_selecionado = "Todos"

botao, titulo, logo = st.columns([0.045, 0.855, 0.10], vertical_alignment="top")
with botao:
    st.markdown('<div class="cjr-filter-button">', unsafe_allow_html=True)
    with st.popover("≡", help="Abrir filtros"):
        renderizar_filtro_nucleo(nucleos_disponiveis)
    st.markdown("</div>", unsafe_allow_html=True)
with titulo:
    renderizar_cabecalho_texto()
with logo:
    renderizar_logo_topo()

st.markdown('<div class="cjr-topbar-line"></div>', unsafe_allow_html=True)

nucleo_selecionado = st.session_state.nucleo_selecionado

df_filtrado = df if nucleo_selecionado == "Todos" else df[df["nucleo"] == nucleo_selecionado]

with st.container():
    renderizar_metricas_principais(df_filtrado, colunas_escala)

    tab_geral, tab_pergunta, tab_nucleo, tab_categoricas, tab_textuais = st.tabs(
        [
            "Visão geral",
            "Análise por pergunta",
            "Perfil por núcleo",
            "Respostas categóricas",
            "Respostas textuais",
        ]
    )

    with tab_geral:
        esquerda, direita = st.columns([1, 1])
        with esquerda:
            plot_ranking_perguntas(df_filtrado, colunas_escala)
        with direita:
            plot_distribuicao_notas(df_filtrado, colunas_escala)

        if nucleo_selecionado == "Todos":
            plot_heatmap_medias(df, colunas_escala)
        else:
            st.info("Selecione “Todos” no filtro de núcleo para comparar os núcleos no mapa de calor.")

    with tab_pergunta:
        pergunta_selecionada = st.selectbox(
            "Indicador",
            colunas_escala,
            format_func=titulo_coluna,
        )

        esquerda, direita = st.columns([1, 1])
        with esquerda:
            plot_media(pergunta_selecionada, df_filtrado)
        with direita:
            plot_boxplot(pergunta_selecionada, df_filtrado)

    with tab_nucleo:
        nucleos_radar = sorted(df["nucleo"].dropna().unique().tolist())
        nucleo_radar = (
            st.selectbox("Núcleo para análise", nucleos_radar)
            if nucleo_selecionado == "Todos"
            else nucleo_selecionado
        )

        plot_radar_nucleo(df, colunas_escala, nucleo_radar)

    with tab_categoricas:
        if not colunas_categoricas:
            st.warning("Nenhuma coluna categórica foi encontrada no dataset processado.")
        else:
            pergunta_cat = st.selectbox(
                "Pergunta categórica",
                colunas_categoricas,
                format_func=titulo_coluna,
            )

            esquerda, direita = st.columns([2, 1])
            with esquerda:
                plot_respostas_categoricas(df_filtrado, pergunta_cat)
            with direita:
                contagem = df_filtrado[pergunta_cat].value_counts(dropna=False).reset_index()
                contagem.columns = ["Resposta", "Quantidade"]
                contagem = contagem.sort_values("Quantidade", ascending=False)
                st.dataframe(
                    contagem,
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "Resposta": st.column_config.TextColumn("Resposta", width="large"),
                        "Quantidade": st.column_config.NumberColumn("Quantidade", width="small"),
                    },
                )

    with tab_textuais:
        renderizar_respostas_textuais(df_filtrado)
