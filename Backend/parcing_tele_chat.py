from telethon import TelegramClient, sync, events
from telethon import functions, types
from datetime import datetime
import psycopg2

"""
Automatic authentification in telegram
Parse unread messages from channel which user is subscribed to
Save them in DB(PostgreSQL)
Make them read in telegram channel(green marks)
"""

def upload_data_db(data_to_insert):
    try:
        con = psycopg2.connect(
        database="*******", 
        user="*******", 
        password="*****", 
        host="*****", 
        port="******"        
        )

        print('Successfully connected')
        
        cur = con.cursor()
        for i  in data_to_insert:
            cur.execute(
                "INSERT INTO ******(post_text, post_date,\
                post_id, channel_name) VALUES(%s, %s, %s, %s)", i 
            )       
        con.commit()
        print('news successfully uploaded to DB')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        con.close()
#https://my.telegram.org/auth?to=apps
api_id = ******
api_hash = '********'
phone_number = '******'
client = TelegramClient('Session1', api_id, api_hash)
chats_ = [
    'https://t.me/breakingmash', 'https://t.me/rt_russian',
    'https://t.me/bbcrussian', 'https://t.me/sportsru'
    ]
info = []


client.start()

@client.on(events.NewMessage(chats=chats_))
async def my_event_handler(event):    
  
    info.append((event.text, datetime.now(), event.id, event.chat.title))
    print('1')
    if len(info) >= 10 :
        upload_data_db(info) 
        info.clear()

client.run_until_disconnected()

# нужна команда чтобы прервать программу

