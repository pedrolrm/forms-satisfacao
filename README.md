# Dashboard de Satisfação CJR

Dashboard em Streamlit para análise das respostas do formulário de satisfação da CJR. O projeto lê dados de uma planilha Google Sheets, trata as respostas com pandas e apresenta visualizações interativas com Plotly.

## Funcionalidades

- Filtro por núcleo.
- Métricas gerais de satisfação, sobrecarga e risco de saída.
- Ranking das perguntas numéricas.
- Distribuição geral das notas.
- Comparativo entre núcleos por mapa de calor.
- Análise detalhada por pergunta com média e boxplot.
- Radar de perfil por núcleo.
- Visualização de respostas categóricas.
- Aba para respostas textuais identificadas pelo nome do membro.

## Tecnologias

- Python
- Streamlit
- pandas
- Plotly
- st-gsheets-connection

## Estrutura do Projeto

```text
.
├── app.py
├── requirements.txt
├── README.md
├── assets/
│   └── cjr_logo.png
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml
└── src/
    ├── config.py
    ├── data_processing.py
    ├── data_source.py
    ├── plots.py
    ├── styles.py
    └── ui.py
```

## Módulos

- `app.py`: orquestra o fluxo principal do dashboard.
- `src/data_source.py`: faz a conexão e leitura dos dados do Google Sheets.
- `src/data_processing.py`: limpa e transforma o dataframe original.
- `src/plots.py`: concentra as visualizações em Plotly.
- `src/styles.py`: concentra o CSS e a identidade visual do Streamlit.
- `src/ui.py`: concentra componentes de interface, como cabeçalho, métricas e tabelas textuais.
- `src/config.py`: centraliza caminhos, cores e configurações globais.

## Instalação

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração do Google Sheets

O app usa `st-gsheets-connection`, então é necessário configurar o arquivo `.streamlit/secrets.toml` com as credenciais e parâmetros da conexão.

Esse arquivo não deve ser versionado. Ele já está listado no `.gitignore`.

Exemplo geral de estrutura:

```toml
[connections.gsheets]
spreadsheet = "URL_DA_PLANILHA"
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "..."
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

A planilha precisa conter as colunas originais do formulário. O tratamento e renomeação das colunas estão definidos em `src/data_processing.py`.

## Execução

Execute o dashboard com:

```bash
streamlit run app.py
```

Por padrão, o Streamlit abrirá em:

```text
http://localhost:8501
```

## Dados Esperados

O formulário deve conter campos como:

- data e hora da resposta;
- e-mail;
- nome completo;
- núcleo;
- notas de 1 a 10 para satisfação, crescimento, sobrecarga, valorização, voz, pertencimento e probabilidade de saída;
- respostas categóricas sobre motivação, participação em eventos e intenção de saída;
- sugestões textuais para núcleo, coordenadoria e DIREX.

As colunas de escala são detectadas automaticamente quando seus valores pertencem ao intervalo de 1 a 10.

## Identidade Visual

A interface segue a paleta visual da CJR:

- fundo principal: `#F5F5F5`;
- azul: `#001830`;
- verde: `#27BD80`;
- preto auxiliar: `#151515`;
- branco para cards e gráficos: `#FFFFFF`.

A logo utilizada pelo app fica em:

```text
assets/cjr_logo.png
```

## Observações

- Arquivos locais de dados, como `.csv` e `.xlsx`, são ignorados pelo Git.
- O dashboard foi organizado para facilitar manutenção futura: dados, gráficos, estilo e componentes visuais ficam em módulos separados.
- Ao alterar `.streamlit/config.toml`, reinicie o Streamlit para garantir que o tema seja reaplicado corretamente.
