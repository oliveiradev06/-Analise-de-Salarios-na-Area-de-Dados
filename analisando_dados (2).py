import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display
import sys
import plotly.io as pio

# Detectar ambiente e ajustar renderer do Plotly
try:
    if 'google.colab' in sys.modules:
        pio.renderers.default = "colab"  # Para Google Colab
    else:
        pio.renderers.default = "browser"  # Para VS Code / Jupyter local
except:
    pio.renderers.default = "png"  # Caso não funcione, mostra imagem estática

print(f"Renderer do Plotly: {pio.renderers.default}")

# Carregar os dados
df = pd.read_csv("https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv")

df.head(10)
df.info()
df.describe()

linhas, colunas = df.shape
print("N° de Linhas:", linhas)
print("N° de Colunas:", colunas)

df.rename(columns={
    'work_year': 'ano',
    'experience_level': 'senioridade',
    'employment_type': 'contrato',
    'job_title': 'cargo',
    'salary': 'salario',
    'salary_currency': 'moeda',
    'salary_in_usd': 'usd',
    'employee_residence': 'residencia',
    'remote_ratio': 'remoto',
    'company_location': 'localizacao',
    'company_size': 'tamanho_empresa'
}, inplace=True)

display(df.columns)

df["senioridade"].value_counts()
df['contrato'].value_counts()
df['remoto'].value_counts()
df['tamanho_empresa'].value_counts()

df['senioridade'] = df['senioridade'].replace({
    'SE': 'Sênior',
    'MI': 'Pleno',
    'EN': 'Junior',
    'EX': 'Executivo'
})

display(df['senioridade'].value_counts())

df['contrato'] = df['contrato'].replace({
    'FT': 'Tempo Integral',
    'CT': 'Contrato',
    'PT': 'Tempo Parcial',
    'FL': 'Freelancer'
})

display(df['contrato'].value_counts())

df['tamanho_empresa'] = df['tamanho_empresa'].replace({
    'M': 'Médio',
    'L': 'Grande',
    'S': 'Pequeno'
})

display(df['tamanho_empresa'].value_counts())

df['remoto'] = df['remoto'].replace({
    0: 'Presencial',
    50: 'Híbrido',
    100: 'Remoto'
})

display(df['remoto'].value_counts())

df.describe(include='object')
df.isnull().sum()
df["ano"].unique()
df[df.isnull().any(axis=1)]

import numpy as np

# Exemplos de preenchimento de valores nulos
df_salarios = pd.DataFrame({
    'nome': ['Ana', 'Bruno', 'João', 'Daniel', 'Tiago'],
    'salario': [4000, np.nan, 5000, np.nan, 100000],
})
df_salarios['salario_media'] = df_salarios['salario'].fillna(df_salarios['salario'].mean().round(2))
df_salarios['salario_mediana'] = df_salarios['salario'].fillna(df_salarios['salario'].median())

df_temperaturas = pd.DataFrame({
    'Dia_Semana': ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'],
    'Temperatura': [30, np.nan, np.nan, 28, 27, 20, 25]
})
df_temperaturas['Preechido_ffill'] = df_temperaturas["Temperatura"].ffill()

df_temperaturas = pd.DataFrame({
    'Dia_Semana': ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'],
    'Temperatura': [30, np.nan, np.nan, 28, 27, 20, 25]
})
df_temperaturas['Preechido_ffill'] = df_temperaturas["Temperatura"].bfill()

df_cidades = pd.DataFrame({
    'pessoas': ['Ana', 'Bruno', 'João', 'Daniel', 'Tiago'],
    'cidades': ['São Paulo', np.nan, 'Santa Catarina', 'Curitiba', np.nan]
})
df_cidades['cidade_preenchida'] = df_cidades['cidades'].fillna('Não Informado')

# Remover linhas com nulos
df_limpo = df.dropna()
df_limpo = df_limpo.assign(ano=df_limpo['ano'].astype('int64'))

# Gráficos
df_limpo['senioridade'].value_counts().plot(kind='bar', title='Distribuição de Senioridade')

sns.barplot(data=df_limpo, x='senioridade', y='usd')
plt.figure(figsize=(8,5))
sns.barplot(data=df_limpo, x='senioridade', y='usd')
plt.title('Salário Médio por Senioridade')
plt.xlabel('Senioridade')
plt.ylabel('Salário Médio Anual (USD)')
plt.show()

ordem = df_limpo.groupby('senioridade')['usd'].mean().sort_values(ascending=True).index

plt.figure(figsize=(8,5))
sns.barplot(data=df_limpo, x='senioridade', y='usd', order=ordem)
plt.title('Salário Médio por Senioridade')
plt.xlabel('Senioridade')
plt.ylabel('Salário Médio Anual (USD)')
plt.show()

plt.figure(figsize=(10,5))
sns.histplot(df_limpo['usd'], bins=50, kde=True)
plt.title('Distribuição dos Salários Anuais')
plt.xlabel('Salário em USD')
plt.ylabel('Frequência')
plt.show()

plt.figure(figsize=(8,5))
sns.boxplot(x=df_limpo['usd'])
plt.title('Boxplot dos Salários Anuais')
plt.xlabel('Salário em USD')
plt.show()

ordem_senioridade = ['Junior', 'Pleno', 'Sênior', 'Executivo']

plt.figure(figsize=(8,5))
sns.boxplot(x='senioridade', y='usd', data=df_limpo, order=ordem_senioridade)
plt.title('Boxplot dos Salários Anuais por Senioridade')
plt.xlabel('Senioridade')
plt.ylabel('Salário em USD')
plt.show()

plt.figure(figsize=(8,5))
sns.boxplot(x='senioridade', y='usd', data=df_limpo, order=ordem_senioridade, palette='Set3', hue='senioridade')
plt.title('Boxplot dos Salários Anuais por Senioridade')
plt.xlabel('Senioridade')
plt.ylabel('Salário em USD')
plt.show()

import plotly.express as px

# Salário médio por senioridade
senioridade_medio_salario = df_limpo.groupby('senioridade')['usd'].mean().sort_values(ascending=False).reset_index()
fig = px.bar(senioridade_medio_salario, x='senioridade', y='usd',
             title='Média Salarial por Senioridade',
             labels={'senioridade': 'Senioridade', 'usd': 'Salário Médio Anual (USD)'})
fig.show()

# Proporção dos tipos de trabalho
remoto_contagem = df_limpo['remoto'].value_counts().reset_index()
remoto_contagem.columns = ['tipo_trabalho', 'quantidade']

fig = px.pie(remoto_contagem, names='tipo_trabalho', values='quantidade',
             title='Proporção dos tipos de trabalho')
fig.update_traces(textinfo='percent+label')
fig.show()
