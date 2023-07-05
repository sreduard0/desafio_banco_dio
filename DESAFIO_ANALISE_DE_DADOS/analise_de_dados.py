import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo XLSX
df = pd.read_excel('despesas.xlsx')

# Converter a coluna de data para o tipo datetime
df['Data'] = pd.to_datetime(df['Data'])

# Calcular o total gasto por categoria
total_por_categoria = df.groupby('Categoria')['Valor'].sum()
print(total_por_categoria)

# Criar um gráfico de pizza para visualizar o total gasto por categoria
total_por_categoria.plot(kind='pie', title='Total Gasto por Categoria')
plt.show()

# Calcular o total gasto por mês
df['Mes'] = df['Data'].dt.to_period('M')
total_por_mes = df.groupby('Mes')['Valor'].sum()
print(total_por_mes)

# Criar um gráfico de linha para visualizar o total gasto por mês
total_por_mes.plot(kind='line', title='Total Gasto por Mês')
plt.show()
