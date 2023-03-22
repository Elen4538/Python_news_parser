"""
@author: Lena
"""

import datetime
import re

from bs4 import BeautifulSoup
import psycopg2
import requests
from urllib.error import HTTPError, URLError

class MyDatabase():
    def __init__(self, database1="*******",
                user1="*******",
                password1="********",
                host1="********", 
                port1="******"
                ):
        self.conn = psycopg2.connect(database=database1, 
                                    user=user1, 
                                    password=password1,
                                    host=host1,
                                    port=port1                                    
                                    ) #cursorclass=psycopg2.extras.DictCursor    
    def __del__(self):
        self.conn.close()
        print('connection closed')

    def query(self, info_to_insert):
  
        with self.conn.cursor() as curs:            
            sql = "INSERT INTO ***********(post_url_number, post_date, \
                                            post_header, post_text,\
                                            picture_url, post_comment, plus)\
                                            VALUES(%s, %s, %s, %s, %s, %s, %s)"
            curs.execute(sql, info_to_insert)
            self.conn.commit()                       
        print('info uploaded successfully')
        
    def check_post(self, insert_number):
        with self.conn.cursor() as cur:           
            exists_query = """ SELECT * FROM ******** WHERE\
                                post_url_number = %s """            
            cur.execute(exists_query, (insert_number,))
            res = cur.fetchone()  
            if res != None:
                print('in db')
                return True 
            else:
                print('not in db')
                return False         
try:

    html = "https://tjournal.ru/news"   
    response = requests.get(html, timeout=10)
    
except HTTPError as e:
    print(e)
    
except URLError as e:
    print('The server could not be found!')
else:
    print('It Worked!')

soup = BeautifulSoup(response.text, 'lxml')

for news in soup.find_all('div', class_='feed__item l-island-round', limit=20):   
    # News has zero comments    
    if str(news.find("span", 
                    class_="vote__value__v vote__value__v--real").text) == '—':
        print('news has no voices, next news')
    # select news which has voices more than 30
    else:
    
        if int(news.find("span",
            class_="vote__value__v vote__value__v--real").text) >= 30:   
        
            try:
                image = (news.find('div', class_='andropov_image')
                        .get('data-image-src'))
            except AttributeError:
                image = 'no picture'
                
            post_url = news.find('a', class_='content-feed__link').get('href')
            
            post_number = re.search(r'\d+', str(post_url))
            insert_number = post_number.group()        
        
            post_response = requests.get(post_url)
            post_soup = BeautifulSoup(post_response.text, 'lxml')        
        
            post_date = post_soup.find('time')['title']
            insert_date = (datetime.datetime.strptime(post_date[:10], "%d.%m.%Y")
                        .strftime("%Y-%m-%d"))
        
            post_header = post_soup.find('h1', class_='content-title').text
        
            post_text = (post_soup.find('div', class_='content content--full')
                        .find_all('p'))
                
            article = ''
            for i in post_text:
                article += i.text.strip()

            comments = int(post_soup.find('span', 
                class_='comments_counter__count__value').text)
            
            plus = 0
            
            info_to_insert = [insert_number, insert_date, 
                            post_header, article, image,
                            comments, plus]        
            try:
                sql_upload = MyDatabase()
                if not sql_upload.check_post(insert_number): 
                    sql_upload.query(info_to_insert)
                else:
                    print('Post already in DB')             
                    
            except Exception as e:
                print(e)
            
            info_to_insert.clear()