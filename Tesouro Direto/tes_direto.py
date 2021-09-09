# Import bibliotecas
from datetime import datetime
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import requests
import csv

# Pre-ambulos Pandas -  Mostrar max de caracteres e minimo de linhas
pd.set_option("display.max_colwidth", 150)
pd.set_option("display.min_rows", 20)

# Urls para obter os valores do tesouro direto, vendas e recompras
URL_titulos_tesouro = 'https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv'
URL_titulos_vendas = 'https://www.tesourotransparente.gov.br/ckan/dataset/f0468ecc-ae97-4287-89c2-6d8139fb4343/resource/e5f90e3a-8f8d-4895-9c56-4bb2f7877920/download/VendasTesouroDireto.csv'
URL_titulos_recompra = "https://www.tesourotransparente.gov.br/ckan/dataset/f30db6e4-6123-416c-b094-be8dfc823601/resource/30c2b3f5-6edd-499a-8514-062bfda0f61a/download/RecomprasTesouroDireto.csv"

df_td = [] # Vetor dos titulos do tesouro direto

def busca_tit_tesouro_direto(url):

    global df_td

    # Requisicao da URL
    r = requests.get(url)

    # Deconing para padrao utf-8 (sujeira ao fazer a requisicao)
    decoded_content = r.content.decode('utf-8')
    # Ler o retorno do csv
    cr = csv.reader(decoded_content.splitlines(), delimiter=';')

    # Transformar em lista de listas e concatenar em um vetor
    my_list = list(cr)
    for row in my_list:
        df_td.append(row)

    # Transformar em um dataframe
    df_tesouro_direto = pd.DataFrame(df_td, columns=df_td[0])
    df_tesouro_direto.drop(index=df_tesouro_direto.index[0], 
                           axis=0, 
                           inplace=True)

    # Transformar colunas em datetime
    df_tesouro_direto['Data Vencimento'] = pd.to_datetime(df_tesouro_direto['Data Vencimento'], dayfirst=True)
    df_tesouro_direto['Data Base']       = pd.to_datetime(df_tesouro_direto['Data Base'], dayfirst=True)

    # Organizar o dataframe
    multi_indice = pd.MultiIndex.from_frame(df_tesouro_direto.iloc[:, :3])

    # Setar o index pelos tipos de tesouro direto
    df_tesouro_direto = df_tesouro_direto.set_index(multi_indice).iloc[: , 3:]  

    return df_tesouro_direto


def busca_venda_tesouro(url):

    # Ler o csv capturado
    df  = pd.read_csv(url, sep=';', decimal=',')

    # Transformar colunas em datetime
    df['Vencimento do Titulo'] = pd.to_datetime(df['Vencimento do Titulo'], dayfirst=True)
    df['Data Venda']       = pd.to_datetime(df['Data Venda'], dayfirst=True)

    # Organizar o dataframe
    multi_indice = pd.MultiIndex.from_frame(df.iloc[:, :3])

    # Setar o index pelos tipos de tesouro direto
    df_tesouro_direto_venda = df.set_index(multi_indice).iloc[: , 3:]  

    return df_tesouro_direto_venda

def busca_recompras_tesouro(url):

    df  = pd.read_csv(url, sep=';', decimal=',')
    df['Vencimento do Titulo'] = pd.to_datetime(df['Vencimento do Titulo'], dayfirst=True)
    df['Data Resgate']       = pd.to_datetime(df['Data Resgate'], dayfirst=True)
    multi_indice = pd.MultiIndex.from_frame(df.iloc[:, :3])
    df_tesouro_recompra = df.set_index(multi_indice).iloc[: , 3:]  
    
    return df_tesouro_recompra

# Executars as funcoes para obter os valores dos titulos do tesouro. vendas e recompras
df_tesouro_direto = busca_tit_tesouro_direto(URL_titulos_tesouro)
df_tesouro_direto_venda = busca_venda_tesouro(URL_titulos_vendas)
df_tesouro_recompra = busca_recompras_tesouro(URL_titulos_recompra)

### Analise do dataframe referente o Tesouro Direto ###

