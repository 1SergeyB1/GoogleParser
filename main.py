import urllib
import requests
from bs4 import BeautifulSoup
import re

search_q = '/search?q='
#Ниже вводится запрос для поиска
query = "негры"
query = query.replace(' ', '+')
URL = f"https://google.com{search_q}{query}"

resp = requests.get(URL)
maximum = 0
find_number = re.compile(r'start=\d+')
linkin_re = re.compile(r'/url\?q=\D+')
link_str = ''

while True:
    soup = BeautifulSoup(resp.content, "html.parser")
    links = soup.find_all('a', href=True)
    number = re.findall(find_number, links[-7]['href'])
    if number:
        number = int(number[0].split('=')[1])
    else:
        number = 0
    for link in links:
        if re.findall(linkin_re, link['href']) and (str(link['href']).count('google.com/') == 0) and (str(link['href']).count('/search') == 0):
            link_str = link_str + link['href'] + '\n'
    if number > maximum:
        search_q = links[-7]['href']
        URL = f"https://google.com{search_q}"
        resp = requests.get(URL)
        maximum = number
    else:
        print(soup)
        break

with open('links.txt','w',encoding='utf-8') as file:
    file.write(link_str)