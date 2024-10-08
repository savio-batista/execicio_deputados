# -*- coding: utf-8 -*-
"""Exercicio.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AVtWGs9dBGeoMazBKl5KraIRQZIlgWAe

<img src="https://raw.githubusercontent.com/andre-marcos-perez/ebac-course-utils/main/media/logo/newebac_logo_black_half.png" alt="ebac-logo">

---

# **Módulo** | Análise de Dados: Análise Exploratória de Dados de Logística II
Caderno de **Exercícios**<br>
Professor [André Perez](https://www.linkedin.com/in/andremarcosperez/)

---

# **Tópicos**

<ol type="1">
  <li>Manipulação;</li>
  <li>Visualização;</li>
  <li>Storytelling.</li>
</ol>

---

# **Exercícios**

Este *notebook* deve servir como um guia para **você continuar** a construção da sua própria análise exploratória de dados. Fique a vontate para copiar os códigos da aula mas busque explorar os dados ao máximo. Por fim, publique seu *notebook* no [Kaggle](https://www.kaggle.com/).

---

# **Análise Exploratória de Do Comprometimento de Deputados**

## 1\. Contexto

Analisando os dados refentes a avaliações do deputados brasileiros eleitos em 2022, é possível responder as seguintes perguntas:

*   Que partido possui mais deputados produtivos?
*   Que partido possui mais deputados que fiscalizam o executivo?
*   Que partido possui mais deputados capazes de cooperar?
*   Que partido possui melhor alinhamento?
*   Que eixo político possui deputados mais comprometidos com o dever?

## 2\. Pacotes e bibliotecas
"""

# -- Importa Bibliotecas Pertinentes
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sklearn

"""## 3\. Exploração de dados"""

# Defina o diretório onde o arquivo kaggle.json está localizado
os.environ['KAGGLE_CONFIG_DIR'] = os.path.expanduser('~/.kaggle')

# Baixe o dataset
os.system('kaggle datasets download -d nabuchadresar/notas-deputados-brasil-2022')

# Extraia o arquivo baixado
os.system('unzip notas-deputados-brasil-2022.zip')

# Carregue o CSV em um DataFrame do pandas
df = pd.read_csv('rank_legislabr_completo.csv')

"""## 4\. Manipulação"""

#Função para calcular as médias dos indicadores
def calcular_medias(df):
    return [
        df['Produtividade'].mean(),
        df['Fiscalização'].mean(),
        df['Cooperação'].mean(),
        df['Alinhamento'].mean()
    ]


def calcular_percentual(df, coluna, x, condicao='abaixo'):
    """
    Calcula a porcentagem dos valores de uma coluna que estão abaixo ou acima de um valor x.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    coluna (str): Nome da coluna a ser analisada.
    x (float): Valor de referência.
    condicao (str): 'abaixo' para valores abaixo de x, 'acima' para valores acima de x.

    Retorna:
    float: Porcentagem dos valores abaixo ou acima de x.
    """
    if condicao == 'abaixo':
        valores_filtrados = df[df[coluna] < x]
    elif condicao == 'acima':
        valores_filtrados = df[df[coluna] > x]
    else:
        raise ValueError("Condição deve ser 'abaixo' ou 'acima'")

    percentual = (len(valores_filtrados) / len(df)) * 100
    return round(percentual, 2)

"""O rank_legislabr_completo.csv contém as features:

nome: nome do deputado;

estado: o estado do deputado;

partido: partido do deputado;

As seguintes features são do site https://indice.legislabrasil.org/public/.
n_prod_leg: Mede o trabalho efetuado pelo parlamentar na elaboração, análise e votação de instrumentos legislativos;

n_fisc: Mede a fiscalização que o deputado concretiza em relação ao Executivo Federal;

n_mobi: Mede a capacidade do parlamentar de articulação e cooperação com outros agentes políticos;

n_alin_partd: Alinhamento partidário do parlamentar em relação à votação da maioria do seu partido.
"""

# Carregue o CSV em um DataFrame do pandas
dt_notas = pd.read_csv('rank_legislabr_completo.csv')

