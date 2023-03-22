import psycopg2
import pymysql
import sqlite3
import telebot

# программа должна вытаскивать самую популярную новость и передавать в телеграм канал

token = '**************'
bot = telebot.TeleBot(token)
chat_id = *************

#VC
try:
    conn_vc = pymysql.connect(host='******',
                            db='*********', 
                            user='*******', 
                            password='**************')
    print('Successfully connected to *****')
    
    with conn_vc.cursor() as curs:

        sql_query = 'SELECT * FROM **** \
                    WHERE post_comments= (SELECT MAX(post_comments) \
                    FROM ******);'
        curs.execute(sql_query)
        result_VC = curs.fetchone()

except Exception as e:
    print(e)
#TJ
try:
    conn_tj = psycopg2.connect(database="**********", 
                                user="********",
                                password="*******",
                                host="*********", 
                                port="*********")
    print('Successfully connected to TJ_db')
    
    with conn_tj.cursor() as curs:
        sql_query = "SELECT * FROM ***** WHERE post_comment \
                    = (SELECT MAX(post_comment) FROM *******);"
        curs.execute(sql_query)
        result_TJ = curs.fetchone()

except Exception as e:
    print(e)
#Habr
try:
    conn_habr = sqlite3.connect('************')
    print("Successfully connected to SQLite")
    sql_query = 'SELECT * FROM ******* WHERE comments \
                = (SELECT MAX(comments) FROM *******);'
    curs = conn_habr.cursor()
    curs.execute(sql_query)
    result_habr = curs.fetchone()    
    curs.close()

except Exception as e:
    print(e)

comments_lst = [result_VC, result_TJ, result_habr] 
print(result_habr)
popular_news = max(comments_lst, key=lambda x: x[-2])
print(popular_news[5])
#switch to telechat send message

try:
    
    info = f'{popular_news[2]}\n{popular_news[3]}\n{popular_news[4]}'
    if len(info) > 4096:
        for x in range(0, len(info), 4096):
            bot.send_message(chat_id, info[x:x+4096])
    else:
        bot.send_message(chat_id, info)

    if popular_news[5] != 'no picture':
        bot.send_message(chat_id, f'{popular_news[5]}')
    
    print('info successfully published in Telegram channel')

except Exception as e:
    print(e)