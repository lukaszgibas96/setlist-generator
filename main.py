import csv
from pdf_generator import generate_pdf_file
import datetime as dt

def main():

    run_application()
    
# ---------------------- function definitions

def run_application():

    songs = load_songs_from_csv()
    while True:
    
            show_menu()
            menu_choice = get_menu_choice()
            if menu_choice == 1:

                event_date, event_place = get_event_info_from_user()
                soundcheck = get_soundcheck_from_user(songs)
                intro = get_intro_from_user()
                setlist, setlist_duration = get_song_list_from_user(songs,section = "song")
                bis,_ = get_song_list_from_user(songs, section = "bis")
                generate_pdf_file(event_date,
                                  event_place,
                                  soundcheck,
                                  intro,
                                  setlist,
                                  setlist_duration,
                                  bis)
                say_pdf_saved()


            elif menu_choice == 2:
                show_database(songs)

            elif menu_choice == 3:
                add_song_to_database(songs)

            elif menu_choice == 4:
                edit_song_in_database(songs)

            elif menu_choice == 0:
                say_goodbye()
                break 

def show_menu():

    print("""
    ======================================
              SETLIST GENERATOR
    ======================================

    1. Generate setlist
    2. Show database
    3. Add song
    4. Edit song
    0. Exit
    ---------------------------------------
    """)

