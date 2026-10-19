from flask import Flask , render_template , request, redirect, flash, session
from flask import jsonify
from main import load_songs_from_csv, save_songs_to_CSV, check_song_number_format, check_polish_character, check_duration_format, song_number_exists, overwrite_song_title_and_duration, convert_time_to_sec, convert_sec_to_time, check_place_format
from pdf_generator import generate_pdf_file
import datetime as dt

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
        song = find_song_row_by_number(number, songs)
        current_title = song["title"]
        current_duration = song["duration"]
        return render_template(
                "edit_song.html", 
                number= number, 
                title= current_title, 
                duration= current_duration
                )

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
                return render_template(
                        "edit_song.html", 
                        error= "Invalid song duration format. Please, use mm:ss format.", 
                        number = number, 
                        title= new_title, 
                        duration= new_duration
                        )
        else:
            return render_template(
                    "edit_song.html", 
                    error= "Please, use title w/o polish characters", 
                    number = number,
                    title = new_title, 
                    duration= new_duration
                    )

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/remove", methods= ["GET", "POST"])
def remove_song():
    songs = load_songs_from_csv()
    if request.method == "GET":
        return render_template("remove.html", remove_number="")
    else:
        number = request.form["remove_number"]
        if song_number_exists(number,songs):
            return redirect(f"/remove/{number}")
        else:
            return render_template("remove.html", error = f"Song {number} does not exist in database.")

@app.route("/remove/<number>", methods=["GET","POST"])
def confirm_remove_song(number):
    songs = load_songs_from_csv()
    song= find_song_row_by_number(number, songs)
    if request.method == "GET":
        return render_template("remove_confirm.html", number= number, title= song["title"])
    elif request.method == "POST":
        songs.remove(song)
        save_songs_to_CSV(songs)
        flash(f'Song "{number} - {song["title"]}" successfully REMOVED from database!')
        return redirect("/songs")
    
@app.route("/generate_setlist/get_event_details", methods =["GET", "POST"])  
def get_event_details():
    if request.method == "POST":
        max_length = 200
        event_date = request.form["event_date"]
        event_place = request.form["event_place"].strip()
        if check_date_format(event_date):
            date_object = check_date_format(event_date)
            if check_if_not_past_date(date_object):
                session["date"] = event_date
            else:
                return render_template("get_event_details.html",
                                       error= "Invalid date. Date cannot be from past",
                                       event_date = event_date,
                                       event_place = event_place
                                        )
        else:
            return render_template("get_event_details.html", 
                                    error= "Invalid date format. Please use YYYY-MM-DD",
                                    event_date = event_date,
                                    event_place = event_place
                                    )      
        if check_place_format(event_place):
            if check_place_length(event_place,max_length):
                session["place"] = event_place
            else:
                return render_template("get_event_details.html",
                                        error= f"Place name is too long. Maximum amount cannot exceed {max_length} characters.",
                                        event_date = event_date,
                                        event_place = event_place
                                        )
        else:
            return render_template("get_event_details.html",
                                    error = r'Invalid place format. Place can not include /\:*?"<>| characters',
                                    event_date = event_date,
                                    event_place = event_place
                                    )

        return redirect("/generate_setlist/songs")
    elif request.method == "GET":
        return render_template("get_event_details.html")  

