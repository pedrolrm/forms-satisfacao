import streamlit as st

from src.config import BLACK, GREEN, NAVY, PRIMARY_BG, WHITE


def aplicar_estilos():
    st.markdown(
        f"""
        <style>
            :root {{
                --cjr-bg: {PRIMARY_BG};
                --cjr-navy: {NAVY};
                --cjr-green: {GREEN};
                --cjr-black: {BLACK};
                --cjr-white: {WHITE};
            }}

            * {{
                box-sizing: border-box;
            }}

            html,
            body,
            .stApp {{
                overflow-x: hidden;
            }}

            .stApp {{
                background: var(--cjr-bg);
                color: var(--cjr-black);
            }}

            [data-testid="stHeader"] {{
                background: transparent;
                border: 0;
                box-shadow: none;
            }}

            [data-testid="stDecoration"],
            [data-testid="stToolbar"] {{
                display: none;
            }}

            [data-testid="stSidebar"],
            [data-testid="stSidebarCollapsedControl"] {{
                display: none;
            }}

            [data-testid="stAppViewContainer"] > .main .block-container {{
                max-width: 1500px;
                padding-top: 1.4rem;
                padding-bottom: 1.2rem;
            }}

            .cjr-filter-title,
            .cjr-popover-title {{
                color: var(--cjr-navy);
                font-size: 1rem;
                font-weight: 850;
                margin: 0;
            }}

            .cjr-popover-subtitle {{
                color: rgba(21, 21, 21, 0.68);
                font-size: 0.82rem;
                line-height: 1.35;
                margin: 0.2rem 0 0.9rem 0;
            }}

            [data-baseweb="select"] > div,
            [data-baseweb="select"] input {{
                background: var(--cjr-white);
                color: var(--cjr-black);
                border-color: rgba(21, 21, 21, 0.35);
                box-shadow: none;
            }}

            [data-baseweb="select"] > div:hover,
            [data-baseweb="select"] > div:focus-within {{
                border-color: var(--cjr-green);
                box-shadow: 0 0 0 1px var(--cjr-green);
            }}

            [data-baseweb="select"] svg {{
                color: var(--cjr-navy);
            }}

            [data-baseweb="popover"],
            [data-baseweb="menu"] {{
                background: var(--cjr-white);
                color: var(--cjr-black);
            }}

            [role="option"] {{
                color: var(--cjr-black);
                background: var(--cjr-white);
            }}

            [role="option"]:hover,
            [aria-selected="true"][role="option"] {{
                background: rgba(39, 189, 128, 0.14);
                color: var(--cjr-navy);
            }}

            h1, h2, h3 {{
                color: var(--cjr-navy);
                letter-spacing: 0;
            }}

            .cjr-topbar {{
                padding-bottom: 0.75rem;
                border-bottom: 1px solid rgba(0, 24, 48, 0.12);
                margin-bottom: 0.75rem;
            }}

            .cjr-topbar-line {{
                border-bottom: 1px solid rgba(0, 24, 48, 0.12);
                margin: 0.25rem 0 0.75rem 0;
            }}

            .cjr-filter-button button {{
                width: 44px;
                height: 40px;
                padding: 0;
                background: var(--cjr-white);
                border: 1px solid rgba(21, 21, 21, 0.28);
                border-radius: 8px;
                color: var(--cjr-navy);
                font-size: 1.15rem;
                font-weight: 850;
                box-shadow: none;
            }}

            .cjr-filter-button button:hover {{
                border-color: var(--cjr-green);
                color: var(--cjr-navy);
                background: rgba(39, 189, 128, 0.08);
            }}

            .cjr-filter-button button:focus {{
                border-color: var(--cjr-green);
                box-shadow: 0 0 0 1px var(--cjr-green);
            }}

            [data-baseweb="popover"] > div {{
                background: var(--cjr-white);
                border: 1px solid rgba(0, 24, 48, 0.18);
                border-radius: 8px;
                box-shadow: 0 16px 36px rgba(0, 24, 48, 0.16);
                padding: 1rem;
                min-width: 280px;
            }}

            [data-baseweb="popover"] [data-testid="stVerticalBlock"] {{
                gap: 0.45rem;
            }}

            [data-baseweb="popover"] [data-baseweb="select"] {{
                margin-top: -0.15rem;
            }}

            [data-baseweb="popover"] [data-testid="stMarkdownContainer"] p {{
                margin: 0;
            }}

            [data-baseweb="popover"] [data-testid="stWidgetLabel"] p {{
                color: var(--cjr-black);
                font-size: 0.85rem;
                font-weight: 650;
                margin-bottom: 0.25rem;
            }}

            .cjr-eyebrow {{
                color: var(--cjr-green);
                font-weight: 800;
                text-transform: uppercase;
                font-size: 0.78rem;
                margin-bottom: 0.35rem;
            }}

            .cjr-title {{
                color: var(--cjr-navy);
                font-size: 2rem;
                font-weight: 850;
                line-height: 1.08;
                margin: 0;
            }}

            .cjr-subtitle {{
                color: rgba(21, 21, 21, 0.72);
                font-size: 1rem;
                margin-top: 0.55rem;
                max-width: 780px;
            }}

            .cjr-logo-top {{
                justify-self: end;
                width: 86px;
                height: auto;
                margin-top: 0.1rem;
            }}

            div[data-testid="stHorizontalBlock"] {{
                gap: 1rem;
            }}

            div[data-testid="stMetric"] {{
                background: var(--cjr-white);
                border: 1px solid rgba(21, 21, 21, 0.22);
                border-left: 4px solid var(--cjr-green);
                padding: 0.7rem 1rem;
                border-radius: 8px;
            }}

            div[data-testid="stMetricLabel"] p {{
                color: rgba(21, 21, 21, 0.68);
                font-weight: 650;
            }}

            div[data-testid="stMetricValue"] {{
                color: var(--cjr-navy);
            }}

            .stTabs [data-baseweb="tab-list"] {{
                gap: 0.35rem;
                border-bottom: 1px solid rgba(0, 24, 48, 0.12);
                margin-top: 0.75rem;
            }}

            .stTabs [data-baseweb="tab"] {{
                background: transparent;
                border-radius: 8px 8px 0 0;
                padding: 0.65rem 1rem;
                color: var(--cjr-navy);
                border: 1px solid transparent;
            }}

            .stTabs [aria-selected="true"] {{
                background: var(--cjr-navy);
                color: var(--cjr-white);
                border-color: var(--cjr-navy);
                box-shadow: inset 0 -3px 0 var(--cjr-green);
            }}

            .stTabs [data-baseweb="tab-highlight"] {{
                background-color: var(--cjr-green);
            }}

            .stTabs [data-baseweb="tab"] p {{
                color: inherit;
                font-weight: 700;
            }}

            [data-testid="stPlotlyChart"] {{
                background: var(--cjr-white);
                border: 1px solid var(--cjr-black);
                border-radius: 8px;
                overflow: hidden;
                max-width: 100%;
                padding: 0;
            }}

            [data-testid="stPlotlyChart"] > div {{
                max-width: 100%;
                overflow: hidden !important;
            }}

            [data-testid="stPlotlyChart"] .js-plotly-plot,
            [data-testid="stPlotlyChart"] .plot-container,
            [data-testid="stPlotlyChart"] .svg-container {{
                max-width: 100% !important;
                overflow: hidden !important;
            }}

            div[data-testid="stDataFrame"] {{
                border: 1px solid var(--cjr-black);
                border-radius: 8px;
                overflow: hidden;
            }}

            @media (max-width: 900px) {{
                .cjr-logo-top {{
                    justify-self: start;
                    width: 72px;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
