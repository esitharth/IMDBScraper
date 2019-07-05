from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import csv as csv
import time
from PIL import Image
import requests
from io import BytesIO
import os
import datetime
import argparse

def Main():
    #using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", help="scrap the titles of IMDB movies set.", dest="title", action="store_true")
    parser.add_argument("-p", help= "scraps the posters of IMDB movies set", dest="poster", action="store_true")
    parser.add_argument("-tp", help="scraps the titles and posters of IMDB movies set", dest="titleposter", action="store_true")
    args = parser.parse_args()

    if(args.title == True):
        scraper
    elif(args.poster == True):
        poster_scraper
    elif(args.titleposter == True):
        scraper
        poster_scraper



def time_calc(*args, **kwargs):         #decorator definition
    def func_wrapper(func):
        if kwargs['enable']:
            if kwargs['logTime']:
                start_time = time.time()
                func()
                end_time = time.time()
                time_taken = end_time - start_time
                print(time_taken)

                if kwargs['logToFile']:
                    file = open("files/log.txt","a")
                    file.write("Executed at: "+ str(datetime.datetime.now()) +" Total Time of execution: " + str(time_taken) + " Function Executed: "+ func.__name__ +"\n" )
                    file.close()

            elif not kwargs['logTime']:
                 func()

        elif not kwargs['enable']:
            func()

    return func_wrapper


def writelisttocsv(csv_file, data_list):

    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
        for data in data_list:
            writer.writerow(data)
    return


@time_calc(enable=True, logTime=True, logToFile=True)
def scraper():
    url = "https://www.imdb.com/chart/top?ref_=nv_wl_img_3"
    html = urlopen(url)
    df = pd.DataFrame()
    bs = BeautifulSoup(html.read(), 'html.parser')
    #get table containing the values
    table = bs.find_all('table')[0]
    i = 0
    df = [("id","movie_name", "link_to_detail", "poster_link")]
    # get movie names
    for row in bs.select("table tr"):

        if (row):
            element = row.find("td", {"class": "titleColumn"})
            if (element):

                movie_name = element.findChild().text #getting the individual movie names
                print(i)
                i=i+1
                print(movie_name)
                http_link = "http://www.imdb.com" + element.find('a').get('href') #navigating to the movie's page
                print(http_link)
                html = urlopen(http_link)
                bs1 = BeautifulSoup(html.read(), 'html.parser')
                poster_div = bs1.find("div", {"class": "poster"})
                poster_http = poster_div.find("img").get('src') #getting the poster url
                print("poster_http : " + poster_http)
                df.append((i, movie_name, http_link, poster_http)) #appending to the dataframe

                # if (i == 4):
                #     break

    csv_file = "IMDB_Movie_index.csv"
    writelisttocsv(csv_file, df) #Saving the dataframe to csv


@time_calc(enable=True, logTime=True, logToFile=True)
def poster_scraper():
    df = pd.read_csv('IMDB_Movie_index.csv') #loading dataframe from csv
    df_imgsrc = df['poster_link'] #loading poster source url
    df_imgname = df['movie_name'] #loading movie name url
    print("posters at /posters")
    i = 0
    for imgurl in df_imgsrc:
        print(i)
        print(imgurl)
        response = requests.get(imgurl)
        img = Image.open(BytesIO(response.content))
        #print(img)
        img_name = df_imgname[i]+ '.jpg'
        img.save('posters/'+img_name,  'JPEG')
        i=i+1


#poster_scraper

if __name__ == '__main__':
    Main()