@app.route("/generate_setlist/songs", methods= ["GET", "POST"])
def create_setlist():
    song_quantity = 5
    if request.method == "POST":
        songs = load_songs_from_csv() 
        action = request.form["action"]   
        intro = request.form["intro"]
        soundcheck = request.form["soundcheck"]
        setlist = request.form.getlist("song")
        bis = request.form.getlist("bis")
        data_form = {
                     "soundcheck": soundcheck,
                     "intro": intro,
                     "setlist": setlist,
                     "bis": bis
                     }
        
        if action == "calculate":
            clear_setlist = clear_blank_position_from_list(setlist)
            clear_bis = clear_blank_position_from_list(bis)
            if not check_songs_input(soundcheck,clear_setlist,clear_bis,songs) == None:
                wrong_songs = check_songs_input(soundcheck,clear_setlist,clear_bis,songs)
                return render_template("create_setlist.html",
                                       error =f"song/s {','.join(wrong_songs)} not exist in database",
                                       **data_form
                                       )

            current_duration_sec = calculate_setlist_duration(setlist,songs)
            current_bis_duration_sec = calculate_setlist_duration(bis,songs)
            total_duration_sec = current_duration_sec + current_bis_duration_sec
            minutes, seconds = convert_sec_to_time(current_duration_sec)
            bis_minutes, bis_seconds = convert_sec_to_time(current_bis_duration_sec)
            total_minutes, total_sec = convert_sec_to_time(total_duration_sec)
            current_duration = f"{minutes}min {seconds}sec"
            current_bis_duration = f"{bis_minutes}min {bis_seconds}sec"
            total_duration = f"{total_minutes}min {total_sec}sec"
            return render_template(
                        "create_setlist.html",
                        **data_form, 
                        current_duration=current_duration, 
                        current_bis_duration= current_bis_duration, 
                        total_duration=total_duration
                        )
        elif action == "generate":
            clear_setlist = clear_blank_position_from_list(setlist)
            clear_bis = clear_blank_position_from_list(bis)
            if not check_songs_input(soundcheck,clear_setlist,clear_bis,songs) == None:
                            wrong_songs = check_songs_input(soundcheck,clear_setlist,clear_bis,songs)
                            return render_template("create_setlist.html",
                                                   error =f"song/s {','.join(wrong_songs)} not exist in database",
                                                   **data_form
                                                   )
            event_date = session["date"]
            event_place = session["place"]
            current_duration_sec = calculate_setlist_duration(setlist,songs)
            soundcheck = find_song_row_by_number(soundcheck,songs)
            setlist = create_songlist(setlist,songs)
            bis = create_songlist(request.form.getlist("bis"),songs)
            
            generate_pdf_file(  event_date,
                                event_place,
                                soundcheck,
                                intro,
                                setlist,
                                current_duration_sec,
                                bis
                                )
            flash("Setlist successfuly generated and saved!")
        elif action == "add_row":
            setlist.append("")
            return render_template(
                            "create_setlist.html", 
                            intro=intro, 
                            soundcheck=soundcheck, 
                            setlist=setlist, 
                            bis=bis
                            )
        elif action == "remove_row":
            if setlist:
                setlist.pop()
            return render_template(
                "create_setlist.html", 
                intro=intro, 
                soundcheck=soundcheck, 
                setlist=setlist, 
                bis=bis
                )
        elif action == "add_bis":
            bis.append("")
            return  render_template(
                    "create_setlist.html", 
                    intro=intro, 
                    soundcheck=soundcheck,
                    setlist=setlist, 
                    bis=bis
                    )
        elif action == "remove_bis":
            if bis:
                bis.pop()
            return  render_template(
                    "create_setlist.html", 
                    intro=intro, 
                    soundcheck=soundcheck,
                    setlist=setlist, 
                    bis=bis
                    )
        return redirect("/songs")

    elif request.method == "GET":
        setlist = []
        for _ in range(song_quantity):
            setlist.append("")
        return render_template("create_setlist.html", setlist = setlist, bis = [""])  

# ----------------- auxiliary functions -----------------

def find_song_row_by_number(number,database):

    for song in database:
        if song["number"] == str(number):
            return song
        
def calculate_setlist_duration(songlist,database):
    current_duration_sec = 0
    for song in songlist:
        if song_number_exists(song,database):
            current_song = find_song_row_by_number(song,database)
            current_duration_sec += convert_time_to_sec(current_song["duration"])
    return current_duration_sec

def create_songlist(user_setlist,database):
    song_list = []
    for song_number in user_setlist:
        for row in database:
                    if row["number"] == str(song_number):
                        song_list.append({"number": row["number"], "title": row["title"]})
    return song_list

def check_date_format(date):
    try:
        date_object = dt.datetime.strptime(date, "%Y-%m-%d").date()
        return date_object
    except ValueError:
        return False

def check_if_not_past_date(date_object):
    today_date = dt.date.today()
    if today_date > date_object: 
        return False
    return True
    
def check_place_length(place,max_length):
    if len(place) > max_length:
        return False
    return True

def check_song_list(songlist,database):
    for song in songlist:
        if not song_number_exists(song,database):
            return False
    return True

def list_wrong_songs(song_list,database):
    wrong_list = []
    for song in song_list:
        if not song_number_exists(song,database):
            wrong_list.append(song)
    return wrong_list

def check_songs_input(soundcheck,setlist,bis,database):
    wrong = []
    if not song_number_exists(soundcheck,database):
        wrong.append(soundcheck)
    if not check_song_list(setlist,database):
        wrong_songs = list_wrong_songs(setlist,database)
        wrong.extend(wrong_songs)
    if not check_song_list(bis,database):
        wrong_bis = list_wrong_songs(bis,database)
        wrong.extend(wrong_bis)
    
    if len(wrong) > 0:
        return wrong

def clear_blank_position_from_list(setlist):
    clear_setlist = []
    for song in setlist:
        if song != "":
            clear_setlist.append(song)
    return clear_setlist
                
if __name__ == "__main__":
    app.run(debug=True)