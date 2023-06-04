from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
from bs4 import BeautifulSoup
import requests


map = {}
id = 0

options = webdriver.ChromeOptions()

options.add_argument("user-agent = hello")

driver = webdriver.Chrome(
  executable_path ='/Users/ksushaiva/Documents/Program/deiver_chroom/chromedriver',
  options= options)


try:
  driver.get('https://ip-calculator.ru/siteip/')
  time.sleep(1)


  fin_input = driver.find_element("id", 'site') 

  # fin_input.send_keys("{arg}")
  fin_input.clear()

  fin_input.send_keys("https://www.youtube.com/")

  fin_input.send_keys(Keys.ENTER)

  time.sleep(8)
  f_in = driver.find_element("id", 'myInput') 

# -------------------------------------------
  main_page = driver.page_source
  
  html_text = requests.get(main_page).text

  # используем парсер lxml
  soup = BeautifulSoup(html_text, 'lxml')
  
  ads = soup.find_all('td', class_ = 'table table-hover table-bordered')
  file = open("outs.txt", "w")
  file.write(ads.txt)
  file.close()
  # for i in range(len(ads)):
  #   ad = ads[i]
  #   id +=1
  #   map[id] = {}
  #   ahy = ad.find('td',  class_ = 'table table-hover table-bordered').text
  #   map[id] = ahy
  # print(soup)
  # fin_input.send_keys(Keys.ENTER)
  # fin_input.find_element("id", 'ts_input') 

# except:

finally:
  driver.close()
  # items = soup.find_all('td', class_='table table-hover table-bordered')
  # # print(items)
  # for item in items:
  #   # item = soup.find(class_ = 'result')
  #   # result_list.append(item)
  #    print(item.get_text())
  #    print(item)
  driver.quit()
