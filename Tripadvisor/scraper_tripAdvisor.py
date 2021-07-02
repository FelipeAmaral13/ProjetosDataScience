
# Biliotecas
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
import time
import os
import re

from leia import SentimentIntensityAnalyzer 


# Caminho
path_to_file = os.getcwd()

# Numero de paginas para raspagem
num_page = 100

# Site
url = "https://www.tripadvisor.com.br/Restaurant_Review-g887228-d3809377-Reviews-Chimarron_Churrascaria-Juiz_de_Fora_State_of_Minas_Gerais.html"

# Robo
driver = webdriver.Chrome()
driver.get(url)

# Cookie
driver.find_element_by_xpath('//*[@id="_evidon-accept-button"]').click()

# Vetor com as informacoes
csvWriter = []

for i in range(0, num_page):
    print(f'Pag: {i+1}')
    
    # Expandir o Review 
    time.sleep(2)
    try:
        driver.find_element_by_xpath("//span[@class='taLnk ulBlueLinks']").click()
    except (WebDriverException, NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException)  as e :
        print('Sem expandir')
    container = driver.find_elements_by_xpath(".//div[@class='review-container']")

    for j in range(len(container)):

        try:
            title = container[j].find_element_by_xpath(".//span[@class='noQuotes']").text
        except (WebDriverException, NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException)  as e :
            title = 'Sem Info'
        try:
            date = container[j].find_element_by_xpath(".//span[contains(@class, 'ratingDate')]").get_attribute("title")
        except (WebDriverException, NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException)  as e :
            date = 'Sem Info'
        try: 
            rating = container[j].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class").split("_")[3]
        except (WebDriverException, NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException)  as e :
            rating = 'Sem Info'
        try:
            review = container[j].find_element_by_xpath(".//p[@class='partial_entry']").text.replace("\n", " ")
        except (WebDriverException, NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException)  as e :
            review = 'Sem Info'

        #print(date, rating, title, review)
        csvWriter.append([date, rating, title, review]) 

    # Proxima pag
    driver.find_element_by_xpath('.//a[@class="nav next ui_button primary"]').click()

driver.close()

df = pd.DataFrame(csvWriter, columns=['DATA', 'RATING', 'TITULO', 'REVIEW'])

### ENCODING
df.to_csv('TripAdvisor.csv', sep=';')

### --------------------------- Analise das datas dos reviews

# Regex para troca de "de" para "/"
df['DATA'] = df['DATA'].apply(lambda x: re.sub(r" de ",'/', x))

# Substiuir nome dos meses por seu respecitvo numero
df['DATA']=df['DATA'].str.replace('janeiro','01',regex=True)
df['DATA']=df['DATA'].str.replace('fevereiro','02',regex=True)
df['DATA']=df['DATA'].str.replace('março','03',regex=True)
df['DATA']=df['DATA'].str.replace('abril','04',regex=True)
df['DATA']=df['DATA'].str.replace('maio','05',regex=True)
df['DATA']=df['DATA'].str.replace('junho','06',regex=True)
df['DATA']=df['DATA'].str.replace('julho','07',regex=True)
df['DATA']=df['DATA'].str.replace('agosto','08',regex=True)
df['DATA']=df['DATA'].str.replace('setembro','09',regex=True)
df['DATA']=df['DATA'].str.replace('outubro','10',regex=True)
df['DATA']=df['DATA'].str.replace('novembro','11',regex=True)
df['DATA']=df['DATA'].str.replace('dezembro','12',regex=True)

# Transformar em tipo datetime
df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%y')

# Colunas de ano, mes, dia e dia da semana
df['ANO'] = df['DATA'].dt.year
df['MES'] = df['DATA'].dt.month
df['DIA'] = df['DATA'].dt.day
df['DIA_SEMANA'] = df['DATA'].dt.day_name()

# 1) Qual dia da semana tem mais reviews?
df['DIA_SEMANA'].value_counts()

# 2) Qual mes tem mais reviews?
df['MES'].value_counts()

## ----------------------------------------------------------------------------

### ---------------------------  Analise do RATING
df['RATING/10'] = df['RATING'].astype('int')
df['RATING/10'] = df['RATING/10']/10

# 3) Qual a media, maior e menor nota?
df['RATING/10'].mean()
min(df['RATING/10'])
max(df['RATING/10'])

# 4) Quais amostras sao nota 1(min)
df[df['RATING/10'] == 1.0]

## ----------------------------------------------------------------------------


### --------------------------- Analises dos RAVIEWS
# Limpando as mensagens
msgm = []
for i in range(len(df)):
    try:
        texto  = df['REVIEW'][i]
        # limpando a conversa
        texto = texto.replace('\t', '')
        texto = texto.replace('\n', '')
        texto = texto.replace('\r', '')
        texto = texto.replace('\xa0', '')

        # Dividindo as linhas dos texto
        texto = texto.split('<\\br>')
        msgm.append(texto)
    except :
        print(i)


# Analise de sentimentos das conversas
s = SentimentIntensityAnalyzer()

for j in range(len(msgm))[:5]:

    # Análise de texto simples
    for i in range(len(msgm[j])):
        print(f'Mensagem: {msgm[j][i]}')
        s.polarity_scores(msgm[j][i])
    print('-----------------------------------------------')

# Coluna de Scores calculados da analise de sentimentos
df['SCORES'] = df['REVIEW'].apply(lambda review: s.polarity_scores(review))
# Coluna do Scores normalizado (-1 a +1)
df['COMPOUND']  = df['SCORES'].apply(lambda score_dict: score_dict['compound'])

# Coluna para a classificacao Pos ou Neg da menssagem
df['COMP_SCORES'] = df['COMPOUND'].apply(lambda c: 'pos' if c >=0 else 'neg')

# CALCULAR A PROPORCAO DE MENSAGENS POS E NEG
df['COMP_SCORES'].value_counts()


# Analise das mensagens negativas e com Rating menor/igual que 4
df[(df['COMP_SCORES'] == 'neg') & (df['RATING/10'] <= 4)]
