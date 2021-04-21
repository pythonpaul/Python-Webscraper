import bs4
from bs4 import BeautifulSoup    
import re
    def scan_links():

        i = input("Enter search query: ")
        google_search = "https://www.google.com/search?q="+i

        get_links = requests.get(google_search, timeout=5)

        print(get_links)
        soup = BeautifulSoup(get_links.content, 'html.parser')
        a = soup.find_all('div')
        a = str(a)

        x = ""
        y = []
        for l in a:
            if l == " ":  
                y.append(x)
                x = ""
            else:
                x += l 
        print(y)
        txt = ''
        array = []
scan_links()
