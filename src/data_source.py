import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection


@st.cache_data(ttl="10m")
def carregar_dados():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_original = conn.read()
        return df_original
    except Exception as erro:
        st.error(f"Erro ao conectar com o Google Sheets: {erro}")
        return pd.DataFrame()
