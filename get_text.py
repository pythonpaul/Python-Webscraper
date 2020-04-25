import requests
import webbrowser
from bs4 import BeautifulSoup
from lxml import html

site = "https://www.nature.com/articles/d41586-020-00655-8"

response = requests.get(site, timeout=5)

print(response)

soup = BeautifulSoup(response.content, 'html.parser')
#print(soup)

#print(soup.prettify)

p = soup.find_all('p')
#print(p)

for n in p:
    print(''.join(n.find_all(text=True)))


















'''
def scan(x):
    w = " "

    if x == 1:
        w = "bing img"
    q = raw_input(w + " search: ")

    p = {"q": q}

    r = requests.get(sites[x], params=p)

    print("Status:", r.status_code)
    webbrowser.open(r.url)

#query = ''
'''

'''
while(query != 'iie'):
    query = input("Enter keyword: ")

    if query == "b":
        openPage()

    else:
        continue
'''
