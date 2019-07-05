from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import csv as csv
import time
from PIL import Image
import requests
from io import BytesIO
from sqlalchemy import MetaData, create_engine, Column, Integer, String, ForeignKey, Table, insert, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, session
from flask_sqlalchemy import SQLAlchemy
meta = MetaData()
db = SQLAlchemy()
Base = declarative_base()


class Movie(Base):
   __tablename__ = 'movies'
   id = Column(Integer, primary_key =  True)
   name = Column(String)

   link = Column(String)
   poster_link = Column(String)


def create_DB():
    data = pd.read_csv('IMDB_Movie_index.csv')
    engine = create_engine('sqlite:///movies.db', echo=True)

    Movie.drop(engine)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    # movies = Table('movies', meta,
    #                Column('id', Integer, primary_key=True),
    #                Column('movie_name', String, unique=True),
    #                Column('movie_link', String, unique=True),
    #                Column('poster_link', String, unique=True))


    # engine = create_engine('sqlite:///movies.db', echo=True)

    # meta.create_all(engine)
        #engine.execute(tbl.delete())


   # # movie = Movies()
   #
   #  conn = engine.connect()
   #  stmt = insert(movies)
   #  dict = data.to_dict('records')
   #  result = conn.execute(stmt, dict)
    for index, row in data.iterrows():
        c = Movie(id = index, name = row['movie_name'], link = row['link_to_detail'], poster_link = row['poster_link'])
        session.add(c)
        session.commit()
        # result = conn.execute(stmt)
    for row in result:
        print(row)
    session.close()


def read_db(movi_name):
    engine = create_engine('sqlite:///movies.db', echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    q = select(movies).where(movie_name == 'Le parrain')
    result = conn.execute(q)
    print(result)

def time_calc(func): #decorator definition
    def func_wrapper():
        start_time = time.time()
        func()
        end_time = time.time()
        return (end_time - start_time)
    return func_wrapper


def writelisttocsv(csv_file, data_list):

    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
        #writer.writerow(csv_columns)
        for data in data_list:
            writer.writerow(data)
    return

@time_calc #decorator usage
def scraper():
    url = "https://www.imdb.com/chart/top?ref_=nv_wl_img_3"
    html = urlopen(url)
    df = pd.DataFrame()
    bs = BeautifulSoup(html.read(), 'html.parser')

    table = bs.find_all('table')[0]
    i = 0
    df = [("id","movie_name", "link_to_detail", "poster_link")]
    # get movie names
    for row in bs.select("table tr"):

        if (row):
            element = row.find("td", {"class": "titleColumn"})
            if (element):
               # print(element.find('a').get('href'))

               # print(element.select("a"))
                movie_name = element.findChild().text
                print(i)
                i=i+1
                print(element.findChild().text)
                http_link = "http://www.imdb.com" + element.find('a').get('href')
                print(http_link)
                html = urlopen(http_link)
                bs1 = BeautifulSoup(html.read(), 'html.parser')
                poster_div = bs1.find("div", {"class": "poster"})
                #print(poster_div)
                poster_http = poster_div.find("img").get('src')
                print("poster_http : " + poster_http)
                df.append((i, movie_name, http_link, poster_http))
                #i = i + 1

                if (i == 4):
                    break
    #df.to_csv('IMDB_Movie_index.csv', index=None, header=True)
    tuple = df[2]
    print(tuple[2])
    csv_file = "IMDB_Movie_index.csv"
    writelisttocsv(csv_file, df)

def poster_scraper():
    df = pd.read_csv('IMDB_Movie_index.csv')
    df_ImgSrc = df['poster_link']
    i = 1
    for imgUrl in df_ImgSrc:
        print(imgUrl)
        response = requests.get(imgUrl)
        img = Image.open(BytesIO(response.content))
        print(img)
        img_name = str(i) + '.jpg'
        img.save('/home/sitharth/Programming/PythonProjectEpitaSem1/venv/posters/'+img_name,  'JPEG')
        i=i+1

#poster_scraper()

#print(scraper())

create_DB()

read_db('Les évadés')
