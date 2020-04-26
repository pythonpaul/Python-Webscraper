import requests
import webbrowser
from bs4 import BeautifulSoup
from lxml import html

def scan_links():

    i = input("Enter search query: ")
    google_search = "https://www.google.com/search?q="+i

    get_links = requests.get(google_search, timeout=5)

    print(get_links)

    soup = BeautifulSoup(get_links.content, 'html.parser')
    #print(soup)

    #print(soup.prettify)

    a = soup.find_all('a')
    print(a)

    txt = ''
    array = []

    for n in a:
        #print(''.join(n.find_all(text=True)))
        array.append(str(''.join(n.find_all(text=True))))

    for x in range(len(array)-1):
        txt += array[x]+'\n'
    print(txt)

    site_array = []

    import re

    for i in range(0, len(array)):
        curr = array[i]
        if "http" in curr:
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', curr)
            print(url[0])
            site_array.append(url[0])
    scan_site(site_array)

def scan_site(x):
    print("site_array: ")
    print(x)
    for i in x:

        print("type of url array: " + str(type(x)))
        site = requests.get(i, timeout=5)
        site_soup = BeautifulSoup(site.content, 'html.parser')

        p = site_soup.find_all('p')
        #print(p)

        txt = ''
        txt_array = []

        for n in p:
            #print(''.join(n.find_all(text=True)))
            txt_array.append(str(''.join(n.find_all(text=True))))

        for x in range(len(txt_array)-1):
            txt += txt_array[x]+'\n'
        #print(txt)

        import sys
        import os

        file_path = './text_data.txt'

        if not os.path.exists(file_path):
            f = open('text_data.txt', 'w+')
            f.write(txt)
            f.close()
        if os.path.exists(file_path):
            f = open('text_data.txt', 'a+')
            f.write(txt)

scan_links()














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
