import datetime
import re

from bs4 import BeautifulSoup
import pymysql
import requests
from urllib.error import HTTPError, URLError

#import class
def check_tag(tag, soup_arg):
    if tag not in soup_arg:
        return False
    else:
        return True 

class DB(object): 
    def __init__(self,host1='*****',
                 datasource='****', 
                 db_user='******', 
                 db_password='******'):
        self.conn = pymysql.connect(host=host1, db=datasource, 
                                    user=db_user, password=db_password,
                                     cursorclass=pymysql.cursors.DictCursor)

    def __del__(self):
        self.conn.close()
        print('connection closed')

    def query(self, data_to_insert):
        with self.conn.cursor() as cursor:
            sql = "INSERT INTO *****( \
                             post_url_number, post_date, \
                             post_header, post_text, picture_url, \
                             post_comments, plus) \
                             VALUES(%s, %s, %s, %s,%s, %s, %s)"               
            cursor.execute(sql, data_to_insert)            
            self.conn.commit()
            print('Uploaded information')
    
    def check_post(self, insert_number):
        with self.conn.cursor() as cur:
            if 0 <  cur.execute("Select * FROM ***** \
                                post_url_number = %s", (insert_number,)):
                print('post has been in DB')
                return False
            else:
                return True
    
    def last_record(self):
        with self.conn.cursor() as curs:
            sql = "SELECT * FROM ****** WHERE post_number = (SELECT MAX(post_number) FROM *****);"
            curs.execute(sql)
            return curs.fetchone()


try:
    html = 'https://vc.ru/tech' 
    response = requests.get(html, timeout=10) 
    
except HTTPError as e:
    print(e)
    
except URLError as e:
    print('The server could not be found!')

else:
    print('It Worked!')

soup = BeautifulSoup(response.text, 'lxml') 
# Find 20 last news and check it.
# Whether this news has voices more than 20 and having picture.
for item in soup.find_all( \
    'div', class_='feed__item l-island-round', limit=20):    
    
    if int(item.find( \
        'span', class_='comments_counter__count__value').text) >= 20:       
        
        try:
            image = item.find('div', class_='andropov_image').get( \
                'data-image-src')
                                        
        except AttributeError:
            image = 'no picture'                           
        # Get these news HTML and collect information. 
        post_url = item.find('a', class_='content-feed__link').get('href')
        
        post_number = re.search(r'\d+', str(post_url))
        insert_number = post_number.group()                
        
        new_response = requests.get(post_url)
        new_soup = BeautifulSoup(new_response.text, 'lxml')     
        
        post_date = new_soup.find('time')['title']
        insert_date = (datetime.datetime.strptime(post_date[:10],"%d.%m.%Y")
                    .strftime("%Y-%m-%d"))
        
        header = new_soup.find('h1', class_='content-title').text        
        
        text_post = new_soup.find('div', class_= \
             'content content--full').find_all('p')
        article = ''
        for i in text_post:
            article += i.text.strip()
        
        comments = (int(new_soup.find('span', 
                                class_='comments_counter__count__value').text))
        print(comments)
                
        plus = 0

        info_to_insert = [insert_number, insert_date, 
                        header, article, image, comments, plus]
                      
        try:
            sql_connection = DB()
# Check whether post not in DB.
            if sql_connection.check_post(insert_number):
                sql_connection.query(info_to_insert)
            else:
                print('Post already in DB')            
        except Exception as e:
            print(e)
                
        info_to_insert.clear()

try:
    get_vc_record = DB()
    VC_record = get_vc_record.last_record()

except Exception as e:
    print(e)




    

