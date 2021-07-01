
# Biliotecas
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
import time
import os

# Caminho
path_to_file = os.getcwd()

# Numero de paginas para raspagem
num_page = 10

# Site
url = "https://www.tripadvisor.com.br/Restaurant_Review-g303506-d21410749-Reviews-Camarada_Camarao_Rio_Sul_RJ-Rio_de_Janeiro_State_of_Rio_de_Janeiro.html"

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