'''
Para facilitar o entendimento, leia que:
n_prod_leg: Mede o trabalho efetuado pelo parlamentar na elaboração, análise e votação de instrumentos legislativos = PRODUTIVIDADE

n_fisc: Mede a fiscalização que o deputado concretiza em relação ao Executivo Federal = FISCALIZAÇÃO

n_mobi: Mede a capacidade do parlamentar de articulação e cooperação com outros agentes políticos = COOPERAÇÃO

n_alin_partd: Alinhamento partidário do parlamentar em relação à votação da maioria do seu partido = ALINHAMENTO
'''

# Para melhor entendimento, fica mais claro se renomearmos as colunas
dt_notas = dt_notas.rename(columns={'n_prod_leg': 'Produtividade', 'n_fisc': 'Fiscalização', 'n_mobi': 'Cooperação', 'n_alin_partd': 'Alinhamento'})

# Remover colunas que não nos interessam
dt_notas = dt_notas.drop(columns=['Unnamed: 0','nome','estado'])
dt_original = dt_notas

# Exibe as primeiras linhas do datatable
print(dt_notas.head())

dt_notas.info() #nota-se que não há dados nulos no arquivo

"""## 5\. Visualização

É importante observar a quantidade de deputados por partido

Em 2022 o então presidente era Jair Bolsonaro (PL), o qual não foi reeleito.
"""

# -- Primeiro, um levantamento da quantidade de deputados por partido
dt_quantidade = dt_notas['partido'].value_counts()

plt.figure(figsize=(10, 6))
sns.barplot(x=dt_quantidade.index, y=dt_quantidade.values)
plt.title('Quantidade por Partido')
plt.xlabel('Partido')
plt.ylabel('Quantidade')
plt.xticks(rotation=90)  # Rotaciona os rótulos do eixo x se necessário
plt.show()

"""É evidente que o Partido Liberal (PL) possui a maioria dos deputados, seguido por partidos de Centro, vulgo Direita (União Brasil e PP) e em terceiro o Partido dos Trabalhadores (PT)

Vejamos como a média dos principais partidos se relaciona
"""

# Filtrando os dados para os partidos PL, UNIÃO, PSOL e PT
# Para o estudo de caso, escolheu-se 4 partidos:
#dois de direita (PL e UNIÃO BRASIL) e dois sociais democratas (PT e PSOL)
df_PL = dt_notas.loc[dt_notas['partido'] == 'PL']
df_UNIAO = dt_notas.loc[dt_notas['partido'] == 'UNIÃO']
df_PSOL = dt_notas.loc[dt_notas['partido'] == 'PSOL']
df_PT = dt_notas.loc[dt_notas['partido'] == 'PT']

# Calculando as médias para PL e PT
medias_PL = calcular_medias(df_PL)
medias_UNIAO = calcular_medias(df_UNIAO)
medias_PSOL = calcular_medias(df_PSOL)
medias_PT = calcular_medias(df_PT)

# -- Para melhor visualização, utilizaremos um gráfico de barra com as médias

# Definindo os rótulos das barras e a posição das barras
labels = ['Produtividade', 'Fiscalização', 'Cooperação', 'Alinhamento']
x = np.arange(len(labels))
width = 0.1  # Largura das barras

# Criando o gráfico de barras
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width/2, medias_PL, width, label='PL', color='blue')
ax.bar(x + width/2, medias_UNIAO, width, label='UNIÃO', color='green')
ax.bar(x + width*1.5, medias_PSOL, width, label='PSOL', color='orange')
ax.bar(x + width*2.5, medias_PT, width, label='PT', color='red')


# Adicionando títulos e rótulos
ax.set_xlabel('Variáveis')
ax.set_ylabel('Média')
ax.set_title('Médias das Variáveis por Partido')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

# Exibindo o gráfico
plt.show()

"""Para uma visualização mais aprofundada além das médias, utilizaremos o pairplot"""

df_analise = dt_notas.loc[dt_notas['partido'].isin(['PL', 'PT', 'UNIÃO', 'PSOL'])]

# Dicionário de cores
cores_partidos = {
    'PL': 'blue',
    'UNIÃO': 'green',
    'PT': 'red',
    'PSOL': 'yellow'
}

with sns.axes_style('whitegrid'):

  grafico = sns.pairplot(data=df_analise, hue="partido", palette = cores_partidos)

"""É evidente que deputados do PL e UNIÃO se agrupam nos setores localizado à esquerda e para baixo dos gráficos (baixo desempenho) enquanto deputados do PT e PSOL se localizam à direita e para cima dos gráficos (bom desempenho), sendo a única excessão o indicador de Alinhamento.

Para reforçar o parágrafo anterior, vamos analisar um desempenho medido em porcentagem de cada indicador.
"""