def analise_tesouro(dataframe, tesouro, data, graph=False):

    # Organizar dataframe
    dataframe.sort_index(inplace=True)

    # Transformar em lista
    tipos_titulos = dataframe.index.droplevel(level=1).droplevel(level=1).drop_duplicates().to_list()

    # Selecionar o tesouro
    sel_tesouro = dataframe.loc[(tesouro, data)]

    # Formatar coluna para float
    for col in range(len(sel_tesouro.columns)):
        sel_tesouro[sel_tesouro.columns[col]] = sel_tesouro[sel_tesouro.columns[col]].apply(lambda x: float(x.split()[0].replace(',', '.')))
    
    # Plot da colun PU Base Manha
    if graph == True:
        sel_tesouro['PU Base Manha'].plot()
        plt.title('PU Base Manha')
        plt.xlabel('Data')
        plt.ylabel('Valor R$')
        plt.grid()
        plt.show()

    return sel_tesouro

# Tesouros a serem analisados
sel_tesouro_1 = analise_tesouro(df_tesouro_direto, 'Tesouro Selic', '2024-09-01', graph=False)
sel_tesouro_2 = analise_tesouro(df_tesouro_direto, 'Tesouro Prefixado', '2024-07-01')
sel_tesouro_3 = analise_tesouro(df_tesouro_direto, 'Tesouro IPCA+', '2026-08-15')

# Request da tabela de rentabiblidade dos tesouros
url_tabela_rend = 'https://apiapex.tesouro.gov.br/aria/v1/sistd/custom/ultimaRentabilidadeCSV'

# Vetor para concatenar as informacoes raspadas
tab_rend = []

def tabela_rend(url):

    # Request da url
    r = requests.get(url)

    # Deconing para padrao utf-8 (sujeira ao fazer a requisicao)
    decoded_content = r.content.decode('latin1')
    # Ler o retorno do csv
    cr = csv.reader( decoded_content.splitlines(), delimiter=';')

    # Transformar em lista de listas e concatenar em um vetor
    my_list = list(cr)
    for row in my_list:
        tab_rend.append(row)

    # Transformar em um dataframe
    df_tab_tab = pd.DataFrame(tab_rend, columns=tab_rend[0])
    df_tab_tab.drop(index=df_tab_tab.index[0], 
                           axis=0, 
                           inplace=True)

    return df_tab_tab

# Tabela com os rendimentos de cada tesouro
df_tab_tab = tabela_rend(url_tabela_rend)

# Selecionar o tesouro a ser analisado
sel_selic = df_tab_tab[(df_tab_tab['Títulos'] == 'Tesouro Selic') & (df_tab_tab['Vencimento'] == '01/09/2024')]

sel_ipca = df_tab_tab[(df_tab_tab['Títulos'] == 'Tesouro IPCA+') & (df_tab_tab['Vencimento'] == '15/08/2026')]

# Rendimento dos ultimos 30 dias
rend_bruto_30_selic = float(sel_selic['Últ. 30 dias'].str.replace(',', '.'))

rend_bruto_30_ipca = float(sel_ipca['Últ. 30 dias'].str.replace(',', '.'))


# Fazer o equilibrio da carteira

#Valor atual investido
valor_atual_selic = 437.40
valor_atual_ipca = 115.32

# Quantia para investimento
qnt = 150

# Estrategia de investimento
porc_investimento = {'Tesouro_Selic':0.50, 'Tesouro_IPCA': 0.25, 'Tesouro_prefixo': 0.25 }

# Valor que investiria segunda minha estrategia (50%->Selic, 25%->IPCA, 25%->Prefixo)
val_teorico_selic = valor_atual_selic + (qnt*porc_investimento['Tesouro_Selic'])
val_teorico_ipca = valor_atual_ipca + (qnt*porc_investimento['Tesouro_IPCA'])

# Valor do rendimento mensal do Titulo
valor_rend_mensal_selic = valor_atual_selic + (valor_atual_selic * rend_bruto_30_selic/100)
valor_rend_mensal_ipca =  valor_atual_ipca  + (valor_atual_ipca *  rend_bruto_30_ipca/100)













