from flask import Flask , render_template , request
from flask import jsonify
from main import load_songs_from_csv, save_songs_to_CSV, check_song_number_format, check_polish_character, check_duration_format


app = Flask(__name__)

@app.route("/songs")

def load_songs():
    songs = load_songs_from_csv()
    return render_template("songs.html",songs = songs)

@app.route("/greet", methods= ["GET", "POST"])

def post():
    if request.method == "POST":
        username = request.form["username"] 
        return f"Hello, {username}"
    else:
        return render_template("greet.html")

@app.route("/add_song", methods= ["GET", "POST"])

def add_song():
    if request.method == "POST":
        songs = load_songs_from_csv()
        new_number = request.form["number"]
        new_title = request.form["title"]
        new_duration = request.form["duration"]

        if check_song_number_format(new_number):
            if not check_polish_character(new_title):
                if check_duration_format(new_duration):
                    songs.append({"number": new_number, "title": new_title, "duration": new_duration})
                    save_songs_to_CSV(songs)
                    return "New song save to database"
                else:
                    return render_template("add_song.html", error= "Invalid duration format", number= new_number, title= new_title)
            else:
                return render_template("add_song.html", error= "Please, use title w/o polish characters", number= new_number, duration= new_duration)
        else:
            return render_template("add_song.html", error= "Invalid song number format", title= new_title, duration= new_duration)
        
    else:
        return render_template("add_song.html", number= "", title= "", duration= "")






if __name__ == "__main__":
    app.run(debug=True)