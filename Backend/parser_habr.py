import sqlite3 
import requests
from bs4 import BeautifulSoup
#from fake_useragent import UserAgent
from urllib.error import HTTPError, URLError
import re
import fake_useragent

class Database():

    def __init__(self):
        self.connection = sqlite3.connect(
                                '*****')
        print("Successfully connected to SQLite")
    
    def __del__(self):
        self.connection.close()
        print('DB is closed')
    
    def query(self, data):
        try:
            sql = ("INSERT INTO **********( \
                                        post_number, post_date, post_header,\
                                        post_text, image_url, tags, comments,\
                                        plus) VALUES(?, ?, ?, ?, ?, ?, ?, ?)")
            curs1 = self.connection.cursor()
            curs1.execute(sql, (*data,))
            self.connection.commit()
            curs1.close()
            print('Data uploaded successfully')
        except Exception as e:
            print('query Error:', e)
    
    def check_data(self, post_number):
        try:
            curs = self.connection.cursor()
            sql = "SELECT EXISTS(SELECT * FROM ******* WHERE post_number =?)" ##
            curs.execute(sql, (post_number,))               
            self.connection.commit()        
            res = curs.fetchone()[0] 
            curs.close()

            if res >= 1: 
                print('news in BD already')
                return False
            else:
                print('need to add news in DB')
                return True
        except Exception as e:
            print('check_data Error:', e)

user = fake_useragent.UserAgent().random
url = 'https://habr.com/ru/all/'
header = {'user-agent': user}
list_to_parse = []

try:
    response = requests.get(url,headers=header, timeout=10)
except HTTPError as e:
    print(e)
    
except URLError as e:
    print('The server could not be found!')
else:
    print('It Worked!')    

soup = BeautifulSoup(response.text, 'lxml')

for news in soup.select('article.tm-articles-list__item', limit=20): 
    part_reference = news.find('a', class_=\
                                'tm-article-snippet__title-link').get('href')
    list_to_parse.append('https://habr.com'+part_reference)
    
# Parse each news in the list.
# Prepare Soup, collect information into variable.
for news in list_to_parse:
    news_response = requests.get(news)
    news_soup = BeautifulSoup(news_response.text, 'lxml')
   
    post_number =  (re.search(r'\d+', str(news))).group()
    print(post_number)
    
    post_date = news_soup.find('time')['title'][:10]
    insert_date = str(post_date)

    post_header = (news_soup.find('h1', class_='tm-article-snippet__title tm-article-snippet__title_h1').text) 
    
    insert_header = str(post_header)
    
    post_article = ''
    for words in news_soup.find_all('div', id='post-content-body'):
        post_article += words.text 
    
    tags_list = []
    
    tags = (news_soup.find('div', class_=
                            'tm-separated-list tm-article-presenter__meta-list')
                            .find_all('a', class_='tm-tags-list__link'))
    for tag in tags:
        tags_list.append(tag.text)
    tags_string = ', '.join(tags_list) 
    print('tags:')
    print(tags_string)

    comments = news_soup.find('span', class_='tm-article-comments-counter-link__value').text
    comments = re.sub('\D', '', comments)
    if len(comments) == 0:
        comments = 0
    
    print('comments:')
    print(comments)
    plus = 0
    
    try:
        
        link = news_soup.find('div', class_='article-formatted-body article-formatted-body_version-2').find('img')
        image = link.get('data-src')
        
    except AttributeError:
        image = 'no picture'
        print('no picture')

    info_to_insert = [post_number, insert_date, insert_header,
                    post_article, image, tags_string, comments, plus]

    try:
        sql_upload = Database()
        print('instance created')
        if sql_upload.check_data(post_number):
            sql_upload.query(info_to_insert)
            print('Data uploaded')
    except sqlite3.Error as error:
        print('Connection error', error)
    except Exception as e:
        print('Another error:', e)
    info_to_insert.clear()