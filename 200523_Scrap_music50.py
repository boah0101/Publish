import requests
from bs4 import BeautifulSoup
# URL을 읽어서 HTML를 받아오고,

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.



headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200403&hh=23&rtm=N&pg=1',headers=headers)
# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')


songs = soup.select("#body-content > div.newest-list > div > table > tbody > tr")
count = 0

for song in songs:
    a_tag = song.select_one("td.info > a.title")
    if a_tag is not None:
        count = count +1
        title = song.select_one("td.info > a.title").text  
        artist = song.select_one("td.info > a.artist").text                
        print(count," ",title.strip()," by ",artist.strip())
        
   
        doc = {
            'rank' : count,
            'title' : title.strip(),
            'artist' : artist,
            }
        db.songs.insert_one(doc)