from flask import Flask
from flask import jsonify
from main import load_songs_from_csv

app = Flask(__name__)

@app.route("/songs")

def load_songs():
    songs = load_songs_from_csv()

    database = "<p> ===== CURRENT DATABASE ===== </p>"

    for row in songs:
        song_line = f'<ul>{row["number"]}. {row["title"]} - {row["duration"]}</ul>'
        database = database + song_line
    database = database + "<p>============================</p>"
    return database

app.run(debug=True)