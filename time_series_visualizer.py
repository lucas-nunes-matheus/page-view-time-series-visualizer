import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Importar dados
df = pd.read_csv("fcc-forum-pageviews.csv", index_col='date', parse_dates=True)

# Limpar dados: filtrar os 2,5% superiores e inferiores do conjunto de dados
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]

# Função para gráfico de linha
def draw_line_plot():
    # Criar um gráfico de linha
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df['value'], color='tab:red', linewidth=1)

    # Definir título e rótulos
    ax.set_title('Visualizações Diárias do Fórum freeCodeCamp 5/2016-12/2019')
    ax.set_xlabel('Data')
    ax.set_ylabel('Visualizações')

    # Salvar imagem e retornar fig
    fig.savefig('line_plot.png')
    return fig

# Função para gráfico de barras
def draw_bar_plot():
    # Copiar e modificar dados para o gráfico de barras mensais
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Desenhar gráfico de barras
    fig = df_bar.plot(kind='bar', figsize=(10, 6), legend=True).figure
    plt.title('Média Mensal de Visualizações')
    plt.xlabel('Anos')
    plt.ylabel('Média de Visualizações')

    # Ajustar legenda
    plt.legend(title='Meses', labels=['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])

    # Salvar imagem e retornar fig
    fig.savefig('bar_plot.png')
    return fig

# Função para gráfico de caixa
def draw_box_plot():
    # Preparar dados para gráficos de caixa
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Criar a figura e dois subgráficos (Gráfico de caixa por ano e por mês)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharey=True)

    # Gráfico de caixa por ano
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Gráfico de Caixa por Ano (Tendência)')
    axes[0].set_xlabel('Ano')
    axes[0].set_ylabel('Visualizações')

    # Gráfico de caixa por mês
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axes[1].set_title('Gráfico de Caixa por Mês (Sazonalidade)')
    axes[1].set_xlabel('Mês')
    axes[1].set_ylabel('Visualizações')

    # Salvar imagem e retornar fig
    fig.savefig('box_plot.png')
    return fig
