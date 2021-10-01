import mimetypes
from tkinter import *
import tkinter as tk
import os
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Progressbar
import praw
import datetime
import webbrowser
from tkcalendar import DateEntry
import requests
from bs4 import BeautifulSoup
import re
import time
from joblib import Parallel, delayed
import multiprocessing


root = tk.Tk()
root.geometry('1000x400')

local_time = time.localtime()
hr = local_time.tm_hour
min = local_time.tm_min
mon = local_time.tm_mon
sec = local_time.tm_sec
day = local_time.tm_mday
fn = f'{mon}_{day}_21.csv'

current_date = f"{mon}/{day}/21"
# ********* Months must be automated
us_com_date = f'May {day}, 2021'
data = open(fn, 'a', encoding="utf-8")
data.write("model, date, topic, description, comments, link" + "\n")

num_cores = multiprocessing.cpu_count()

def us_community(search, my_day):
    # only gets first page

    # search = ['https://us.community.samsung.com/t5/Galaxy-S21/bd-p/GalaxyS21']
    data = open(fn, 'a', encoding="utf-8")

    r = requests.get(search, timeout=5)
    soup = BeautifulSoup(r.content, 'lxml')
    a = soup.find_all('h3')
    link_regex = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",str(a))
    #print(link_regex)

    for link in link_regex:
       #r = requests.get(link)#, timeout=60)
        r = requests.get(link)#, timeout=60)
        soup = BeautifulSoup(r.content, 'lxml')
        post_date = soup.find(class_='custom-topic-date')
        #d = soup.find(class_="DateTime lia-message-posted-on lia-component-common-widget-date")
        lfd = soup.find(class_="local-friendly-date")
        asd = soup.find(class_="DateTime lia-message-posted-on lia-component-common-widget-date")
        #print(link)
        #replies = soup.find_all("div", {"class": "lia-message-body-content"})
        time = soup.find("title", {"class":"local-friendly-date"})
        '''
        if int(my_day) < 10:
            my_day = f'0{my_day}
        '''
        if f"{mon}-{my_day}-2021" in str(asd):#str(lfd):
            post_time = re.search('\d+-\d+-\d{4} \d+:+\d+ \w{2}', str(asd))
            #print(asd)
            print(post_time.group())
            #os.startfile(link)
            t = lfd['title']
            a = soup.find('h2')

            lfd = soup.find_all(class_="local-friendly-date")

            com_list = []
            replies = soup.find_all("div", {"class": "lia-message-body-content"})
            for com, rep in zip(lfd, replies):
                print(str(com["title"]))
                print(str(rep.get_text()).replace("\n", "").replace("\t", ""))
                com_list.append(
                    str(com["title"]) + str(rep.get_text()).replace("\n", "").replace("\t", "").replace(",", ""))
            try:
                #print(com_list[0])
                #print(f'{lfd[0]["title"]},{search[36:]},{str(a.get_text()).replace(",", "")},{com_list[0]},{link},{str(com_list).replace(",", "")}\n')
                data.write(f'{lfd[0]["title"]},{search[36:]},{str(a.get_text()).replace(",", "")},{com_list[0]},{link},{str(com_list).replace(",", "")}\n')
            except IndexError:
                print('index error')
        else:
            continue

uslinks = ['https://us.community.samsung.com/t5/Computers/bd-p/get-help-computers-and-printers',
            'https://us.community.samsung.com/t5/Computing/ct-p/get-help-computing',
            'https://us.community.samsung.com/t5/Galaxy-S21/bd-p/GalaxyS21',
            'https://us.community.samsung.com/t5/Note20/bd-p/get-help-galaxy-note20',
            'https://us.community.samsung.com/t5/Galaxy-S20/bd-p/get-help-galaxy-s20',
            'https://us.community.samsung.com/t5/Galaxy-Z-Flip/bd-p/get-help-galaxy-ZFlip',
            'https://us.community.samsung.com/t5/Galaxy-Fold/bd-p/Gethelp-galaxy-fold',
            'https://us.community.samsung.com/t5/Galaxy-Note-Phones/bd-p/get-help-phones-galaxy-note-phones',
            'https://us.community.samsung.com/t5/Galaxy-S-Phones/bd-p/get-help-phones-galaxy-s-phones',
            'https://us.community.samsung.com/t5/Other-Mobile-Devices/bd-p/get-help-phones-other-mobile-devices']
