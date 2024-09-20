import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime, timedelta

# 1. Conexão com o Banco de Dados
conn = sqlite3.connect('be_boss18k.db')
cursor = conn.cursor()

# 2. Criar Tabela para Vendas
cursor.execute('''
CREATE TABLE IF NOT EXISTS vendas (
    ID INTEGER PRIMARY KEY,
    Produto TEXT,
    Preço REAL,
    Data_Venda TEXT,
    Cliente_ID INTEGER
)
''')

# 3. Gerar Dados Fictícios e Inserir no Banco de Dados
def gerar_dados_ficticios(n):
    produtos = ['Anel', 'Pulseira', 'Colar']
    data_inicio = datetime.now() - timedelta(days=n)
    
    for i in range(n):
        produto = np.random.choice(produtos)
        preco = np.random.uniform(50, 500)
        data_venda = (data_inicio + timedelta(days=i)).strftime('%Y-%m-%d')
        cliente_id = np.random.randint(1, 100)
        
        cursor.execute('''
        INSERT INTO vendas (Produto, Preço, Data_Venda, Cliente_ID)
        VALUES (?, ?, ?, ?)
        ''', (produto, preco, data_venda, cliente_id))
    
    conn.commit()

# Gerar e inserir 1000 registros
gerar_dados_ficticios(1000)

# 4. Consultar Dados
df_vendas = pd.read_sql_query('SELECT * FROM vendas', conn)

# 5. Análise de Vendas
vendas_por_produto = df_vendas.groupby('Produto')['Preço'].sum().reset_index()

# 6. Visualização de Dados
plt.figure(figsize=(10, 6))
plt.bar(vendas_por_produto['Produto'], vendas_por_produto['Preço'], color='skyblue')
plt.title('Total de Vendas por Produto')
plt.xlabel('Produto')
plt.ylabel('Total de Vendas (R$)')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()

# 7. Análise de Satisfação (Simulação)
def gerar_feedback(n):
    feedbacks = []
    for _ in range(n):
        produto = np.random.choice(['Anel', 'Pulseira', 'Colar'])
        satisfacao = np.random.choice(['Satisfeito', 'Neutro', 'Insatisfeito'])
        feedbacks.append((produto, satisfacao))
    return feedbacks

# Gerar e exibir feedback de 50 clientes
feedbacks = gerar_feedback(50)
df_feedback = pd.DataFrame(feedbacks, columns=['Produto', 'Satisfacao'])
print("\nFeedback dos Clientes:")
print(df_feedback.value_counts())

# 8. Fechar Conexão com o Banco de Dados
conn.close()
