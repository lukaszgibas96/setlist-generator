import csv
import sys
from pdf_generator import generate_pdf_file

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
                setlist, setlist_duration = generate_setlist(songs)
                generate_pdf_file(setlist,setlist_duration,event_date,event_place)
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
     return int(input("Choose action: "))

def get_setlist_from_user(songs):

    show_database(songs)

    setlist = []
    x = int(input("Choose first song: "))

    while x != 0:
        setlist.append(x)
        x = int(input("Choose next song: "))

    return setlist

def get_event_info_from_user():

    date = input("Event date (DD.MM.YYYY): ")
    place = input("Event place: ")

    return date,place

def create_setlist(user_setlist, dataset):
    setlist = []
    setlist_duration = 0
     
    for song_number in user_setlist:
             
        for row in dataset:
            if row["number"] == str(song_number):
                setlist.append({"number": row["number"], "title": row["title"]})
                setlist_duration += int(convert_time_to_sec(row["duration"]))
    return setlist, setlist_duration

def generate_setlist(songs):
    num_setlist = get_setlist_from_user(songs)
        
    setlist , setlist_duration = create_setlist(num_setlist, songs)
            
    print(f"Final setlist:\n {setlist}")
    print(f"Duration: {setlist_duration}")
    return setlist, setlist_duration

def convert_time_to_sec(str_time):
     minutes, seconds = str_time.split(":")
     total = int(minutes) * 60 + int(seconds)
     return total

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

        new_number = input("New song's number: ")

        if song_number_exists(new_number, songs):
            print("This song number already exists in database.")

        else:
            new_title = input("New song's title: ")
            new_duration = input("Duration of new song: ")
            songs.append({"number": new_number, "title": new_title, "duration": new_duration})

            save_songs_to_CSV(songs)

        if not ask_to_continue_add():
            break

def song_number_exists(number,database):

    for row in database:
        if row["number"] == number:
            return True
    return False

def ask_to_continue_add():
    next_step = input("Do you want add another song? < YES / NO >")
    
    if next_step == "YES":
        return True
    else:
        return False

def ask_to_continue_edit():
    next_step = input("Do you want edit another song? < YES / NO >")
    
    if next_step == "YES":
        return True
    else:
        return False

def save_songs_to_CSV(songs):
    
    with open("songs.csv", "w",newline="\n") as file:
        writer = csv.DictWriter(file, fieldnames= ["number", "title", "duration"])
        writer.writeheader()
        writer.writerows(songs)
        say_save_completed()

def edit_song_in_database(songs):

    while True:
        edit_number = input("What song would you edit?")

        if song_number_exists(edit_number,songs):

            edit_title = input("<EDIT> Song's title: ")
            edit_duration = input("<EDIT> Duration of song: ")

            overwrite_song_title_and_duration(edit_number,edit_title,edit_duration,songs)  

            save_songs_to_CSV(songs) 

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


# ---------------------- validation functions



# ----------------------

if __name__ == "__main__":
    main()