#uslinks = ['https://us.community.samsung.com/t5/Galaxy-Watch/bd-p/get-help-wearables-galaxy-watch']
def uscom():
    day = input("Enter day of the month: ", )

    results = Parallel(n_jobs=num_cores)(delayed(us_community)(i, day) for i in uslinks)

def get_reddit():
    global te
    s = topic_list.curselection()
    s = topic_list.get(s[0])
    run(s)

def run(subreddit):
    # Authentication
    reddit = praw.Reddit(
        client_id="",
        client_secret="",
        user_agent="",
    )

    data = open(fn, 'a', encoding="utf-8")
    count = 0
    banned_list = ["camera", "tip", "photography", "review", "news", "psa", "spoiler",
                   "update", "advice needed", "general", "impression", 'wallpaper', 'samsung official',
                   'scheduled megathread', "rumor", "pro tip","samsung tv", "shot on galaxy a50 (unedited)",
                   "tips & tricks","wallpapers","cases", "screen protectors", 'purchase', 'availability',
                   'pro tip', 'general discussion', 'meme', 'Galaxy S21U - Exynos', 'leak', 'deal', 'watch band']
    try:

        for submissions in reddit.subreddit(subreddit).new(limit=200):#int(amount.get())):
            c = str(submissions.link_flair_text).lower().strip()
            if c not in banned_list:
                time = submissions.created_utc
                post_time = datetime.datetime.fromtimestamp(submissions.created_utc)
                date = datetime.date.fromtimestamp(time)
                print('-------------------------')
                print(str(cal.get_date())[8:10])
                print('-------------------------')
                if (date == cal.get_date()) and (str(post_time.time())[0:2] >= str(hour.get())):
                    print(c)
                    postlink = "https://www.reddit.com" + submissions.permalink
                    desc = submissions.selftext.replace(",", "")
                    desc = desc.replace("\n", " ")
                    for char in desc:
                        if ord(char) > 255:
                            desc = desc.replace(char, "")
                    title = submissions.title.replace(",", "")

                    if desc == "":
                        desc = submissions.url
                        '''
                        try:
                            os.startfile(desc)
                        except FileNotFoundError:
                            print()
                        '''

                    comment_list = []
                    x = ""
                    link_list.insert(tk.END, postlink)
                    count += 1

                    import re
                    com_count = 0

                    for comment in submissions.comments.list():
                        try:
                            z = re.match("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                                         comment.body)
                            comment.body = comment.body.replace(",", "")
                            for char in comment.body:
                                if ord(char) > 255:
                                    comment.body = comment.body.replace(char, "")
                            '''
                            if z:
                                os.startfile(z.group(0))
                            '''
                            com_count += 1
                            x += f'\n[[#{com_count}]_{datetime.datetime.fromtimestamp(comment.created_utc)}: {comment.body}]'
                        except:
                            print('no body')
                    comment_list.append(x)

                    data.write(f'{post_time},{subreddit},{title},{desc},{postlink},{comment_list} \n')
                    #data.write(f'{c}, {title}, {postlink}\n')
                    t = f'{count}) \n {post_time}\n TITLE: {title}, \n DESCRIPTION: {desc} \n COMMENTS: {len(submissions.comments.list())}\n '

                    for char in t:
                        if ord(char) > 255:
                            t = t.replace(char, "")
                    output_textbox.insert(tk.INSERT, '\n' + t + '\n')

                    for x in comment_list:
                        output_textbox.insert(tk.INSERT, x + '\n')
    except Exception as e:
        pass
    link_list.pack(side=RIGHT, fill=BOTH)

def all_reddit():
    #samsunggalaxy
    '''
    l = ["GalaxyBook", "samsunggalaxy", "SamsungGalaxyASeries", "GalaxyA50", "GalaxyA51",
         "GalaxyA52", "GalaxyA71", "GalaxyFold", "galaxynote10", "GalaxyNote20","galaxyzflip",
         "Note20", "galaxys10", "Galaxy_S20", "GalaxyS20FE", "GalaxyS21", "S21Ultra",
         "GalaxyZFold2", "samsung","GalaxyZFlip3", "Galaxy_ZFold3", "ZFold3", 'galaxybuds',
         'GalaxyWatch']


    l = ["GalaxyBook", "samsunggalaxy", "SamsungGalaxyASeries", "GalaxyA50", "GalaxyA51",
         "GalaxyA52", "GalaxyA71", "galaxynote10", "GalaxyNote20", "Note20", "galaxys10",
         "Galaxy_S20", "GalaxyS20FE", "GalaxyS21", "S21Ultra"]

    '''
    '''
    l = ["GalaxyBook", "samsunggalaxy", "SamsungGalaxyASeries", "GalaxyA50", "GalaxyA51",
         "GalaxyA52", "GalaxyA71", "galaxynote10", "GalaxyNote20", "Note20", "galaxys10",
         "Galaxy_S20", "GalaxyS20FE", "GalaxyS21", "S21Ultra"]

    '''

    l = ["GalaxyBook", "samsunggalaxy", "SamsungGalaxyASeries", "GalaxyA50", "GalaxyA51",
         "GalaxyA52", "GalaxyA71", "GalaxyFold", "galaxynote10", "GalaxyNote20", "galaxyzflip",
         "Note20", "galaxys10", "Galaxy_S20", "GalaxyS20FE", "GalaxyS21", "S21Ultra",
         "GalaxyZFold2", "samsung", "GalaxyZFlip3", "Galaxy_ZFold3", "ZFold3", 'galaxybuds',
         'GalaxyWatch']


    for s in l:
        run(s)


    #results = Parallel(n_jobs=num_cores)(delayed(run(i) for i in l)


def android_central():
    data = open(fn, 'a', encoding="utf-8")

    search = ['https://forums.androidcentral.com/samsung-galaxy-note-20-note-20-ultra/',
              'https://forums.androidcentral.com/samsung-galaxy-note-10-note-10-plus-2019/',
              'https://forums.androidcentral.com/samsung-galaxy-s21-s21-plus-s21-ultra/',
              'https://forums.androidcentral.com/samsung-galaxy-note-9/',
              'https://forums.androidcentral.com/samsung-galaxy-a50/',
              'https://forums.androidcentral.com/samsung-galaxy-s10-s10-plus/',
              'https://forums.androidcentral.com/samsung-galaxy-s20-s20-plus-s20-ultra/',
              'https://forums.androidcentral.com/samsung-galaxy-s9-s9-plus/',
              'https://forums.androidcentral.com/samsung-galaxy-s10e/',
              'https://forums.androidcentral.com/samsung-galaxy-z-flip/',
              'https://forums.androidcentral.com/samsung-galaxy-fold/',
              'https://forums.androidcentral.com/samsung-galaxy-z-flip-3/',
              'https://forums.androidcentral.com/samsung-galaxy-z-fold-3/']

    q = input("Android Central: (y) yesterday, (t) today")

    if q == "y":
        dd = 'Yesterday'
    if q == "t":
        dd = "Today"

    if mon < 10:
        month = f'0{mon}'
    else:
        month = mon
    if day < 10:
        daymod = f'0{day}'
    else:
        daymod = day
    print(f'{month}-{daymod}-2021')

    for search_link in search:
        r = requests.get(search_link, timeout=5)
        soup = BeautifulSoup(r.content, 'lxml')
        a = soup.find_all(class_='t')
        #collect from recent post date, not comment
        post_date = soup.find_all(class_='label')
        post_links = soup.find_all("h1")
        #print(post_links)
        #print(post_date)
        #f'{month}-{daymod}-2021'

        #dd = 'Today'  # f'{mon}-07-2021' #Today Yesterday
        #dd = f'{mon}-12-2021'
        for p,i in zip(post_date,post_links[1:]):
            if dd in p.get_text():
                #print(type(p.get_text()))
                print(p.get_text())
                #print(i)
                link_regex = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(i))
                #print(link_regex)
                #print(i.get_text() + "\n")
                for link in link_regex:
                    r = requests.get(link, timeout=5)
                    soup = BeautifulSoup(r.content, 'lxml')
                    title = i.get_text().replace(",","")
                    m = soup.find(class_="message").get_text().replace(",", "").replace("\n", "")
                    #print(m.get_text())
                    print(f'{dd}\n android central\n{title}\n{m}\n{link}\n{"comments"} \n')
                    data.write(f'{dd} android central,{title},{m},{link}\n')
