from flask import Flask , render_template , request, redirect, flash
from flask import jsonify
from main import load_songs_from_csv, save_songs_to_CSV, check_song_number_format, check_polish_character, check_duration_format, song_number_exists, overwrite_song_title_and_duration


app = Flask(__name__)
app.secret_key = "temp"

@app.route("/songs")

def load_songs():
    songs = load_songs_from_csv()
    return render_template("songs.html",songs = songs)


@app.route("/add_song", methods= ["GET", "POST"])

def add_song():
    if request.method == "POST":
        songs = load_songs_from_csv()
        new_number = request.form["number"]
        new_title = request.form["title"]
        new_duration = request.form["duration"]

        if check_song_number_format(new_number):
            if not song_number_exists(new_number, songs):
                if not check_polish_character(new_title):
                    if check_duration_format(new_duration):
                        songs.append({"number": new_number, "title": new_title, "duration": new_duration})
                        save_songs_to_CSV(songs)
                        flash("New song successfully added to database!")
                        return redirect("/songs") 
                    else:
                        return render_template("add_song.html", error= "Invalid duration format", number= new_number, title= new_title, duration= new_duration)
                else:
                    return render_template("add_song.html", error= "Please, use title w/o polish characters", number= new_number, title= new_title, duration= new_duration)
            else:
                return render_template("add_song.html", error= "Song currently exist in database", number= new_number, title= new_title, duration= new_duration)
        else:
            return render_template("add_song.html", error= "Invalid song number format", number= new_number, title= new_title, duration= new_duration)
        
    else:
        return render_template("add_song.html", number= "", title= "", duration= "")

@app.route("/edit_song/<number>", methods= ["POST", "GET"])

def edit_song(number):

    songs = load_songs_from_csv()
    if request.method == "GET":
        current_title, current_duration = find_song_by_number(number, songs)
        return render_template("edit_song.html", number= number, title= current_title, duration= current_duration)

    elif request.method == "POST":
        new_title = request.form["title"]
        new_duration = request.form["duration"]
        if not check_polish_character(new_title):
            if check_duration_format(new_duration):
                overwrite_song_title_and_duration(number,new_title,new_duration,songs)
                save_songs_to_CSV(songs)
                flash(f"Song {number} -  successfully updated in database!")
                return redirect("/songs")
            else:
                return render_template("edit_song.html", error= "Invalid song duration format. Please, use mm:ss format.", number = number, title= new_title, duration= new_duration)
        else:
            return render_template("edit_song.html", error= "Please, use title w/o polish characters", number = number,title = new_title, duration= new_duration)
@app.route("/home")

def home():
    return render_template("home.html")

# ----------------- auxiliary functions -----------------

def find_song_by_number(number,database):

    for song in database:
        if song["number"] == str(number):
            current_title = song["title"]
            current_duration = song["duration"]
            return current_title, current_duration
        


if __name__ == "__main__":
    app.run(debug=True)