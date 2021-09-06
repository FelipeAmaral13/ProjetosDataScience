import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import requests
import csv


pd.set_option("display.max_colwidth", 150)
pd.set_option("display.min_rows", 20)


URL_titulos_tesouro = 'https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv'
URL_titulos_vendas = 'https://www.tesourotransparente.gov.br/ckan/dataset/f0468ecc-ae97-4287-89c2-6d8139fb4343/resource/e5f90e3a-8f8d-4895-9c56-4bb2f7877920/download/VendasTesouroDireto.csv'


df_csv = []

def busca_tit_tesouro_direto(url):

    global df_csv

    r = requests.get(URL_titulos_tesouro)

    decoded_content = r.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=';')

    my_list = list(cr)
    for row in my_list:
        df_csv.append(row)

    df_tesouro_direto = pd.DataFrame(df_csv, columns=df_csv[0])
    df_tesouro_direto.drop(index=df_tesouro_direto.index[0], 
                           axis=0, 
                           inplace=True)

    df_tesouro_direto['Data Vencimento'] = pd.to_datetime(df_tesouro_direto['Data Vencimento'], dayfirst=True)
    df_tesouro_direto['Data Base']       = pd.to_datetime(df_tesouro_direto['Data Base'], dayfirst=True)
    multi_indice = pd.MultiIndex.from_frame(df_tesouro_direto.iloc[:, :3])
    df_tesouro_direto = df_tesouro_direto.set_index(multi_indice).iloc[: , 3:]  

    return df_tesouro_direto



df_tesouro_direto = busca_tit_tesouro_direto(URL_titulos_tesouro)


https://github.com/codigoquant/python_para_investimentos/blob/master/20_Tesouro_Direto_com_Python.ipynb