#android_central()

def xda():
    data = open(fn, 'a', encoding="utf-8")
    x = input("XDA: (y) yesterday, (t) today")

    search = ["https://forum.xda-developers.com/f/samsung-galaxy-s20-fe-questions-answers.11397/",
              'https://forum.xda-developers.com/f/samsung-galaxy-s21.12089/',
              'https://forum.xda-developers.com/c/samsung-galaxy-s21.11933/',
              'https://forum.xda-developers.com/f/samsung-galaxy-s21-ultra.12091/',
              'https://forum.xda-developers.com/c/samsung-galaxy-s21.11933/',
              'https://forum.xda-developers.com/f/samsung-galaxy-a52-5g.12133/',
              'https://forum.xda-developers.com/f/samsung-galaxy-a32-5g.12145/',
              'https://forum.xda-developers.com/c/samsung-galaxy-a42-5g.11705/',
              'https://forum.xda-developers.com/c/samsung-galaxy-s10.8693/',
              'https://forum.xda-developers.com/c/samsung-galaxy-s10.8507/',
              'https://forum.xda-developers.com/c/samsung-galaxy-s10-5g.8861/',
              'https://forum.xda-developers.com/c/samsung-galaxy-note-20-ultra.11203/',
              'https://forum.xda-developers.com/c/samsung-galaxy-note-20.11095/',
              'https://forum.xda-developers.com/c/samsung-galaxy-s20-s20-s20-ultra.9711/',
              'https://forum.xda-developers.com/c/samsung-galaxy-s10e.8763/',
              'https://forum.xda-developers.com/c/samsung-galaxy-note-10.9007/',
              'https://forum.xda-developers.com/c/samsung-galaxy-z-fold-2.11261/',
              'https://forum.xda-developers.com/c/samsung.11975/,'
              'https://forum.xda-developers.com/f/samsung-galaxy-z-fold3.12349/',
              'https://forum.xda-developers.com/f/samsung-galaxy-z-flip-3.12351/']

    # search = ['https://forum.xda-developers.com/f/samsung-galaxy-s21.12089/']
    dd = current_date
    #dd = current_date
    for search_link in search:

        r = requests.get(search_link, timeout=5)
        soup = BeautifulSoup(r.content, 'lxml')

        post_date = soup.find_all(class_="structItem-startDate")

        title = soup.find_all(class_="structItem-title")
        # print(post_date)
        # print(title)
        # link_regex = re.findall("/t/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!3*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str())[0]
        today_list = []
        if x == "y":
            pull_day = "Yesterday"
            dd = f"{mon}/{day-1}/21"
        if x == "t":
            pull_day = "Today"

        for d, t in zip(post_date, title):
            post_date = d.get_text()
            #print(post_date)
            link_regex = re.findall("/t/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(t))[0]

            if pull_day in str(post_date):
                link = "http://forum.xda-developers.com" + str(link_regex)
                r = requests.get(link, timeout=5)
                soup = BeautifulSoup(r.content, 'lxml')
                description = soup.find(class_="bbWrapper").get_text().replace(",", "").replace("\n", "")
                # print(t.get_text())
                print("\n")
                title = t.get_text().replace("\n","")
                # print(post_date)
                # print("forum.xda-developers.com" + str(link_regex))
                today_list.append(f'{post_date}, {link_regex}')
                # '{post_time},{subreddit},{title},{desc},{postlink},{comment_list} \n')
                data.write(f'{dd.strip()}{post_date[8:]},XDA,{title},{description},{str(link)}\n')
                #print(f'{t.get_text()}\n{current_date}\n{post_date[8:]}\n{link} \n {description}')
                #print(f'{current_date} {post_date[8:]},xda,{t.get_text()},{description},{link}')
                print(f'{dd} {post_date[8:]}\nxda\n{title}\n{description}\n{link}')

def send_email():
    import smtplib, ssl
    import email
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    port = 465  # 587
    smtp_server = 'smtp.gmail.com'
    password = 'Plttest135!'
    sender_email = "plttest201@gmail.com"
    receiver_email = "plttest201@gmail.com"

    context = ssl.create_default_context()

    csv = f'{mon}_{day}_21.csv'

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message['Subject'] = f"{csv} Mainstat Update"

    ctype, encoding = mimetypes.guess_type(csv)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/",1)

    fp = open(csv, "rb")
    attachment = MIMEBase(maintype, _subtype=subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)

    message.attach(attachment)

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        #server.echlo()
        #server.starttls(context=context)

        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    data = open(fn, 'r+')
    data.truncate()

#send_email()

#loop the buttons?


download_button = tk.Button(text="Send Email", command=send_email)
download_button.pack(side=TOP)


def us_red_pull():
    uscom()
    all_reddit()
    #send_email()

def xda_ac_pull():
    try:
        xda()
        android_central()
    except Exception as e:
        print(e)
        pass
    #send_email()

download_button = tk.Button(text="Reddit & USCom Pull", command=us_red_pull)
download_button.pack(side=TOP)

download_button = tk.Button(text="XDA/AC", command=xda_ac_pull)
download_button.pack(side=TOP)

amount = tk.Entry()
amount.pack(side=TOP)

#GalaxyA50

sr_button_titles = ["GalaxyBook","GalaxyA50","samsunggalaxy", "GalaxyA51", "GalaxyA52", "GalaxyA71", "GalaxyFold", "galaxynote10", "GalaxyNote20",
                    "Note20", "galaxys10", "Galaxy_S20", "GalaxyS20FE", "GalaxyS21", "S21Ultra", "GalaxyZFold2",
                    "galaxybuds", "samsung", "tmobile", "verizon"]

output_textbox = tk.Text()
output_textbox.pack(side=LEFT, expand=YES, fill=BOTH)

scrollbar = Scrollbar(root)
scrollbar.pack(side=LEFT, fill=Y)

def open_link():
    s = link_list.curselection()
    print(s)
    s = link_list.get(s[0])
    webbrowser.open_new_tab(s)

linkbar = Scrollbar(root)
linkbar.pack(side=RIGHT)
link_list = Listbox(root, yscrollcommand=linkbar.set, width=100)
link_button = tk.Button(text="open link", command=open_link)
link_button.pack(side=RIGHT)

topic_list = Listbox(root, yscrollcommand=scrollbar.set)

for topic in sr_button_titles:
    topic_list.insert(END, topic)
topic_list.pack(side=LEFT)

cal = DateEntry(root, width=12)
cal.pack()

hour = Spinbox(from_=0,to=24,wrap=True,width=2,state="readonly",justify=CENTER)

hour.pack()

import datetime

print(datetime.datetime.now())

scrollbar.config(command=topic_list.yview)
root.mainloop()
