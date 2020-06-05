import requests
from bs4 import BeautifulSoup
import re

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
    import os

    file_name = input('Enter a file name to store text data: ')
    file_name = file_name + '.txt'
    file_path = './' + file_name

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


        if not os.path.exists(file_path):
            f = open(file_name, 'w+')
            f.write(txt)
            f.close()
        if os.path.exists(file_path):
            f = open(file_name, 'a+')
            f.write(txt)

scan_links()
