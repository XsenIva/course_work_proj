from bs4 import BeautifulSoup
import requests
import time

subDomainsHttp = []
subDomainsHttps = []

responseDomains = {}


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
    # print(f"time scan subdomain %s second " % (time.time() - start_time)) 

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
    

find_subdomain("graphworld.ru", "tiny")
for domain in subDomainsHttp:
    parse_page(domain)

print(responseDomains)