'''
n_prod_leg ou PRODUTIVIDADE, n_fisc Mede ou FISCALIZAÇÃO, n_mobi ou COOPERAÇÃO e n_alin_partd ou ALINHAMENTO
todos variam de 0 a 10, vejamos a porcentagem de deputados que estão abaixo de 3 pontos em cada um dos partidos da análise
'''

# -- 1º parâmetro: PRODUTIVIDADE

list_colunas = ('Produtividade', 'Fiscalização', 'Cooperação', 'Alinhamento')
list_partidos = ('PL', 'UNIÃO', 'PT', 'PSOL')
df_indicadores = pd.DataFrame()

for  coluna in list_colunas:
  for partido in list_partidos:

    if partido == 'PL':
      df = df_PL
    elif partido == 'UNIÃO':
      df = df_UNIAO
    elif partido == 'PT':
      df = df_PT
    elif partido == 'PSOL':
      df = df_PSOL

    valor = 3
    posicao = 'abaixo'
    produtividade_abaixo = calcular_percentual(df, coluna, valor, posicao)

    # o valor tido como aceitável varia de acordo com o indicador
    if coluna == 'Produtividade':
      valor = 6
    elif coluna == 'Fiscalização':
      valor = 3
    else:
      valor = 7

    posicao = 'acima'
    produtividade_acima = calcular_percentual(df, coluna, valor, posicao)
    mediano = 100 - produtividade_acima - produtividade_abaixo
    # Adiciona informações ao DataFrame
    nova_linha = pd.DataFrame({
            'Partido': [partido],
            'Indicador': [coluna],
            'Péssimo(%)': [produtividade_abaixo],
            'Mediano(%)': [mediano],
            'Ótimo(%)': [produtividade_acima]

        })
    df_indicadores = pd.concat([df_indicadores, nova_linha], ignore_index=True)

print(df_indicadores)

"""CONCLUSÃO


PRODUTIVIDADE: O PSOL é o partido com mais deputados produtivos (33,33%) enquanto o UNIÃO BRASIL é o partido com menos deputados produtivos (43,33%)

FISCALIZAÇÃO: O PSOL é o partido com deputados que mais fiscalizam (55,56%) enquanto o PL é o partido que menos realiza esse trabalho (98,75%)

COOPERAÇÃO: Os deputados do PT cooperam mais com os demais partidos (10,53%) enquanto os deputados do UNIÃO cooperam menos (56,67%)

ALINHAMENTO: Referente ao alinhameto dos deputados com o interesse do partido, o PSOL possui o maior alinhamento (100%) enquanto o UNIÃO possui o menor (16,67%)

Nota-se que os partidos de viés social democrata (PSOL e PT) possuem indicadores melhores que os partidos com deputados de direita e extrema direita (UNIÃO BRASIL e PL)

PREDIÇÃO

---

Aplicando os conceitos vistos no curso
"""

# Criação de um modelo
from sklearn.cluster import KMeans

# Remove
dt_predicao = dt_notas.drop(['partido'], axis=1)
print(dt_original.head())

model = KMeans()

wcss = []

# Determinação número de clusters
for k in range(1, 11):

  model = KMeans(n_clusters=k)
  model = model.fit(dt_predicao)
  wcss.append(model.inertia_)

with sns.axes_style('whitegrid'):

  grafico = sns.lineplot(x=range(1, 11), y=wcss, marker="8", palette="pastel")
  grafico.set(title='Método do Cotovelo', ylabel='WCSS', xlabel='Qtd. clusters');

#O número ideal de clusters é 4

model = KMeans(n_clusters=4)
model = model.fit(dt_predicao)

clusters = model.labels_
clustered_data = pd.concat([dt_predicao, pd.DataFrame(clusters, columns=['cluster'])], axis=1)

with sns.axes_style('whitegrid'):

  grafico = sns.pairplot(data=clustered_data, hue='cluster', palette="pastel")

#Predição

data = np.array([[8.7, 5.0, 4.9, 9.1]])

df = pd.DataFrame(data, columns=['Produtividade','Fiscalização','Cooperação','Alinhamento'])

cluster = model.predict(data.reshape(1, -1))
print(cluster)