# Projeto - Balancear carteira de investimentos do Tesouro Direto

O objetivo desse projeto é realizar o balaceamento da carteira de investimento do Tesouro Direto. 
É feita uma raspagem de dados colentando dos titulos do Tesouro direto, as vendas ocorridas e a recompras realizadas, todas essas informações obtidas pelo site:
![https://www.tesourotransparente.gov.br](https://www.tesourotransparente.gov.br)


### Gráfico de Vendas dos Preços Unitários dos Títulos

![Tesouro Selic](https://user-images.githubusercontent.com/5797933/133174860-9ba84eb6-f53b-4377-b8c3-6be4b9357819.png)
![Tesouro prefixado](https://user-images.githubusercontent.com/5797933/133174864-4fe5d5d0-76d5-4183-af2f-7d685adeebe9.png)
![Tesouro IPCA](https://user-images.githubusercontent.com/5797933/133174865-10b28072-11e6-46ef-b3db-4e634c430372.png)

### Função balancear_carteira

A função balancear_carteira é responsável pelo cálculo do balanceamento da carteira de acordo com a estratégia adotada.

`balancear_carteira(valor_selic, valor_ipca, valor_prefixado, qntia_investir)`
