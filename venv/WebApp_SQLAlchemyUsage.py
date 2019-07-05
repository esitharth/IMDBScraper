from flask import Flask, render_template, request, send_from_directory
import pandas as pd

from flask_sqlalchemy import SQLAlchemy
#from IMDB_Scrape import scraper, poster_scraper

import os
import zipfile

df = pd.read_csv('IMDB_Movie_index.csv')
df.set_index('id', inplace=True)
#scraper()
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config[‘SQLALCHEMY_DATABASE_URI’] = ‘sqlite:///’ + os.path.join(basedir, ‘app.sqlite’)
db = SQLAlchemy(app)

class Movie(db.Model):
    name = db.Column(db.String(40), unique=True, nullable=False, primary_key=True)
    link = db.Column(db.String, unique=True)
    poster_link = db.Column(db.String, unique=True)

    def __init__(self, name, link, poster_link):
        self.name = name
        self.link = link
        self.poster_link = poster_link



if __name__ == "__main__":
    app.run(debug=True)

#
# @app.route("/")
# def main():
#     return render_template('index.html', table = df.to_html())
#
# @app.route('/', methods=['POST','GET'])
# def main_post():
#     if(request.form.get("list_all","")):
#
#         df_movies = df.iloc[:,[0]]
#         return render_template('index.html', table=df_movies.to_html())
#
#     elif (request.form.get("list_all_with_link", "")):
#         df_movies_link = df.iloc[:, [0,1]]
#         return render_template('index.html', table=df_movies_link.to_html())
#         #print("current_pop_film_with_poster")
#     elif (request.form.get("list_all_with_poster_link", "")):
#         print("current_pop_film_with_poster")
#     elif (request.form.get("poster_for_one_film", "")):
#         print("current_pop_film_with_poster")
#     elif (request.form.get("scrape_all_poster", "")):
#         if request.method == 'POST' :
#             poster_scraper()
#             print("display posters")
#             zipf = zipfile.ZipFile('posters/Posters.zip', 'w', zipfile.ZIP_DEFLATED)
#             zipdir('posters',zipf)
#             zipf.close()
#             #return send_file('posters','1.jpg', as_attachment=True)
#             return send_from_directory('posters', filename = 'Posters.zip', as_attachment=True)
#             #return render_template('index.html')

#file path /home/sitharth/Programming/PythonProjectEpitaSem1/venv/posters/
# @app.route('/display_posters', methods=['POST','GET'])
# def display_posters():
#
#     return


# if __name__ == "__main__":
#     app.run()

