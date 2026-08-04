import csv
import sys

def main():

    run_application()
    

    
        

    



# ---------------------- function definitions

def run_application():

    songs = load_songs_from_csv()
    while True:
    
            show_menu()
            menu_choice = get_menu_choice()
            if menu_choice == 1:
                generate_setlist(songs)
                
            elif menu_choice == 2:
                add_song_to_database(songs)

            elif menu_choice == 3:
                show_database(songs)

            elif menu_choice == 0:
                say_goodbye()
                break 
    
    

def show_menu():

    print("""
    ======================================
              SETLIST GENERATOR
    ======================================

    1. Generate setlist.
    2. Add song.
    3. Show database.
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

def get_setlist_from_user():
    setlist = []
    x = int(input("Choose first song: "))

    while x != 0:
        setlist.append(x)
        x = int(input("Choose next song: "))

    return setlist

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
    num_setlist = get_setlist_from_user()
        
    setlist , setlist_duration = create_setlist(num_setlist, songs)
            
    duration = convert_sec_to_time(setlist_duration)
    print(f"Final setlist:\n {setlist}")
    print(f"Duration: {duration}")

def convert_time_to_sec(str_time):
     minutes, seconds = str_time.split(":")
     total = int(minutes) * 60 + int(seconds)
     return total

def convert_sec_to_time(sec_time):
    minutes = sec_time // 60
    seconds = sec_time % 60

    return f"{minutes}min {seconds}sec"

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

    new_number = input("New song's number: ")
    new_title = input("New song's title: ")
    new_duration = input("Duration of new song: ")

    with open("songs.csv", "a") as file:
        writer = csv.DictWriter(file)
        writer.writerow({"number": new_number, "title": new_title, "duration": new_duration})



if __name__ == "__main__":
    main()
