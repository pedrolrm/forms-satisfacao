import base64

import pandas as pd
import streamlit as st

from src.config import LOGO_PATH


def formatar_numero(valor):
    if pd.isna(valor):
        return "-"
    return f"{valor:.2f}".replace(".", ",")


def _logo_data_uri():
    if not LOGO_PATH.exists():
        return None

    encoded = base64.b64encode(LOGO_PATH.read_bytes()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def renderizar_cabecalho_texto():
    st.markdown(
        """
        <div>
            <div class="cjr-eyebrow">Dashboard CJR | Forms de Satisfação</div>
            <h1 class="cjr-title">Dashboard de Satisfação dos Membros</h1>
            <div class="cjr-subtitle">
                Uma visão gerada a partir dos dados coletados no formulário de satisfação de membro
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def renderizar_logo_topo():
    logo_uri = _logo_data_uri()
    if not logo_uri:
        return

    st.markdown(
        f'<img class="cjr-logo-top" src="{logo_uri}" alt="CJR">',
        unsafe_allow_html=True,
    )


def renderizar_filtro_nucleo(nucleos_disponiveis):
    st.markdown(
        """
        <div class="cjr-popover-title">Filtros</div>
        <div class="cjr-popover-subtitle">Recorte os dados por núcleo.</div>
        """,
        unsafe_allow_html=True,
    )
    return st.selectbox("Núcleo", nucleos_disponiveis, key="nucleo_selecionado")


def renderizar_metricas_principais(df_filtrado, colunas_escala):
    media_geral = df_filtrado[colunas_escala].mean().mean()
    media_satisfacao = df_filtrado["nota_satisfacao"].mean() if "nota_satisfacao" in df_filtrado else None
    media_sobrecarga = df_filtrado["nota_sobrecarga"].mean() if "nota_sobrecarga" in df_filtrado else None
    risco_saida = df_filtrado["probabilidade_sair"].mean() if "probabilidade_sair" in df_filtrado else None

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Média geral", formatar_numero(media_geral))
    col2.metric("Satisfação", formatar_numero(media_satisfacao))
    col3.metric("Sobrecarga", formatar_numero(media_sobrecarga))
    col4.metric("Risco de saída", formatar_numero(risco_saida))


def renderizar_respostas_textuais(df_filtrado):
    colunas_textuais = {
        "sugestao_nucleo": "Sugestões para o núcleo",
        "sugestao_coordenadoria": "Sugestões para a coordenadoria",
        "sugestao_direx": "Sugestões para a DIREX",
    }
    colunas_disponiveis = [
        coluna for coluna in colunas_textuais if coluna in df_filtrado.columns
    ]

    if not colunas_disponiveis:
        st.warning("Nenhuma coluna de resposta textual foi encontrada no dataset processado.")
        return

    coluna_texto = st.selectbox(
        "Tipo de resposta",
        colunas_disponiveis,
        format_func=colunas_textuais.get,
    )

    respostas = df_filtrado[["nome", coluna_texto]].copy()
    respostas[coluna_texto] = respostas[coluna_texto].fillna("").astype(str).str.strip()
    respostas = respostas[respostas[coluna_texto] != ""]
    respostas = respostas.drop_duplicates().sort_values("nome")

    if respostas.empty:
        st.info("Não há respostas textuais para o recorte selecionado.")
        return

    respostas = respostas.rename(
        columns={
            "nome": "Membro",
            coluna_texto: "Resposta",
        }
    )

    st.dataframe(
        respostas,
        hide_index=True,
        width='stretch',
        column_config={
            "Membro": st.column_config.TextColumn("Membro", width="medium"),
            "Resposta": st.column_config.TextColumn("Resposta", width="large"),
        },
    )
