import streamlit as st
from tes_direto import busca_tit_tesouro_direto, busca_venda_tesouro, busca_recompras_tesouro, analise_tesouro, tabela_rend
import pandas as pd

import requests
import csv

URL_titulos_tesouro = 'https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv'
URL_titulos_vendas = 'https://www.tesourotransparente.gov.br/ckan/dataset/f0468ecc-ae97-4287-89c2-6d8139fb4343/resource/e5f90e3a-8f8d-4895-9c56-4bb2f7877920/download/VendasTesouroDireto.csv'
URL_titulos_recompra = "https://www.tesourotransparente.gov.br/ckan/dataset/f30db6e4-6123-416c-b094-be8dfc823601/resource/30c2b3f5-6edd-499a-8514-062bfda0f61a/download/RecomprasTesouroDireto.csv"

url_tabela_rend = 'https://apiapex.tesouro.gov.br/aria/v1/sistd/custom/ultimaRentabilidadeCSV'


def main():

    st.title("API - Balanceamento da Carteira do tesouro Direto")
    html_temp = """
    <div style="background-color:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;">
    API - Balanceamento da Carteira do tesouro Direto </h2>
    </div>
    """

    st.markdown(html_temp, unsafe_allow_html=True)

    


    if st.button("Balancear"):

        valor_atual_selic = st.text_input("Digite o valor investido no - Tesouro Direto: ")
        valor_atual_ipca = st.text_input("Digite o valor investido no - Tesouro IPCA+: ")
        valor_atual_prefixado = st.text_input("Digite o valor investido no - Tesouro Prefixado: ")

        quantia_investir = st.text_input("Digite o valor a ser investido: ")


        st.write('Obtendo as Informações.')

if __name__ == '__main__':
    main()