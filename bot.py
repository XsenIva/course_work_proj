import telebot
import socket
from bs4 import BeautifulSoup
import requests
import time


token='ee95029cee95029cee95029c3ded81050feee95ee95029c8acadc72e9709a021b0614bf'
version = 5.131
domain = id

bot = telebot.TeleBot('6264746759:AAHPmcfrw5feTau8Y0Ug6d735Qse1fjlg4w')


port_list = []
subDomainsHttp = []
subDomainsHttps = []
responseDomains = {}


@bot.message_handler(commands=['start'])
def main(message):
  bot.send_message(message.chat.id, 'tool - инструмент, который позволяет от исходного домена перемещаться по поддоменам и сканировать порты.')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'команда /scan домен - скнирует порты домена')
    bot.send_message(message.chat.id, 'команда /parse домен - ищет поддомены и подключенный к ним сервисы')


@bot.message_handler()
def scan(message):
    if message.text == '/scan':
      bot.send_message(message.chat.id, 'введите имя домена для /scan')
      bot.register_next_step_handler(message, get_domain_scan)
    else: 
      if message.text == '/parse': 
        bot.send_message(message.chat.id, 'введите имя домена для операции /deep')
        bot.register_next_step_handler(message, get_domain_parse)
      else: bot.send_message(message.chat.id, 'ваш домен НЕ принят')


def get_domain_scan(message):
    ip = socket.gethostbyname(message.text)
    for i in range(80):
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      if client.connect_ex((ip, i)):
         bot.send_message(message.chat.id, "Порт" +" " + str(i)+" " + "закрыт")
      else: 
         bot.send_message(message.chat.id, "Порт" +" " + str(i) +" " + "открыт")


def find_subdomain(domain, mode):
    start_time = time.time()
    file = open(f"wordlists/{mode}.txt", 'r')
    content = file.read()
    output = open(f"{domain}.txt", 'w+')
    subdomains = content.splitlines()
    one_percent = len(subdomains) / 100
    i = 0
    percent_load = 0
    for subdomain in subdomains:
        if i // one_percent > percent_load:
            percent_load = i // one_percent
            # print(f"Already {percent_load}%")

        url_http = f"http://{subdomain}.{domain}"
        url_https = f"https://{subdomain}.{domain}"
        i += 1
        try:
            requests.get(url_http)
            # print(f"Discovered URL: {url_http}")
            subDomainsHttp.append(url_http)
            # output.write(f"{url_http}\n")
            requests.get(url_https)
            # output.write(f"{url_https}\n")
            subDomainsHttps.append(url_https)
            # print(f"Discovered URL: {url_https}")
            
        except requests.ConnectionError:
            pass
    file.close()
    output.close()


def parse_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    wordPress = []
    plugins = []
    themes = []

    #find plugins
    def wpVersion(soup):
        metaData = soup.findAll(['meta'])
        for data in metaData:
            try:
                if "WordPress" in data['content']:
                    wordPress.append(data['content'])
            except Exception:
                pass


    def findPlugins(soup):
        allData = soup.findAll(['link'])
        for data in allData:
            try:
                if "/plugins" in data['href']:
                    plugins.append(data['href'])
            except Exception:
                pass
    def findThemes(soup):
        allData = soup.findAll(['link'])
        for data in allData:
            try:
                if "/themes" in data['href']:
                    themes.append(data['href'])
            except Exception:
                pass
    
    wpVersion(soup)
    findPlugins(soup)
    findThemes(soup)
    responseDomains[domain] = {'wordPress': wordPress, 'plugins':plugins, 'themes': themes}
    

def get_domain_parse(message):
      find_subdomain(message.text, "tiny")
      for domain in subDomainsHttp:
        parse_page(domain)
      for domain in subDomainsHttps:
         parse_page(domain)
      for domain in responseDomains:
        bot.send_message(message.chat.id, f"Домен: {domain} \n {responseDomains[domain]['wordPress']}  \n {responseDomains[domain]['plugins']} \n {responseDomains[domain]['themes']} ")


bot.polling(non_stop = True)
