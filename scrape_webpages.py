import bs4
from bs4 import BeautifulSoup    
import requests

def scan_links():
 
  google_search = "https://www.google.com/search?q="+"samsung"
  reddit_posts = "https://www.reddit.com/r/GalaxyS21/"
  i = input("google (g) reddit (r)")
  if i == "g":
    get_links = requests.get(google_search, timeout=5)
  elif i == "r":
    get_links = requests.get(reddit_posts, timeout=5)
  else:
    scan_links()
    
  soup = BeautifulSoup(get_links.content, 'html.parser')
  a = soup.find_all('div')
  a = str(a)

  x = ""
  word_data = []
  hreflinks = []
  for l in a:
      if l == " ":  
          if x.isalpha() == True:
            word_data.append(x)
          if "href" in x:
            hreflinks.append(x)
          x = ""
      else:
          x += l 
  print(word_data)
  print(hreflinks)
  txt = ''
  array = []
scan_links()