def load_songs_from_csv():

    songs = []
    
    with open("songs.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                songs.append({"number": row["number"], "title": row["title"], "duration": row["duration"]})
    return songs

def get_menu_choice():

    while True:
        try:
            x = int(input("Choose action: "))
            if 0 <= x <=4:
                return x 
            else:
                print("Please choose an option from 0 to 4")
        except ValueError:
            print("Invalid input. Please enter a number from 0 to 4")

def get_song_list_from_user(songs,section):

    show_database(songs)

    song_list = []
    while True:
        try:

            current_song_list , current_duration = create_song_list(song_list, songs)
            show_current_song_list_detail(current_song_list,current_duration,section)
            x = input(f"Choose {section} < 0-END / B-BACK > : ")
            if x.strip().lower() == "b":
                song_list.pop()
                print("Removed")
            else:
                if check_song_number_format(x):
                    if song_number_exists(x, songs):
                        song_list.append(int(x))
                    elif int(x) == 0:
                        final_song_list , final_duration = create_song_list(song_list, songs)
                        return final_song_list, final_duration
                    else:
                        print("Song does not exist in database. Choose other number")
                else:
                    print("Invalid song number format. Please, use natural number e.x 1,2,3... etc")
        except ValueError:
            print("Invalid song number.Please, use the correct number")
        except IndexError:
            print("Empty list. Back command unavailable.")
                         
def get_event_info_from_user():

    while True:

        date = input("Event date (YYYY-MM-DD): ")

        try:
            date_object = dt.datetime.strptime(date, "%Y-%m-%d").date()
            today_date = dt.date.today()
        
            if today_date > date_object: 
                print("Invalid date. Date cannot be from past")
                continue   
            place = input("Event place: ")        
            return date,place

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def get_intro_from_user():

    intro = input("Intro: ")
    return intro

def create_song_list(user_setlist, dataset):
    setlist = []
    setlist_duration = 0
     
    for song_number in user_setlist:
             
        for row in dataset:
            if row["number"] == str(song_number):
                setlist.append({"number": row["number"], "title": row["title"]})
                setlist_duration += int(convert_time_to_sec(row["duration"]))
    return setlist, setlist_duration

def convert_time_to_sec(str_time):
     minutes, seconds = str_time.split(":")
     total = int(minutes) * 60 + int(seconds)
     return total

def convert_sec_to_time(sec_time):
    minutes = sec_time // 60
    seconds = sec_time % 60

    return minutes, seconds

def say_goodbye():
    print("""
======================================
      ALL DONE, SEE YOU NEXT TIME
======================================
                    """)

def show_database(songs):
    print("===== CURRENT DATABASE =====")
    for row in songs:
        print(f'{row["number"]}. {row["title"]} - {row["duration"]}')
    print("============================")

def add_song_to_database(songs):

    while True:

        while True:

            new_number = input("New song's number: ")
            if check_song_number_format(new_number):
                if new_number != "0":
                    break
                else:
                    print("Invalid song number. Please, don not use 0 as a song number")
            else:
                print("Invalid song number format. Please, use natural number e.x 1,2,3... etc")

        if song_number_exists(new_number, songs):
            print("This song number already exists in database.")

        else:
            
            while True:
                new_title = input("New song's title: ").strip().lower()
                if check_polish_character(new_title):
                    print("Please, use title w/o polish characters")
                else:
                    break
            while True:    
                new_duration = input("Duration of new song: ")
                if check_duration_format(new_duration):
                    songs.append({"number": new_number, "title": new_title, "duration": new_duration})
                    save_songs_to_CSV(songs)
                    break
                else:
                    print("Invalid duration value. Please use min:sec format.")
              
        if not ask_to_continue_add():
            break

def song_number_exists(number,database):

    for row in database:
        if row["number"] == number:
            return True
    return False

def ask_to_continue_add():
    
    while True:
        next_step = input("Do you want add another song? < YES / NO >")
        choice = check_yes_no_input(next_step) 
        if choice == "y":
                return True
        elif choice == "n":
            return False
        else:
            print("Invalid input. Please, use YES or NO")

def ask_to_continue_edit():

    while True:

        next_step = input("Do you want edit another song? < YES / NO >")
        choice = check_yes_no_input(next_step)
        if choice == "y":
            return True
        elif choice == "n":
            return False
        else:
            print("Invalid input. Please, use YES or NO")

def save_songs_to_CSV(songs):
    
    with open("songs.csv", "w",newline="\n") as file:
        writer = csv.DictWriter(file, fieldnames= ["number", "title", "duration"])
        writer.writeheader()
        writer.writerows(songs)
        say_save_completed()

def edit_song_in_database(songs):

    while True:

        while True:
            edit_number = input("What song would you edit?")
            if check_song_number_format(edit_number):
                break
            else:
                print("Invalid song number format. Please, use natural number e.x 1,2,3... etc")

        if song_number_exists(edit_number,songs):

            while True:
                edit_title = input("<EDIT> Song's title: ").strip().lower()
                if check_polish_character(edit_title):
                    print("Please, use title w/o polish characters")
                else:
                    break
            while True:       
                edit_duration = input("<EDIT> Duration of song: ")
                if check_duration_format(edit_duration):
                    overwrite_song_title_and_duration(edit_number,edit_title,edit_duration,songs)  
                    save_songs_to_CSV(songs)
                    break 
                else:
                    print("Invalid duration value. Please use min:sec format.")

        else:
            print("This song does not exist in database")

        if not ask_to_continue_edit():
            break

def overwrite_song_title_and_duration(edit_number,edit_title,edit_duration,songs):
    for row in songs:
            if row["number"] == edit_number:
                row.update({"title": edit_title, "duration": edit_duration})
                break

def say_save_completed():
    print('''
    
    ======================================
             SONGS SAVED TO CSV
    ======================================''')

def say_pdf_saved():
    print('''
    
    ======================================
                  PDF SAVED
    ======================================''')

def get_soundcheck_from_user(songs):

    soundcheck = {}
    show_database(songs)
    while True:
        
        soundcheck_song = input("Choose soundcheck song: ")
        if check_song_number_format(soundcheck_song):
        
            if song_number_exists(soundcheck_song,songs):
                for row in songs:
                    if soundcheck_song == row["number"]:
                        soundcheck = {"number": row["number"], "title": row["title"]}
                        return soundcheck
            else:
                print("Song does not exist in database")
                continue
        else:
            print("Invalid song number format. Please, use natural number e.x 1,2,3... etc")

def show_current_song_list_detail(song_list,duration,section):
    print(f"===== CURRENT {section.upper()} LIST =====")
    for row in song_list:
        print(f'{row["number"]}. {row["title"]}')

    minutes, seconds = convert_sec_to_time(duration)
    print("============================")
    print(f"Current {section.upper()} Duration: {minutes}min {seconds}sec")
    print("============================")
    


# ---------------------- validation functions

def check_yes_no_input(input_str):
    accepted_input = ["yes", "no", "y", "n"]
    if input_str.strip().lower() in accepted_input:
        return input_str.lower()[0]
    return False

def check_polish_character(word):
    polish_character = "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ"

    for char in word:
        if char in polish_character:
            return True
    return False

def check_duration_format(duration):

    try:
        minutes,seconds = duration.strip().split(":")
        if int(minutes) >= 0:
            if len(minutes) > 1 and minutes.startswith("0"):
                return False
            if 0 <= int(seconds) < 60:
                return True
            return False
        return False
    except ValueError:
        return False

def check_song_number_format(number):
    try:
        if 40 > int(number) >= 0:
            return True
        else:
            return False
    except ValueError:
        return False
# ----------------------

if __name__ == "__main__":
    main()
