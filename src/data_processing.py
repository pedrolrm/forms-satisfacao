import pandas as pd

def limpa_dataframe(df):
    renames = {
            'Carimbo de data/hora': 'data_hora',
            'Endereço de e-mail': 'email',
            'Qual seu nome completo?': 'nome',
            'De 1 a 10, quão satisfeito você está com sua experiência na CJR?': 'nota_satisfacao',
            'De 1 a 10, o quanto você sente que está crescendo profissionalmente?\n': 'nota_crescimento',
            'De 1 a 10, o quão você se sente sobrecarregado? \n': 'nota_sobrecarga',
            'Você se sente motivado nas atividades da EJ?': 'motivado',
            'Você tem participado ativamente dos eventos internos e externos da CJR?': 'participacao_eventos',
            'De 1 a 10, o quão você se sente valorizado na CJR? \n': 'nota_valorizacao',
            'De 1 a 10, o quanto você acredita que sua voz é ouvida? \n': 'nota_voz',
            'De 1 a 10, o quanto você se sente pertencente à CJR?\n': 'nota_pertencimento',
            'Você já pensou em sair da CJR no último mês?': 'pensou_em_sair',
            'De 1 a 10, qual a probabilidade de você sair da CJR nos próximos 3 meses?': 'probabilidade_sair',
            'Você tem alguma sugestão de como o Núcleo ao qual pertence poderia melhorar a sua experiência na CJR?': 'sugestao_nucleo',
            'Você tem alguma sugestão de como a Coordenadoria à qual pertence poderia melhorar a sua experiência na CJR?': 'sugestao_coordenadoria',
            'Você tem alguma sugestão de como a DIREX poderia melhorar a sua experiência na CJR? Pode escrever tudo que vier na cabeça, sem filtros! :)\n': 'sugestao_direx',
            'Qual seu núcleo?': 'nucleo'
        }

    df = df.rename(columns=renames)

    if 'data_hora' in df.columns: # Transformando o tipo do dado pra datetime
        df['data_hora'] = pd.to_datetime(df['data_hora'], format='%d/%m/%Y %H:%M:%S', errors='coerce')

    df['nucleo'] = df['nucleo'].astype(str).str.split(', ') # Separando pessoas que participam de mais de um núcleo
    df = df.explode('nucleo')
    df['nucleo'] = df['nucleo'].str.strip()

    return df


def get_colunas_numericas(df):
    escala = range(1,11)
    colunas_selecionadas = []

    for coluna in df.columns:
        valores_unicos = set(df[coluna].dropna().unique())
        if valores_unicos.issubset(escala):
            colunas_selecionadas.append(coluna)
    
    return colunas_selecionadas


def processa_dados(df_original):
    df = limpa_dataframe(df_original)

    colunas_escala = get_colunas_numericas(df)

    return df, colunas_escala