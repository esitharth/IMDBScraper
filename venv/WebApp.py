from flask import Flask, render_template, request, send_from_directory, send_file
import pandas as pd
# from IMDB_Scrape import scraper, poster_scraper
import os
import zipfile
import datetime
import jinja2
df = pd.read_csv('IMDB_Movie_index.csv') #loading dataframe from csv
df.set_index('id', inplace=True, verify_integrity=True) #setting index
temp = df
app = Flask(__name__)


def log(*args, **kwargs):         #decorator definition
    def func_wrapper(func):
        if kwargs['enable']:
            if kwargs['logTime']:
                if kwargs['logToFile']:
                    file = open("files/webapp_log.txt", "a")
                    file.write("Executed at: " + str(datetime.datetime.now()) + " Function Executed: " + func.__name__ + "\n")
                    func
                    file.close()
                elif not kwargs['logToFile'] :
                    func
            elif not kwargs['logTime']:
                func
        elif not kwargs['enable']:
            func
    return func_wrapper


@log(enable=True, logTime=True, logToFile=True) #log decorator
@app.route("/")
def main():
    dff = df
    return render_template('index.html', table = dff.head(50).values)


@log(enable=True, logTime=True, logToFile=True)
@app.route('/', methods=['POST','GET'])
def main_post():
    global df
    global temp
    dff = df
    if request.form.get("list_all",""):
        return render_template('index.html', table=dff.iloc[:,[0]].head(50).values)

    elif request.form.get("search_movie_in_list", ""):
        search = request.form.get("search")
        df_searched_movies = dff['movie_name']== search
        temp = dff[df_searched_movies].iloc[:, [0, 1]]
        return render_template('index.html', table=dff[df_searched_movies].iloc[:, [0,1]].head(50).values)

    elif request.form.get("delete_movie_in_list", ""):
        delete = request.form.get("delete")
        dff = dff[dff.movie_name!=delete]
        temp = dff[dff.movie_name != delete]
        print(dff)
        df = dff
        return render_template('index.html',table=dff.iloc[:, [0]].head(50).values)

    elif request.form.get("modify_movie", ""):
        modify_old = request.form.get("modify-old")
        modify_new = request.form.get("modify-new")

        dff.movie_name = dff.movie_name.replace(modify_old, modify_new)
        df = dff
        temp = dff
        return render_template('index.html', table=dff.iloc[:, [0, 1]].head(50).values)

    elif request.form.get("to-json", ""):
        temp.to_json(r'files/json/table_dump.json')
        return send_from_directory('files/json/', filename='table_dump.json', as_attachment=True)

    elif request.form.get("to-csv", ""):
        temp.to_csv(r'files/csv/table_dump.csv')
        return send_from_directory('files/csv/', filename='table_dump.csv', as_attachment=True)

    elif request.form.get("get-poster", ""):
        try:
            return send_from_directory('posters/', filename= request.form.get("get-poster","")+".jpg", as_attachment=True)
        finally:
            return render_template('index.html', table = dff.head(50).values)


if __name__ == "__main__":
    app.run(debug=True)

